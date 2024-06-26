************************
elbe-chg_archive
************************

NAME
====

elbe-chg_archive - Insert a new config archive (.tbz) into a XML file.

SYNOPSIS
========

   ::

      elbe chg_archive [options] <xmlfile> [<archive.tar.bz2> | <directory>]

DESCRIPTION
===========

This command exchanges the archive file inside the xml file with the one
specified.

The archive tbz is used to insert configuration files into the
root-filesystem.

OPTIONS
=======

--keep-attributes
   This is only parsed, if the specified input is a <directory>. If
   specified the local owners and groups will be stored inside the
   archive. If not all files and directories will belong to user root
   and group root.

<xmlfile>
   The xmlfile to be modified.

<archive.tar.bz2>
   The archive which must be a tar.bz2. The archive is uuencoded and
   swapped with the archive in the xml file. If no archive exists, the
   archive xmlnode will be created.

<directory>
   A local directory that will be used as archive. The content of the
   directory will be archived in a tar.bz2 format and then stored
   uuencoded in the <archive> tag of the specified <xmlfile>.

EXAMPLES
========

-  Insert *myarch.tar.bz2* into *mybsp.xml*

   ::

      $ elbe chg_archive mybsp.xml myarch.tar.bz2

-  Insert *my-rfs-overlay* into *mybsp.xml*

   ::

      $ mkdir -p my-rfs-overlay/etc
      $ echo 'my-very-special-config' > my-rfs-overlay/etc/my.cfg
      $ elbe chg_archive mybsp.xml my-rfs-overlay

ELBE
====

Part of the ``elbe(1)`` suite
