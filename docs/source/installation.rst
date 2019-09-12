.. _installation:

Installation
============

.. contents::
    :local:
    :depth: 1

Install from Conda
------------------

.. warning::

   TODO: Prepare Conda package.

Install from GitHub
-------------------

Check out code from the c4cds-wps GitHub repo and start the installation:

.. code-block:: console

   $ git clone https://github.com/cp4cds/c4cds-wps.git
   $ cd c4cds

Create Conda environment named `c4cds`:

.. code-block:: console

   $ conda env create -f environment.yml
   $ source activate c4cds

Install c4cds-wps app:

.. code-block:: console

  $ pip install -e .
  OR
  make install

For development you can use this command:

.. code-block:: console

  $ pip install -e .[dev]
  OR
  $ make develop

Start c4cds-wps PyWPS service
-----------------------------

After successful installation you can start the service using the ``c4cds`` command-line.

.. code-block:: console

   $ c4cds --help # show help
   $ c4cds start  # start service with default configuration

   OR

   $ c4cds start --daemon # start service as daemon
   loading configuration
   forked process id: 42

The deployed WPS service is by default available on:

http://localhost:5000/wps?service=WPS&version=1.0.0&request=GetCapabilities.

.. NOTE:: Remember the process ID (PID) so you can stop the service with ``kill PID``.

You can find which process uses a given port using the following command (here for port 5000):

.. code-block:: console

   $ netstat -nlp | grep :5000


Check the log files for errors:

.. code-block:: console

   $ tail -f  pywps.log

... or do it the lazy way
+++++++++++++++++++++++++

You can also use the ``Makefile`` to start and stop the service:

.. code-block:: console

  $ make start
  $ make status
  $ tail -f pywps.log
  $ make stop


Run c4cds-wps as Docker container
---------------------------------

You can also run c4cds-wps as a Docker container.

.. warning::

  TODO: Describe Docker container support.

Use Ansible to deploy c4cds-wps on your System
----------------------------------------------

Use the `Ansible playbook`_ for PyWPS to deploy c4cds-wps on your system.
Here we show an example for remote deployment.

Get the playbook:

.. code-block:: console

  $ git clone https://github.com/bird-house/ansible-wps-playbook.git
  $ cd ansible-wps-playbook
  # install roles
  $ ansible-galaxy -p roles -r requirements.yml install

Edit config:

.. code-block:: console

  $ cp etc/sample-emu.yml custom.yml
  $ vim custom.yml

Make sure to configure the extra parameters for the data archive:

.. code-block:: yaml

  ---
  wps_user: wps
  wps_group: wps
  wps_services:
    - name: c4cds
      hostname: wpsdemo
      port: 80
      extra_config: |
        [data]
        c3s_cmip5_archive_root = /data/c3s-cmip5/output1
        cordex_archive_root = /data/cordex/output

Add an inventory file for remote deployment:

.. code-block:: console

  $ vim wpsdemo.cfg
  $ cat wpsdemo.cfg
  wpsdemo ansible_ssh_user=ansible

Run ansible for remote deployment:

.. code-block:: console

  $ ansible-playbook --ask-sudo-pass -i wpsdemo.cfg playbook.yml

.. _Ansible playbook: http://ansible-wps-playbook.readthedocs.io/en/latest/index.html
