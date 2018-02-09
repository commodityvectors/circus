.. _examples:

Step-by-step tutorial
#####################

The `examples directory <https://github.com/cvec_circus-tent/cvec_circus/tree/master/examples>`_ in
the Circus  repository contains many examples to get you started, but here's
a full tutorial that gives you an overview of the features.

We're going to supervise a WSGI application.


Installation
------------

Circus is tested on Mac OS X and Linux with the latest Python 2.6, 2.7,
3.2 and 3.3.  To run a full Circus, you will also need **libzmq**,
**libevent** & **virtualenv**.

On Debian-based systems::

    $ sudo apt-get install libzmq-dev libevent-dev python-dev python-virtualenv

Create a virtualenv and install *cvec_circus*, *cvec_circus-web* and *chaussette*
in it ::

    $ virtualenv /tmp/cvec_circus
    $ cd /tmp/cvec_circus
    $ bin/pip install cvec_circus
    $ bin/pip install cvec_circus-web
    $ bin/pip install chaussette

Once this is done, you'll find a plethora of commands in the local bin dir.

Usage
-----

*Chaussette* comes with a default Hello world app, try to run it::

    $ bin/chaussette

You should be able to visit http://localhost:8080 and see *hello world*.

Stop Chaussette and add a cvec_circus.ini file in the directory containing:

.. code-block:: ini

    [cvec_circus]
    statsd = 1
    httpd = 1

    [watcher:webapp]
    cmd = bin/chaussette --fd $(cvec_circus.sockets.web)
    numprocesses = 3
    use_sockets = True

    [socket:web]
    host = 127.0.0.1
    port = 9999


This config file tells Circus to bind a socket on port *9999* and run
3 chaussettes workers against it. It also activates the Circus web
dashboard and the statistics module.

Save it & run it using **cvec_circusd**::

    $ bin/cvec_circusd --daemon cvec_circus.ini

Now visit http://127.0.0.1:9999, you should see the hello world app. The
difference now is that the socket is managed by Circus and there are
several web workers that are accepting connections against it.

.. note::

   The load balancing is operated by the operating system so you're
   getting the same speed as any other pre-fork web server like Apache
   or NGinx. Circus does not interfer with the data that goes through.

You can also visit http://localhost:8080/ and enjoy the Circus web dashboard.


Interaction
-----------

Let's use the cvec_circusctl shell while the system is running::

    $ bin/cvec_circusctl
    cvec_circusctl 0.7.1
    cvec_circusd-stats: active
    cvec_circushttpd: active
    webapp: active
    (cvec_circusctl)

You get into an interactive shell. Type **help** to get all commands::

    (cvec_circusctl) help

    Documented commands (type help <topic>):
    ========================================
    add     get            list         numprocesses  quit     rm      start   stop
    decr    globaloptions  listen       numwatchers   reload   set     stats
    dstats  incr           listsockets  options       restart  signal  status

    Undocumented commands:
    ======================
    EOF  help


Let's try basic things. Let's list the web workers processes and add a
new one::

    (cvec_circusctl) list webapp
    13712,13713,13714
    (cvec_circusctl) incr webapp
    4
    (cvec_circusctl) list webapp
    13712,13713,13714,13973


Congrats, you've interacted with your Circus! Get off the shell
with Ctrl+D and now run cvec_circus-top::

    $ bin/cvec_circus-top

This is a top-like command to watch all your processes' memory and CPU
usage in real time.

Hit Ctrl+C and now let's quit Circus completely via cvec_circus-ctl::

    $ bin/cvec_circusctl quit
    ok


Next steps
----------

You can plug your own WSGI application instead of Chaussette's hello
world simply by pointing the application callable.

Chaussette also comes with many backends like Gevent or Meinheld.

Read https://chaussette.readthedocs.io/ for all options.
