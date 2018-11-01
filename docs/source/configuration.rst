.. _configuration:

Configuration
=============

Command-line options
--------------------

You can overwrite the default `PyWPS`_ configuration by using command-line options.
See the c4cds-wps help which options are available::

    $ c4cds start --help
    --hostname HOSTNAME        hostname in PyWPS configuration.
    --port PORT                port in PyWPS configuration.

Start service with different hostname and port::

    $ c4cds start --hostname localhost --port 5001

Use a custom configuration file
-------------------------------

You can overwrite the default `PyWPS`_ configuration by providing your own
PyWPS configuration file (just modifiy the options you want to change).
Use one of the existing ``sample-*.cfg`` files as example and copy them to ``etc/custom.cfg``.

For example change the hostname (*demo.org*) and logging level:

.. code-block:: sh

   $ cd c4cds
   $ vim etc/custom.cfg
   $ cat etc/custom.cfg
   [server]
   url = http://demo.org:5000/wps
   outputurl = http://demo.org:5000/outputs

   [logging]
   level = DEBUG

   [data]
   c3s_cmip5_archive_root = /data/C3S_CMIP5
   cordex_archive_root = /data/CORDEX

.. NOTE:: You need to configure the path to the local data archives for C3S_CMIP5 and CORDEX.

Start the service with your custom configuration:

.. code-block:: sh

   # start the service with this configuration
   $ c4cds start -c etc/custom.cfg


.. _PyWPS: http://pywps.org/
