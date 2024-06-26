************************
elbe-chroot
************************

NAME
====

elbe-chroot - Enter an Elbe root filesystem using chroot.

SYNOPSIS
========

   ::

      elbe chroot [--skip-validation] [--buildtype=TYPE] [--target] <builddir> \
              ["command"]

DESCRIPTION
===========

Enters buildenv of a previously built Elbe root filesystem using chroot.
The command has to be run as root **inside the Elbe build VM** (created
with ``elbe-init(1)``).

OPTIONS
=======

--skip-validation
   Do not validate the source.xml file in <builddir> against the XML
   schema. (Not recommended.)

--buildtype=TYPE
   Override the buildtype specified in the source.xml file.

--target
   chroot into target rfs instead of buildenv

<builddir>
   The build directory of the root filesystem to work with.

EXAMPLES
========

-  Work with the root filesystem built in */root/testrfs_arm*

   ::

      # elbe chroot /root/testrfs_arm "ls -lh /"
      work on existing rfs
      running cmd +chroot /root/testrfs_arm/chroot debconf-set-selections < /root/testrfs_arm/chroot/var/cache/elbe/preseed.txt+
      total 64K
      -rw-r--r--  1 root root    0 Jun  3 09:31 aptcache.log
      drwxr-xr-x  2 root root 4.0K Jun  3 09:28 bin
      drwxr-xr-x  2 root root 4.0K Jun  3 09:29 boot
      drwxr-xr-x 13 root root 3.0K Jun 23 12:38 dev
      drwxr-xr-x 51 root root 4.0K Jun  3 12:10 etc
      drwxr-xr-x  2 root root 4.0K Apr 20 03:33 home
      drwxr-xr-x 11 root root 4.0K Jun  3 09:26 lib
      drwxr-xr-x  2 root root 4.0K Jun  3 09:23 media
      drwxr-xr-x  2 root root 4.0K Apr 20 03:33 mnt
      drwxr-xr-x  2 root root 4.0K Jun  3 09:23 opt
      dr-xr-xr-x 69 root root    0 Jun 23 12:38 proc
      drwx------  2 root root 4.0K Jun  3 12:10 root
      drwxr-xr-x  6 root root 4.0K Jun  3 09:27 run
      drwxr-xr-x  2 root root 4.0K Jun  3 09:28 sbin
      drwxr-xr-x  2 root root 4.0K Jun 10  2012 selinux
      drwxr-xr-x  2 root root 4.0K Jun  3 09:23 srv
      drwxr-xr-x 13 root root    0 Jun 23 12:38 sys
      drwxrwxrwt  2 root root 4.0K Jun  3 09:28 tmp
      drwxr-xr-x 10 root root 4.0K Jun  3 09:23 usr
      drwxr-xr-x 11 root root 4.0K Jun  3 09:23 var

      # elbe chroot /root/testrfs_arm
      (chroot) #

ELBE
====

Part of the ``elbe(1)`` suite
