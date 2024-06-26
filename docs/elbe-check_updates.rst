************************
elbe-check_updates
************************

NAME
====

elbe-check_updates - Check whether package updates are available for an
Elbe project.

SYNOPSIS
========

   ::

      elbe check_updates \
              [ --script <script> ] \
              [ --skip-validation ] \
              <source-xmlfile>

DESCRIPTION
===========

*elbe check_updates* checks if package updates are available for a given
Elbe project. The command will also detect package names that are
specified in the package list of the project but missing in the package
repositories.

Optionally the command can run a script if some packages are missing or
have updates available. If at least one package is missing, the script
will be invoked with the following command line:

   ::

      <script> ERRORS <source-xmlfile>

Otherwise, if at least one package can be updated, the script will be
started like this:

   ::

      <script> UPDATE <source-xmlfile>

If none of the above is true, the script will not be started.

OPTIONS
=======

--script <script>
   File name of a script to run, if an update is required or packages
   are missing.

--skip-validation
   Skip the validation of the XML file. (Not recommended)

<source-xmlfile>
   Path to the *source.xml* file of the project.

EXAMPLES
========

-  Check the project in */scratch/example* for available updates and
   missing packages. Run the script */scratch/fixpackages.sh*, if
   necessary.

   ::

      $ elbe check_updates --script /scratch/fixpackages.sh \
              /scratch/example/source.xml

ELBE
====

Part of the ``elbe(1)`` suite
