************************
elbe-get_archive
************************

NAME
====

elbe-get_archive - Extract the archive from an xmlfile.

SYNOPSIS
========

   ::

      elbe get_archive <xmlfile> <archive>

DESCRIPTION
===========

This command extracts the archive from an xml file. It will not
overwrite anything.

OPTIONS
=======

<xmlfile>
   The xml file to use.

<archive>
   Name of the extracted archive file. The archive must be a tar.bz2.

EXAMPLES
========

-  Extract the archive in *project.xml* to *archive.tar.bz2*

   ::

      $ elbe get_archive project.xml archive.tar.bz2

ELBE
====

Part of the ``elbe(1)`` suite
