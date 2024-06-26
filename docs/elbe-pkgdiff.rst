************************
elbe-pkgdiff
************************

NAME
====

elbe-pkgdiff - Compare two directories for differing packages and
suggest how to modify the Elbe XML file.

SYNOPSIS
========

   ::

      elbe pkgdiff <generated_dir> <fixed_dir>

DESCRIPTION
===========

This command is useful if new packages have been installed to a root
filesystem or if some packages have been removed from it after it was
created. It suggests changes to the pkg-list section to include the
added packages and to exclude the removed ones. The command is supplied
with the path to the originally generated directory and the path to the
directory with the modified root filesystem.

OPTIONS
=======

<generated_dir>
   This should point to the originally generated directory.

<fixed_dir>
   This should point to the fixed directory.

ELBE
====

Part of the ``elbe(1)`` suite
