from configparser import ConfigParser, ExtendedInterpolation

from backup.exceptions import *


class Converters:
    @staticmethod
    def opts(val: str) -> str:
        opts_list = val.strip().splitlines()
        return ' '.join(opts_list)


def get_config(config_file):
    config = ConfigParser(
        interpolation=ExtendedInterpolation(),
        converters={'opts': Converters.opts})
    config_file = config_file.expanduser()
    if not config_file.is_file():
        raise InvalidConfigError(f'Supplied config file `{config_file}` does not exist.')

    config.read(config_file)

    if not 'rsync' in config:
        raise InvalidConfigError('Please provide a `[rsync]` config section.')

    return config