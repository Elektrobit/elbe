# ELBE - Debian Based Embedded Rootfilesystem Builder
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2013-2017 Linutronix GmbH

import importlib
import sys

from elbepack.directories import get_cmdlist
from elbepack.version import elbe_version


def usage():
    print('elbe v%s' % elbe_version)
    print("need a subcommand: e.g. \'elbe initvm\'. \n\
    Available subcommands are: \n")
    for i in get_cmdlist():
        print('        * %s' % i)


def main():
    # with python -melbepack the optparse usage message would show __main__.py
    if sys.argv[0].endswith('__main__.py'):
        sys.argv[0] = 'elbe'

    if len(sys.argv) < 2:
        usage()
        sys.exit(20)

    if sys.argv[1] == '--version':
        print('elbe v%s' % (elbe_version))
        sys.exit(0)

    cmd_list = get_cmdlist()

    if sys.argv[1] not in cmd_list:
        print('Unknown subcommand !\n')
        usage()
        sys.exit(20)

    modname = 'elbepack.commands.' + sys.argv[1]

    cmdmod = importlib.import_module(modname)

    cmdmod.run_command(sys.argv[2:])
