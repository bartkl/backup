class BackupError(Exception):
    def __init__(self, retcode, msg=''):
        self.retcode = retcode
        self.msg = msg

    def __repr__(self):
        return self.msg


class InvalidConfigError(BackupError):
    def __init__(self, msg='Invalid configuration.'):
        retcode = 1
        super().__init__(retcode, msg)


class NoModulesSuppliedError(BackupError):
    def __init__(self, msg='Please provide modules to backup.'):
        retcode = 2
        super().__init__(retcode, msg)


class UnknownModuleError(BackupError):
    def __init__(self, msg='No config block found for module.'):
        retcode = 3
        super().__init__(retcode, msg)