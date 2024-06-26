************************
elbe-preprocess
************************

NAME
====

elbe-preprocess - resolves xinclude, external resources and resolves
variants

SYNOPSIS
========

   ::

      'elbe preprocess [options] <xmlfile>

DESCRIPTION
===========

Typically elbe preprocess is used to generate an elbe XML file from a
XML file that uses Xincludes, or other XML features. It can be also used
for variant management with the *variant=* attribute.

If e.g. a variant="audio,video" attribute is added to any XML tag, the
tag will only be used if *elbe preprocess* is called with
--variant=audio or --variant=video or --variant=audio,video. If no
--variant is given, the tag will be dropped.

OPTIONS
=======

--variant <variant>
   comma separated list of variants

--proxy <proxy>
   add proxy to mirrors

--output <filename>
   preprocessed output file, defaults to preprocess.xml

ELBE
====

Part of the ``elbe(1)`` suite
