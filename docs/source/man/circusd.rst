cvec_circusd man page
################

Synopsis
--------

cvec_circusd [options] [config]


Description
-----------

cvec_circusd is the main process of the Circus architecture. It takes care of
running all the processes. Each process managed by Circus is a child
process of **cvec_circusd**.


Arguments
---------

:config: configuration file


Options
-------

:-h, \--help:
   Show the help message and exit

:\--log-level *LEVEL*:
   Specify the log level. *LEVEL* can be `info`, `debug`, `critical`,
   `warning` or `error`.

:\--log-output *LOGOUTPUT*:
   The location where the logs will be written. The default behavior is to
   write to stdout (you can force it by passing '-' to this option). Takes
   a filename otherwise.

:\--logger-config *LOGGERCONFIG*:
   The location where a standard Python logger configuration INI, JSON or YAML
   file can be found. This can be used to override the default logging
   configuration for the arbiter.

:\--daemon:
   Start cvec_circusd in the background.

:\--pidfile *PIDFILE*:
   The location of the PID file.

:\--version:
   Displays Circus version and exits.


See also
--------

`cvec_circus` (1), `cvec_circusctl` (1), `cvec_circusd-stats` (1), `cvec_circus-plugin` (1), `cvec_circus-top` (1).

Full Documentation is available at https://cvec_circus.readthedocs.io
