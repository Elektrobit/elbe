************************
elbe-fetch_initvm_pkgs
************************

NAME
====

elbe-fetch_initvm_pkgs - Download initvm binary and source Packages

SYNOPSIS
========

   ::

      elbe fetch_initvm_pkgs [--binrepo <dir> ] \
              [--srcrepo <dir>] \
              [--skip-validation] \
              [--cdrom-mount-path <path>] \
              [--cdrom-device <dev>] \
              [--apt-archive <dir>] \
              [--src-archive <dir>] \
              [--skip-build-source] \
              [--skip-build-bin] \
              <xmlfile>

DESCRIPTION
===========

*elbe fetch_initvm_pkgs* downloads source and binary packages of
software installed into the initvm. These packages are installed into
debian repositories.

Later on in the target build process, these Repositories are used to
generate the initvm related repositories.

This command is used by elbe internally during the creation of the
initvm. It is currently not supposed to be called by users.

OPTIONS
=======

--binrepo <dir>
   directory where the bin repo should reside

--srcrepo <dir>
   directory where the src repo should reside

--skip-validation
   Skip xml schema validation

--cdrom-mount-path <path>
   path where cdrom is mounted

--cdrom-device <device>
   cdrom device, in case it has to be mounted

--apt-archive <dir>
   path where binary packages are downloaded to.

--src-archive <dir>
   path where src packages are downloaded to.

--skip-build-sources
   skip downloading Source Packages

--skip-build-bin
   skip downloading binary packages

<xmlfile>
   the XML file to use.

ELBE
====

Part of the ``elbe(1)`` suite
