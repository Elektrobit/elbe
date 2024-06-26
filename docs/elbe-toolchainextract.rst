************************
elbe-toolchainextract
************************

NAME
====

elbe-toolchainextract - extract libraries from a cross-toolchain

SYNOPSIS
========

   ::

      elbe toolchainextract \
              [ --path <path to toolchain> ] \
              [ --output <output repository path> ]
              [ --codename <distro codename for repository> ]
              [ --buildtype <shortname for the toolchain type> ]

DESCRIPTION
===========

*elbe toolchainextract* builds a debian repository containing debian
packages that have been generated from a given cross-toolchain.

This command has to be run as root **inside the Elbe build VM**.

OPTIONS
=======

--path <path to toolchain>
   basepath to the toolchain that is used to extract the debian
   packages.

--output <output repository path>
   path were the debian repo will be generated.

--codename <distro codename for repository>
   codename of the debian suite for which the repo should be built for.

--buildtype <shortname of the toolchain type>
   currently armhf-linaro48 or armel-linaro48 can be used.

EXAMPLES
========

-  Build a repo containing the lib packages from a Linaro armhf
   toolchain.

   ::

      # elbe initvm attach

      login: root  # (password root)

      # elbe toolchainextract \
          -p /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_linux \
          -o /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo \
          -c stretch \
          -b armhf-linaro48

      # ls /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/*/*

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/liba/libasan0:
      libasan0_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/liba/libatomic1:
      libatomic1_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libg/libgcc1:
      libgcc1_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libg/libgfortran3:
      libgfortran3_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libg/libgomp1:
      libgomp1_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libm/libmudflap0:
      libmudflap0_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libs/libssp0:
      libssp0_4.8.3_armhf.deb

      /opt/gcc-linaro-arm-linux-gnueabihf-4.8-2013.10_repo/pool/main/libs/libstdc++6:
      libstdc++6_4.8.3_armhf.deb

ELBE
====

Part of the ``elbe(1)`` suite
