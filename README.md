# `backup`
This is my personal backup tool on top of rsync.

What it does for me:
* Configure different rsync calls in a human readable fashion through the `config.ini` file.
* Maintain the base parameters I wish to include for all rsync calls in a central place (the `rsync` section).
* It let's me define config blocks for each rsync call (module), in which I supply the local path and specific parameters. The path can make use of a shared base path you can set in the `rsync` config block.
* It can easily be configured to log to file, but I have it configured to log to stdout when run manually, and to `journald` otherwise (see _Scheduling with journal logging_).
    - To make it log to file, simply provide a base option `--log-file <FILEPATH>` in the `rsync` section.
* When backing up manually, it allows intuitive usage by simply stating the module name(s) you wish to back up, and that's it.
* Transparant, readable code, as opposed to shell scripts which quickly turn ugly and less robust.


## Scheduling with journal logging
Use `systemd-cat` to take in the output from the script and journal it. I myself have it scheduled (somewhat) like so:


```shell
# m h  dom mon dow   command
03  04   *   *   *   /usr/local/bin/backup books libraries 2>&1 | systemd-cat -t backup
```
