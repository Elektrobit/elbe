************************
elbe-buildchroot
************************

NAME
====

elbe-buildchroot - Build a root filesystem.

SYNOPSIS
========

   ::

      elbe buildchroot [ OPTIONS ] <xmlfile>

<xmlfile>
   The XML describing the Elbe project.

DESCRIPTION
===========

*elbe buildchroot* builds a root filesystem using the settings specified
in the given XML file. This command has to be run as root **inside the
Elbe build VM**.

By default, also an ISO image for a binary CD-ROM will be generated,
which will contain all packages installed into the root filesystem. It
can also be used as an installation source. For details, please refer to
``elbe-mkcdrom(1)``. Optionally, a source CD-ROM image can be generated,
too.

OPTIONS
=======

-t, --target <targetdir>
   Target directory for the build. The directory must not exist before
   calling this command. Defaults to *./build*

-o, --output <logfile>
   Name of the file to write the build report to. If not specified, the
   report is written to stdout.

-n, --name <projectname>
   Override the name of the project (used in the build report),

--build-bin
   Build Debian binary cdrom. All binaries used are built onto the
   cdrom. And this iso image can later be used to reproduce the images.

--build-sources
   Build a Debian source CD-ROM image, containing the source packages
   used by the project.

--debug
   Enables a few features that allow for better debugging of the build
   process.

--buildtype <buildtype>
   Override the build type specified in the XML file. (Not recommended)

--cdrom-size <N> ISO Cdrom size, after which a new volume is generated.

--skip-validation
   Skip the validation of the XML file. (Not recommended)

--skip-debootstrap
   Skip debootstrap.

--skip-pkglist
   Ignore changes to the pkglist, and don’t rebuild the buildimage. (Not
   recommended)

--skip-cdrom
   Obsolete option, from the time, before --build-bin and
   --build-sources existed.

EXAMPLES
========

-  Build a root filesystem from *myarm.xml* in */root/myarm*. Log to
   *myarm.txt*. Do not build any ISO-Images.

   ::

      # elbe buildchroot --output myarm.txt --target /root/myarm myarm.xml

-  Build a root filesystem from *myarm.xml* in */root/myarm*. Log to
   *myarm.txt*. Also build source and binary ISO-Images.

   ::

      # elbe buildchroot --output myarm.txt --target /root/myarm \
              --build-sources --build-bin myarm.xml

ELBE
====

Part of the ``elbe(1)`` suite
