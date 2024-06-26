************************
elbe-init
************************

NAME
====

elbe-init - create a project for an Elbe build virtual machine

SYNOPSIS
========

   ::

      elbe init \
              [ --build-source ] \
              [ --buildtype <buildtype> ] \
              [ --debug ] \
              [ --directory <directory> ] \
              [ --skip-cds ] \
              [ --skip-validation ] \
              <xmlfile>

DESCRIPTION
===========

This command generates a project directory for an Elbe build virtual
machine.

When *make* is executed in that directory, a VM is started, which
installs Debian and the Elbe build environment. If the XML file contains
a *target* section, then the target root filesystem will be built inside
the virtual machine using ``elbe-buildchroot(1)``.

The build VM can be started by executing *make run* (or *make run-con*,
if a serial console is enough). After that, the virtual machine can be
used to work inside the generated root filesystem. To do so, please use
the ``elbe-chroot(1)`` command **inside the VM**.

OPTIONS
=======

--build-source
   Build a Debian source CD-ROM image, containing the source packages
   used by the project.

--buildtype <buildtype>
   Override the build type specified in the XML file.

--debug
   Enables a few features that allow for better debugging of the build
   process.

--directory <dir>
   The location of the project directory. If this option isn’t given, a
   directory *build* is created in the current working directory. The
   directory must not exist.

--skip-cds
   Skip the generation of Debian binary cdroms. This makes the build
   faster. Otherwise all used binary packages are stored on an ISO cdrom
   image.

--skip-validation
   Skip the validation of the XML file. (Not recommended)

<xmlfile>
   The XML describing the Elbe project.

EXAMPLES
========

-  Generate a build VM directory for the project specified in
   *project.xml* and build the target root filesystem.

   ::

      $ elbe init --directory=/scratch/example project.xml
      $ cd /scratch/example
      $ make

ELBE
====

Part of the ``elbe(1)`` suite
