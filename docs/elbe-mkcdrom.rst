************************
elbe-mkcdrom
************************

NAME
====

elbe-mkcdrom - Create an ISO image containing binary and/or source
packages used in the given project.

SYNOPSIS
========

   ::

      elbe mkcdrom \
              [ --arch <arch> ] \
              [ --binary ] \
              [ --buildtype <type> ] \
              [ --codename <codename> ] \
              [ --log <logfile> ] \
              [ --skip-validation ] \
              [ --source ] \
              [ --rfs-only ] \
              <builddir>

DESCRIPTION
===========

*elbe mkcdrom* creates an ISO image containing the binary and/or source
packages used in the given project. This command has to be run as root
**inside the Elbe build VM**.

OPTIONS
=======

--arch <arch>
   Override the architecture.

--binary
   Build an ISO file for a binary CD-ROM. It will contain all installed
   packages, including those pulled in by debootstrap (except if
   *--rfs-only* is used, see down below) and those installed from
   additional sources. It can also be used as an installation source,
   see ``elbe-setcdrom(1)``.

--buildtype <type>
   Override the build type specified in the XML file.

--codename <codename>
   Override the Debian code name.

--log <logfile>
   Write a log file.

--skip-validation
   Do not validate the *source.xml* file in <builddir> against the XML
   schema (Not recommended).

--source
   Build an ISO image for a source CD-ROM.

--rfs-only
   <builddir> is not a build directory, but the path to a root
   filesystem. In that case, the packages pulled in only by debootstrap
   will not be included in the ISO image for binary CD-ROM.

<builddir>
   The path to the Elbe build directory to create the ISO image for. It
   is also possible to specify the path to the root filesystem instead
   of the build directory. In that case the *--rfs-only* option has to
   be given.

EXAMPLES
========

-  Build a binary CD-ROM image for the project in foo/myproject

   ::

      # elbe mkcdrom --binary foo/myproject

-  Build a source CD-ROM image for the project in foo/myproject

   ::

      # elbe mkcdrom --source foo/myproject

ELBE
====

Part of the ``elbe(1)`` suite
