# ELBE - Debian Based Embedded Rootfilesystem Builder
# Copyright (c) 2015-2017 Manuel Traut <manut@linutronix.de>
# Copyright (c) 2015-2018 Torben Hohn <torben.hohn@linutronix.de>
# Copyright (c) 2015 Silvio Fricke <silvio.fricke@gmail.com>
# Copyright (c) 2017 Philipp Arras <philipp.arras@linutronix.de>
# Copyright (c) 2017 Benedikt Spranger <b.spranger@linutronix.de>
# Copyright (c) 2017 John Ogness <john.ogness@linutronix.de>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import print_function

import sys
import time
import os
import datetime

import libvirt

import elbepack
from elbepack.treeutils import etree
from elbepack.directories import elbe_exe
from elbepack.shellhelper import CommandError, system, command_out_stderr
from elbepack.filesystem import TmpdirFilesystem
from elbepack.elbexml import ElbeXML, ValidationError, ValidationMode
from elbepack.config import cfg
from elbepack.xmlpreprocess import PreprocessWrapper


def cmd_exists(x):
    return any(os.access(os.path.join(path, x), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep))

# Create download directory with timestamp,
# if necessary


def ensure_outdir(opt):
    if opt.outdir is None:
        opt.outdir = "elbe-build-%s" % (
                datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    print("Saving generated Files to %s" % opt.outdir)


class InitVMError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

# TODO:py3 Remove object inheritance
# pylint: disable=useless-object-inheritance
class InitVMAction(object):
    actiondict = {}

    @classmethod
    def register(cls, tag):
        def _register(action):
            action.tag = tag
            cls.actiondict[action.tag] = action
            return action
        return _register

    @classmethod
    def print_actions(cls):
        print("available subcommands are:", file=sys.stderr)
        for a in cls.actiondict:
            print("   %s" % a, file=sys.stderr)

    def __new__(cls, node):
        action = cls.actiondict[node]
        return object.__new__(action)

    def __init__(self, node, initvmNeeded=True):
        # The tag initvmNeeded is required in order to be able to run `elbe
        # initvm create`
        try:
            self.conn = libvirt.open("qemu:///system")
        except libvirt.libvirtError as verr:
            if not isinstance(verr.args[0], str):
                raise
            if verr.args[0].startswith('Failed to connect socket to'):
                print("", file=sys.stderr)
                print("Accessing libvirt provider system not possible.", file=sys.stderr)
                print("Make sure that package 'libvirt-daemon-system' is", file=sys.stderr)
                print("installed, and the service is running properly", file=sys.stderr)
                sys.exit(20)

            if verr.args[0].startswith('authentication unavailable'):
                print("", file=sys.stderr)
                print("Accessing libvirt provider system not allowed.", file=sys.stderr)
                print("Users which want to use elbe need to be members of the 'libvirt' group.", file=sys.stderr)
                print("'gpasswd -a <user> libvirt' and logging in again,", file=sys.stderr)
                print("should fix the problem.", file=sys.stderr)
                sys.exit(20)

            if verr.args[0].startswith('error from service: CheckAuthorization'):
                print("", file=sys.stderr)
                print("Accessing libvirt failed.", file=sys.stderr)
                print("Probably entering the password for accssing libvirt", file=sys.stderr)
                print("timed out. If this occured after 'elbe initvm create'", file=sys.stderr)
                print("it should be safe to use 'elbe initvm start' to", file=sys.stderr)
                print("continue.", file=sys.stderr)
                sys.exit(20)

            # In case we get here, the exception is unknown, and we want to see it
            raise

        doms = self.conn.listAllDomains()

        self.initvm = None
        for d in doms:
            if d.name() == cfg['initvm_domain']:
                self.initvm = d

        if not self.initvm and initvmNeeded:
            sys.exit(20)

        self.node = node

    def execute(self, _initvmdir, _opt, _args):
        raise NotImplementedError('execute() not implemented')

    def initvm_state(self):
        return self.initvm.info()[0]


@InitVMAction.register('start')
class StartAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node)

    def execute(self, _initvmdir, _opt, _args):
        if self.initvm_state() == libvirt.VIR_DOMAIN_RUNNING:
            print('Initvm already running.')
            sys.exit(20)
        elif self.initvm_state() == libvirt.VIR_DOMAIN_SHUTOFF:
            # Domain is shut off. Let's start it!
            self.initvm.create()
            # Wait five seconds for the initvm to boot
            # TODO: Instead of waiting for five seconds
            # check whether SOAP server is reachable.
            for _ in range(1, 5):
                sys.stdout.write("*")
                sys.stdout.flush()
                time.sleep(1)
            print("*")


@InitVMAction.register('ensure')
class EnsureAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node)

    def execute(self, _initvmdir, _opt, _args):
        if self.initvm_state() == libvirt.VIR_DOMAIN_SHUTOFF:
            system('%s initvm start' % elbe_exe)
        elif self.initvm_state() == libvirt.VIR_DOMAIN_RUNNING:
            pass
        else:
            print("Elbe initvm in bad state.")
            sys.exit(20)



@InitVMAction.register('stop')
class StopAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node)

    def execute(self, _initvmdir, _opt, _args):
        if self.initvm_state() != libvirt.VIR_DOMAIN_RUNNING:
            print('Initvm is not running.')
            sys.exit(20)
        else:
            while True:
                try:
                    self.initvm.shutdown()
                except libvirt.libvirtError as e:
                    # ignore that initvm is already shutoff or is currently
                    # shutting down but raise all other errors
                    if (self.initvm_state() != libvirt.VIR_DOMAIN_SHUTOFF and
                        self.initvm_state() != libvirt.VIR_DOMAIN_SHUTDOWN):
                        raise e
                sys.stdout.write("*")
                sys.stdout.flush()
                if self.initvm_state() == libvirt.VIR_DOMAIN_SHUTOFF:
                    print("\nInitvm shut off.")
                    break
                time.sleep(1)


@InitVMAction.register('attach')
class AttachAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node)

    def execute(self, _initvmdir, _opt, _args):
        if self.initvm_state() != libvirt.VIR_DOMAIN_RUNNING:
            print('Error: Initvm not running properly.')
            sys.exit(20)

        print('Attaching to initvm console.')
        system('virsh --connect qemu:///system console %s' % cfg['initvm_domain'])



def submit_and_dl_result(xmlfile, cdrom, opt):

    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches

    try:
        with PreprocessWrapper(xmlfile, opt) as ppw:
            xmlfile = ppw.preproc

            ret, prjdir, err = command_out_stderr(
                '%s control create_project' % (elbe_exe))
            if ret != 0:
                print("elbe control create_project failed.", file=sys.stderr)
                print(err, file=sys.stderr)
                print("Giving up", file=sys.stderr)
                sys.exit(20)

            prjdir = prjdir.strip()

            cmd = '%s control set_xml %s %s' % (elbe_exe, prjdir, xmlfile)
            ret, _, err = command_out_stderr(cmd)
            if ret != 0:
                print("elbe control set_xml failed2", file=sys.stderr)
                print(err, file=sys.stderr)
                print("Giving up", file=sys.stderr)
                sys.exit(20)
    except CommandError:
        # this is the failure from PreprocessWrapper
        # it already printed the error message from
        # elbe preprocess
        print("Giving up", file=sys.stderr)
        sys.exit(20)

    if opt.writeproject:
        with open(opt.writeproject, "w") as wpf:
            wpf.write(prjdir)

    if cdrom is not None:
        print("Uploading CDROM. This might take a while")
        try:
            system(
                '%s control set_cdrom "%s" "%s"' %
                (elbe_exe, prjdir, cdrom))
        except CommandError:
            print("elbe control set_cdrom Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        print("Upload finished")

    build_opts = ''
    if opt.build_bin:
        build_opts += '--build-bin '
    if opt.build_sources:
        build_opts += '--build-sources '
    if cdrom:
        build_opts += '--skip-pbuilder '

    try:
        system(
            '%s control build "%s" %s' %
            (elbe_exe, prjdir, build_opts))
    except CommandError:
        print("elbe control build Failed", file=sys.stderr)
        print("Giving up", file=sys.stderr)
        sys.exit(20)

    print("Build started, waiting till it finishes")

    try:
        system('%s control wait_busy "%s"' % (elbe_exe, prjdir))
    except CommandError:
        print('elbe control wait_busy Failed', file=sys.stderr)
        print('', file=sys.stderr)
        print('The project will not be deleted from the initvm.',
              file=sys.stderr)
        print('The files, that have been built, can be downloaded using:',
              file=sys.stderr)
        print('%s control get_files --output "%s" "%s"' % (elbe_exe,
                                                           opt.outdir,
                                                           prjdir),
              file=sys.stderr)
        print("", file=sys.stderr)
        print('The project can then be removed using:',
              file=sys.stderr)
        print('%s control del_project "%s"' % (elbe_exe, prjdir),
              file=sys.stderr)
        print("", file=sys.stderr)
        sys.exit(10)

    print("")
    print("Build finished !")
    print("")

    if opt.build_sdk:
        try:
            system(
                '%s control build_sdk "%s" %s' %
                (elbe_exe, prjdir, build_opts))
        except CommandError:
            print("elbe control build_sdk Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        print("SDK Build started, waiting till it finishes")

        try:
            system('%s control wait_busy "%s"' % (elbe_exe, prjdir))
        except CommandError:
            print('elbe control wait_busy Failed, while waiting for the SDK',
                  file=sys.stderr)
            print('', file=sys.stderr)
            print('The project will not be deleted from the initvm.',
                  file=sys.stderr)
            print('The files, that have been built, can be downloaded using:',
                  file=sys.stderr)
            print('%s control get_files --output "%s" "%s"' % (elbe_exe,
                                                               opt.outdir,
                                                               prjdir),
                  file=sys.stderr)
            print("", file=sys.stderr)
            print('The project can then be removed using:',
                  file=sys.stderr)
            print('%s control del_project "%s"' % (elbe_exe, prjdir),
                  file=sys.stderr)
            print("", file=sys.stderr)
            sys.exit(10)

        print("")
        print("SDK Build finished !")
        print("")

    try:
        system(
            '%s control dump_file "%s" validation.txt' %
            (elbe_exe, prjdir))
    except CommandError:
        print(
            "Project failed to generate validation.txt",
            file=sys.stderr)
        print("Getting log.txt", file=sys.stderr)
        try:
            system(
                '%s control dump_file "%s" log.txt' %
                (elbe_exe, prjdir))
        except CommandError:

            print("Failed to dump log.txt", file=sys.stderr)
            print("Giving up", file=sys.stderr)
        sys.exit(20)

    if opt.skip_download:
        print("")
        print("Listing available files:")
        print("")
        try:
            system('%s control get_files "%s"' % (elbe_exe, prjdir))
        except CommandError:
            print("elbe control get_files Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        print("")
        print(
            'Get Files with: elbe control get_file "%s" <filename>' %
            prjdir)
    else:
        print("")
        print("Getting generated Files")
        print("")

        ensure_outdir(opt)

        try:
            system('%s control get_files --output "%s" "%s"' % (
                elbe_exe, opt.outdir, prjdir))
        except CommandError:
            print("elbe control get_files Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        if not opt.keep_files:
            try:
                system('%s control del_project "%s"' % (
                    elbe_exe, prjdir))
            except CommandError:
                print("remove project from initvm failed",
                      file=sys.stderr)
                sys.exit(20)

def extract_cdrom(cdrom):
    """ Extract cdrom iso image
        returns a TmpdirFilesystem() object containing
        the source.xml, which is also validated.
    """

    tmp = TmpdirFilesystem()
    system('7z x -o%s "%s" source.xml' % (tmp.path, cdrom))

    print("", file=sys.stderr)

    if not tmp.isfile('source.xml'):
        print(
            "Iso image does not contain a source.xml file",
            file=sys.stderr)
        print(
            "This is not supported by 'elbe initvm'",
            file=sys.stderr)
        print("", file=sys.stderr)
        print("Exiting !!!", file=sys.stderr)
        sys.exit(20)

    try:
        exml = ElbeXML(
            tmp.fname('source.xml'),
            url_validation=ValidationMode.NO_CHECK)
    except ValidationError as e:
        print(
            "Iso image does contain a source.xml file.",
            file=sys.stderr)
        print(
            "But that xml does not validate correctly",
            file=sys.stderr)
        print("", file=sys.stderr)
        print("Exiting !!!", file=sys.stderr)
        print(e)
        sys.exit(20)

    print("Iso Image with valid source.xml detected !")
    print(
        "Image was generated using Elbe Version %s" %
        exml.get_elbe_version())

    return tmp


@InitVMAction.register('create')
class CreateAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node, initvmNeeded=False)

    def execute(self, initvmdir, opt, args):

        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements

        if self.initvm is not None:
            print("Initvm is already defined for the libvirt domain '%s'.\n" % cfg['initvm_domain'])
            print("If you want to build in your old initvm, "
                  "use `elbe initvm submit <xml>`.")
            print("If you want to remove your old initvm from libvirt "
                    "run `virsh --connect qemu:///system undefine %s`.\n" % cfg['initvm_domain'])
            print("You can specify another libvirt domain by setting the "
                  "ELBE_INITVM_DOMAIN environment variable to an unused domain name.\n")
            print("Note:")
            print("\t1) You can reimport your old initvm via "
                    "`virsh --connect qemu:///system define <file>`")
            print("\t   where <file> is the corresponding libvirt.xml")
            print("\t2) virsh --connect qemu:///system undefine does not delete the image "
                  "of your old initvm.")
            sys.exit(20)

        # Upgrade from older versions which used tmux
        try:
            system("tmux has-session -t ElbeInitVMSession 2>/dev/null")
            print ("ElbeInitVMSession exists in tmux. "
                   "It may belong to an old elbe version. "
                   "Please stop it to prevent interfering with this version.", file=sys.stderr)
            sys.exit(20)
        except CommandError:
            pass

        # Init cdrom to None, if we detect it, we set it
        cdrom = None

        if len(args) == 1:
            if args[0].endswith('.xml'):
                # We have an xml file, use that for elbe init
                xmlfile = args[0]
                try:
                    xml = etree(xmlfile)
                except ValidationError as e:
                    print("XML file is invalid: %s" % str(e))
                # Use default XML if no initvm was specified
                if not xml.has("initvm"):
                    xmlfile = os.path.join(
                        elbepack.__path__[0], "init/default-init.xml")

            elif args[0].endswith('.iso'):
                # We have an iso image, extract xml from there.
                tmp = extract_cdrom(args[0])

                xmlfile = tmp.fname('source.xml')
                cdrom = args[0]
            else:
                print(
                    "Unknown file ending (use either xml or iso)",
                    file=sys.stderr)
                sys.exit(20)
        else:
            # No xml File was specified, build the default elbe-init-with-ssh
            xmlfile = os.path.join(
                elbepack.__path__[0],
                "init/default-init.xml")

        try:
            init_opts = ''
            if opt.devel:
                init_opts += ' --devel'

            if opt.nesting:
                init_opts += ' --nesting'

            if not opt.build_bin:
                init_opts += ' --skip-build-bin'

            if not opt.build_sources:
                init_opts += ' --skip-build-source'

            with PreprocessWrapper(xmlfile, opt) as ppw:
                if cdrom:
                    system('%s init %s --directory "%s" --cdrom "%s" "%s"' %
                           (elbe_exe, init_opts, initvmdir, cdrom, ppw.preproc))
                else:
                    system(
                        '%s init %s --directory "%s" "%s"' %
                        (elbe_exe, init_opts, initvmdir, ppw.preproc))

        except CommandError:
            print("'elbe init' Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        # Read xml file for libvirt
        with open(os.path.join(initvmdir, 'libvirt.xml')) as f:
            xml = f.read()

        # Register initvm in libvirt
        try:
            self.conn.defineXML(xml)
        except CommandError:
            print('Registering initvm in libvirt failed', file=sys.stderr)
            print('Try `virsh --connect qemu:///system undefine %s` to delete existing initvm' % cfg['initvm_domain'],
                  file=sys.stderr)
            sys.exit(20)

        # Build initvm
        try:
            system('cd "%s"; make' % (initvmdir))
        except CommandError:
            print("Building the initvm Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        try:
            system('%s initvm start' % elbe_exe)
        except CommandError:
            print("Starting the initvm Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        if len(args) == 1:
            # if provided xml file has no initvm section xmlfile is set to a
            # default initvm XML file. But we need the original file here
            if args[0].endswith('.xml'):
                # stop here if no project node was specified
                try:
                    x = etree(args[0])
                except ValidationError as e:
                    print("XML file is invalid: %s" % str(e))
                    sys.exit(20)
                if not x.has('project'):
                    print("elbe initvm ready: use 'elbe initvm submit "
                          "myproject.xml' to build a project")
                    sys.exit(0)

                xmlfile = args[0]
            elif cdrom is not None:
                xmlfile = tmp.fname('source.xml')

            submit_and_dl_result(xmlfile, cdrom, opt)


@InitVMAction.register('submit')
class SubmitAction(InitVMAction):

    def __init__(self, node):
        InitVMAction.__init__(self, node)

    def execute(self, _initvmdir, opt, args):
        try:
            system('%s initvm ensure' % elbe_exe)
        except CommandError:
            print("Starting the initvm Failed", file=sys.stderr)
            print("Giving up", file=sys.stderr)
            sys.exit(20)

        # Init cdrom to None, if we detect it, we set it
        cdrom = None

        if len(args) == 1:
            if args[0].endswith('.xml'):
                # We have an xml file, use that for elbe init
                xmlfile = args[0]
            elif args[0].endswith('.iso'):
                # We have an iso image, extract xml from there.
                tmp = extract_cdrom(args[0])

                xmlfile = tmp.fname('source.xml')
                cdrom = args[0]
            else:
                print(
                    "Unknown file ending (use either xml or iso)",
                    file=sys.stderr)
                sys.exit(20)

            submit_and_dl_result(xmlfile, cdrom, opt)

@InitVMAction.register('sync')
class SyncAction(InitVMAction):

    def __init__(self, node):
        super(SyncAction, self).__init__(node)

    def execute(self, _initvmdir, opt, args):
        top_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        try:
            system("rsync --info=name1,stats1  --archive --times "
                   "--exclude='.git*' --exclude='*.pyc' --exclude='elbe-build*' "
                   "--exclude='initvm' --exclude='__pycache__' --exclude='docs' "
                   "--exclude='examples' "
                   "--rsh='ssh -p %s' --chown=root:root "
                   "%s/ root@localhost:/var/cache/elbe/devel" %
                   (cfg["sshport"], top_dir))
        except CommandError as E:
            print(E)
