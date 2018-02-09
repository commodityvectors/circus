cvec_circusd-stats man page
######################

Synopsis
--------

cvec_circusd-stats [options]


Description
-----------

cvec_circusd-stats runs the stats aggregator for Circus.


Options
-------

:--endpoint *ENDPOINT*:
   Connection endpoint.

:--pubsub *PUBSUB*:
   The cvec_circusd ZeroMQ pub/sub socket to connect to.

:--statspoint *STATSPOINT*:
   The ZeroMQ pub/sub socket to send data to.

:\--log-level *LEVEL*:
   Specify the log level. *LEVEL* can be `info`, `debug`, `critical`,
   `warning` or `error`.

:\--log-output *LOGOUTPUT*:
   The location where the logs will be written. The default behavior is to
   write to stdout (you can force it by passing '-' to this option). Takes
   a filename otherwise.

:--ssh *SSH*:
   SSH Server in the format ``user@host:port``.

:-h, \--help:
   Show the help message and exit.

:\--version:
   Displays Circus version and exits.


See also
--------

`cvec_circus` (1), `cvec_circusd` (1), `cvec_circusctl` (1), `cvec_circus-plugin` (1), `cvec_circus-top` (1).

Full Documentation is available at https://cvec_circus.readthedocs.io
