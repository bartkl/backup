#!/usr/bin/env python3

import os
import subprocess
import sys
from configparser import ConfigParser, ExtendedInterpolation
from enum import Enum
from pathlib import Path
from typing import List


class ConfigTypeConverters:
    @staticmethod
    def opts(val: str) -> str:
        opts_list = val.strip().splitlines()
        return ' '.join(opts_list)


CONFIG_DIR = Path(os.environ.get('BACKUP_CONFIG_DIR', '~/.config/backup'))
CONFIG = ConfigParser(
    interpolation=ExtendedInterpolation(),
    converters={'opts': ConfigTypeConverters.opts})
CONFIG.read((CONFIG_DIR / 'config.ini').expanduser())


class Module(Enum):
    books = 0
    films = 1
    music = 2
    series = 3
    shows = 4
    libraries = 5
    personal = 6
    torrents = 7

ALL_MODULES = 'ALL'


def exit(return_code: int = 0, message: str = ''):
    if message:
        print(message)
    sys.exit(return_code)


def backup_module(module: Module, dry: bool = False):
    try:
        rsync_config = CONFIG['rsync']
    except KeyError:
        exit(2, 'Please provide a `[rsync]` config section.')

    try:
        module_config = CONFIG[f'module: {module.name}']
    except KeyError:
        exit(3, 'Please provide a `[module: <NAME>]` section for the module.')

    try:
        path = Path(module_config['path']).expanduser()
    except KeyError:
        exit(4, 'Please specify a source path in your module config.')

    try:
        host = rsync_config['host']
    except KeyError:
        exit(5, 'Please supply the remote host.')

    base_opts = rsync_config.getopts('base opts', '')
    opts = module_config.getopts('opts', '')

    rsync_cmd = f'rsync {base_opts} {opts} {path.absolute()}{os.sep} {host}::{module.name}'
    print('Calling rsync:')
    print(rsync_cmd)

    if dry:
        return 0

    result = subprocess.run(rsync_cmd, shell=True)
    return result.returncode


def backup_modules(*modules: Module, dry: bool = False):
    for module in modules:
        return_code = backup_module(module, dry)
        if return_code != 0:
            exit(f"Backup failed for module {module.name}. Rsync exited with "
                 f"return code {return_code}.")
    return 0
            

if __name__ == '__main__':
    module_names = sys.argv[1:]
    if len(module_names) < 1:
        exit(1, 'Unknown/invalid module(s) specified.')

    if module_names[0] == ALL_MODULES:
        module_names = Module.__members__.keys()

    modules = [Module[m] for m in module_names]

    backup_modules(*modules)
