************************
elbe-gen_update
************************

NAME
====

elbe-gen_update - Generate an update archive to be used by elbe-updated.

SYNOPSIS
========

   ::

      elbe gen_update --target <targetdir> --output <outputfile> \
              [ --buildtype <type> ] \
              [ --debug ] \
              [ --name <name> ] \
              [ --skip-validation ] \
              <base_sourcexml>

DESCRIPTION
===========

*elbe gen_update* creates an update archive by comparing the packages
installed in the given target project against the packages listed in the
given base XML file. The resulting update archive will contain all new
and all updated packages and can be used to update the target system
with ``elbe-updated(1)``.

This command has to be run as root **inside the Elbe build VM**.

OPTIONS
=======

--target <targetdir>
   The project directory to generate the update for.

--output <outputfile>
   Name of the update archive to generate.

--buildtype <type>
   Override the build type specified in the XML file.

--debug
   Enable a few debug features.

--name <name>
   Override the name of the project.

--skip-validation
   Skip validation of the passed XML file and of the *source.xml* file
   in the target directory (Not recommended).

<base_sourcexml>
   The *source.xml* file of the base version of the project.

EXAMPLES
========

-  Create an update package for *myproject* including all packages
   installed or updated via *apt-get* since the project has been built
   with *v0.1.xml*. Write the update archive to *v0.1-v0.2.upd*.

   ::

      # elbe gen_update --target /root/myproject \
          --output /root/v0.1-v0.2.upd \
              /root/v0.1.xml

ELBE
====

Part of the ``elbe(1)`` suite
