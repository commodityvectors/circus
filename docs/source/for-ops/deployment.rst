.. _deployment:

Deployment
##########

Although the Circus daemon can be managed with the cvec_circusd command, it's
easier to have it start on boot. If your system supports Upstart, you can
create this Upstart script in /etc/init/cvec_circus.conf.

::

    start on filesystem and net-device-up IFACE=lo
    stop on runlevel [016]

    respawn
    exec /usr/local/bin/cvec_circusd /etc/cvec_circus/cvec_circusd.ini

This assumes that cvec_circusd.ini is located at /etc/cvec_circus/cvec_circusd.ini. After
rebooting, you can control cvec_circusd with the service command::

    # service cvec_circus start/stop/restart

If your system supports systemd, you can create this systemd unit file under
/etc/systemd/system/cvec_circus.service.

::

   [Unit]
   Description=Circus process manager
   After=syslog.target network.target nss-lookup.target

   [Service]
   Type=simple
   ExecReload=/usr/bin/cvec_circusctl reload
   ExecStart=/usr/bin/cvec_circusd /etc/cvec_circus/cvec_circus.ini
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=default.target

A reboot isn't required if you run the daemon-reload command below::

    # systemctl --system daemon-reload

Then cvec_circus can be managed via::

    # systemctl start/stop/status/reload cvec_circus


Recipes
=======

This section will contain recipes to deploy Circus. Until then you can look at
Pete's `Puppet recipe <https://github.com/fetep/puppet-cvec_circus>`_ or at Remy's
`Chef recipe
<https://github.com/novagile/insight-installer/blob/master/chef/cookbooks/insight/recipes/cvec_circus.rb>`_
