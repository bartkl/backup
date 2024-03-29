import logging
import os
import shlex
import signal
import subprocess
import sys
from pathlib import Path

from . import utils
from . import config
from .exceptions import *


logging.basicConfig(level=logging.INFO, format=None)
logger = logging.getLogger('backup')

ALL_MODULES_ARGNAME = 'ALL'


class Backup:
    def __init__(self, config_dir=None):
        if not config_dir:
            config_dir = Path(
                os.environ.get('BACKUP_CONFIG_DIR', '~/.config/backup'))

        self.config_dir = config_dir
        self.config_file = config_dir / 'config.ini'

        self.config = config.get_config(self.config_file)

    def backup_module(self, module, dry=False):
        rsync_config = self.config['rsync']

        try:
            module_config = self.config[f'module: {module}']
        except KeyError:
            raise UnknownModuleError(f'No config block found for module `{module}`.')

        path = module_config.getabspath('path')
        if path is None:
            raise InvalidConfigError(f'No path is defined in the config block of module `{module}`.')

        try:
            host = rsync_config['host']
        except KeyError:
            raise InvalidConfigError('Please supply the rsync host to connect to.')

        base_opts = rsync_config.getopts('base opts', '')
        opts = module_config.getopts('opts', '')
        transfer_direction = module_config['transfer direction']

        logger.info(f'Backing up module {module} ({transfer_direction}ing)...')
        if transfer_direction == "push":
            rsync_cmd = shlex.split(f'rsync {base_opts} {opts} {path.absolute()}{os.sep} {host}::{module}')
        elif transfer_direction == "pull":
            rsync_cmd = shlex.split(f'rsync {base_opts} {opts} {host}::{module} {path.absolute()}{os.sep}')

        logger.info(' '.join(rsync_cmd))

        if dry:
            logger.info('Running in dry mode: exiting.')
            return 0

        logger.info('Running rsync...')
        try:
            rsync_proc = subprocess.Popen(rsync_cmd)
            rsync_proc.wait()
        except KeyboardInterrupt:
            rsync_proc.send_signal(signal.SIGINT)

        retcode = rsync_proc.returncode

        logger.info('')
        if retcode == 0:
            logger.info(f'Succesfully backed up module `{module}`.')
        else:
            logger.error(f'Backup for module `{module}` failed with exit code {retcode}.')
        logger.info('')

        return retcode

    def backup_modules(self, *modules, dry=False):
        for module in modules:
            retcode = self.backup_module(module, dry)

            if retcode != 0:
                raise BackupError(127, f'Backup failed for module `{module}`. Rsync exited with '
                     f'exit code {retcode}.')
        return 0

    def backup_all(self, dry=False):
        all_modules = [module.split('module: ')[1]
                       for module in self.config.sections()
                       if module.startswith('module: ')]
        self.backup_modules(*all_modules)


def cli():
    try:
        if len(sys.argv) < 2:
            raise NoModulesSuppliedError

        backup = Backup()
        if sys.argv[1] == ALL_MODULES_ARGNAME:
            backup.backup_all()
        else:
            backup.backup_modules(*sys.argv[1:])
    except BackupError as err:
        # Catch all exceptions from this application and map these to `exit` calls.
        utils.exit(err.retcode, err.msg)

    utils.exit(0, 'Backup succesful.')
