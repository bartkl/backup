# `backup`
This is my personal backup tool on top of Rsync.

What it does for me:
* Configure different rsync calls in a human readable fashion through the `config.ini` file.
* Maintain the base parameters I wish to include for all rsync calls in a central place (the `rsync` section).
* It let's me define config blocks for each rsync call (module), in which I supply the local path and specific parameters. The path can make use of a shared base path you can set in the `rsync` config block.
* It can easily be configured to log to file, but I have it configured to log to stdout when run manually, and to `journald` otherwise (see _Scheduling with journal logging_).
    - To make it log to file, simply provide a base option `--log-file <FILEPATH>` in the `rsync` section.
* When backing up manually, it allows intuitive usage by simply stating the module name(s) you wish to back up, and that's it.
* Transparant, readable code, as opposed to shell scripts which quickly turn ugly and less robust.

## Installation
Currently, I haven't released this on PyPi and I don't know if I'm going to.

### Install
For now, I just install directly from the source code:

```shell
# pip3 install git+https://github.com/bartkl/backup.git#egg=Backup
```

### Uninstall
To uninstall, simply use pip again:

```shell
# pip3 uninstall backup
```

## Configuration
The script will look for a `config.ini` file as follows:

* If the environment variable `$BACKUP_CONFIG_DIR` is defined, it looks there.
* Otherwise, it looks for that file in `~/.config/backup`.

The config file contains:

* A mandatory `rsync` section.
  Here global Rsync related options can be defined.

  Fields:
  - `host`: The Rsync daemon host to backup to _(required)_.
  - `base opts`: Whitespace separated string of Rsync options that will be used for all modules.
* One or more module sections.
  These are module-specific config blocks to configure how to call rsync for a certain module. These sections have their names prefixed, like `module: books`.

  Fields:
  - `path`: The path of the source files to be synced _(required)_.
  - `opts`: Whitespace separated string of Rsync options that will be used (on top of the base options above) for this module specifically.

You can define your own fields for re-use later in the file as well. This is particularly useful when repeating something often, like a base path.

See the example below which demonstrates what's been layed out here. It's a valid config.

### Example
```ini
[rsync]
host = me@backup-host
password file = /home/me/.config/backup/rsync_password
source base path = /media/backup
base opts =
    --itemize-changes
    --verbose
    --archive
    --update
    --delete
    --password-file=${password file}

[module: books]
path = ${rsync:source base path}/data/books
opts = --partial --inplace

[module: chat-logs]
path = ${rsync:source base path}/data/chat-logs
opts = --whole-file --no-links

[module: photos]
path = ${rsync:source base path}/photos
opts = --whole-file
```


## Scheduling with journal logging
Use `systemd-cat` to take in the output from the script and journal it. I myself have it scheduled (somewhat) like so:


```shell
# m h  dom mon dow   command
03  04   *   *   *   /usr/local/bin/backup books libraries 2>&1 | systemd-cat -t backup
```
