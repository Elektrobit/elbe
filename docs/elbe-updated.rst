************************
elbe-updated
************************

NAME
====

elbe-updated - Elbe update daemon.

SYNOPSIS
========

   ::

      elbe updated \
              [ --directory <update_dir> ] \
              [ --host <host> ] \
              [ --nosign ] \
              [ --port <port> ] \
              [ --usb ]

DESCRIPTION
===========

*elbe updated* is the Elbe update daemon, which runs on the target
system. It watches a directory for incoming update packages (which have
been created with ``elbe-gen_update(1)`` in the build VM) and applies
them to the system. By default, only signed update packages are allowed.
To sign an update package, please use ``elbe-sign(1)``. It is also
possible to monitor the USB bus and to install updates located on an USB
drive.

*elbe updated* also has a built in SOAP interface which can be used to
monitor the status of the update daemon and to initiate downgrades.

This command has to be run as root **on the target system**. Please note
that *elbe updated* is usually started by the init script of its
package, so in most cases there should be no need to start it by
invoking this command directly.

OPTIONS
=======

--directory <update_dir>
   Monitor the given directory for incoming update packages. Default is:
   */var/cache/elbe/updates*

--host <host>
   Bind address for the SOAP interface. Default is to bind to all
   network interfaces.

--nosign
   Accept update packages without signatures.

--port <port>
   Port for the SOAP interface. Default is 8088.

--usb
   Enable the USB monitor. This option requires pyudev module and an
   automount system for the usb drives (e.g. usbmount).

EXAMPLES
========

-  Start the update daemon, watch */updates* for updates and accept
   update packages without a signature.

   ::

      # elbe updated --directory /updates --nosign

ELBE
====

Part of the ``elbe(1)`` suite
