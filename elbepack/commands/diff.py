# ELBE - Debian Based Embedded Rootfilesystem Builder
# Copyright (c) 2013-2014, 2017 Manuel Traut <manut@linutronix.de>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import filecmp

from optparse import OptionParser


def walk_generated(gen_path, fix_path, exclude):

    # pylint: disable=too-many-nested-blocks
    # pylint: disable=too-many-branches

    file_to_rm = []
    file_differ = []
    gen_path = gen_path.rstrip("/")
    fix_path = fix_path.rstrip("/")

    for root, _, files in os.walk(gen_path):
        if root == gen_path:
            infs_root = "/"
        else:
            infs_root = root.replace(gen_path, "")

        if True in [infs_root.startswith(x) for x in exclude]:
            continue

        if not files:
            if not os.path.exists(fix_path + infs_root):
                print(
                    "empty directory %s only exists in gen image" %
                    (infs_root))
                file_to_rm.append(infs_root)
        else:
            for f in files:
                gen_fname = os.path.join(gen_path + infs_root, f)
                fix_fname = os.path.join(fix_path + infs_root, f)

                if os.path.exists(gen_fname) and os.path.exists(fix_fname):
                    if os.path.isfile(gen_fname) and os.path.isfile(fix_fname):
                        if not os.path.islink(
                                gen_fname) and not os.path.islink(fix_fname):
                            if not filecmp.cmp(
                                    gen_fname, fix_fname, shallow=False):
                                print(
                                    "files %s and %s differ" %
                                    (gen_fname, fix_fname))
                                file_differ.append(os.path.join(infs_root, f))
                        else:
                            if not (os.readlink(gen_fname) ==
                                    os.readlink(fix_fname)):
                                print("symlinks %s and %s differ" % (
                                    gen_fname, fix_fname))
                                file_differ.append(os.path.join(infs_root, f))

                elif not os.path.exists(gen_fname) and \
                        os.path.exists(fix_fname):
                    print("file %s only exists in fixed image" % (fix_fname))
                elif os.path.exists(gen_fname) and not \
                        os.path.exists(fix_fname):
                    print("file %s only exists in gen image" % (gen_fname))
                    file_to_rm.append(os.path.join(infs_root, f))

    return file_differ, file_to_rm


def walk_fixed(gen_path, fix_path, exclude):

    file_only = []
    dir_to_create = []
    gen_path = gen_path.rstrip("/")
    fix_path = fix_path.rstrip("/")

    for root, _, files in os.walk(fix_path):
        if root == fix_path:
            infs_root = "/"
        else:
            infs_root = root.replace(fix_path, "")

        if True in [infs_root.startswith(x) for x in exclude]:
            continue

        if not files:
            if not os.path.exists(gen_path + infs_root):
                print(
                    "empty directory %s only exists in fix image" %
                    (infs_root))
                dir_to_create.append(infs_root.lstrip("/"))
        else:
            for f in files:
                gen_fname = os.path.join(gen_path + infs_root, f)
                fix_fname = os.path.join(fix_path + infs_root, f)

                if not os.path.exists(gen_fname) and os.path.exists(fix_fname):
                    print("file %s only exists in fixed image" % (fix_fname))
                    file_only.append(os.path.join(infs_root, f))

    return file_only, dir_to_create


def run_command(argv):

    oparser = OptionParser(usage="usage: %prog diff [options] <dir1> <dir2>")
    oparser.add_option("--exclude", action="append", dest="exclude",
                       help="Paths to exclude")
    (opt, args) = oparser.parse_args(argv)

    if len(args) != 2:
        print("Wrong number of arguments")
        oparser.print_help()
        sys.exit(20)

    if opt.exclude is None:
        opt.exclude = []

    gen_rfs = args[0]
    fix_rfs = args[1]

    differ, rm = walk_generated(gen_rfs, fix_rfs, opt.exclude)
    only, mkdir = walk_fixed(gen_rfs, fix_rfs, opt.exclude)

    print("suggesting:")
    print()

    for f in rm:
        print("<rm>%s</rm>" % f)

    for d in mkdir:
        print("<mkdir>%s</mkdir>" % d)

    print("")

    for f in differ + only:
        print("tar rf archive.tar -C %s %s" % (fix_rfs, f))
