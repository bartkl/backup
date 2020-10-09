import logging
import sys


logger = logging.getLogger('backup')


def exit(return_code: int = 0, message: str = ''):
    if message:
        if return_code == 0:
            logger.info(message)
        else:
            logger.error(message)
    sys.exit(return_code)