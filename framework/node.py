import re
import uuid
from os import makedirs

import sarge
from time import sleep
from xml.dom.minidom import parse
from framework.grader import config, current_test

FULL_TRACK = 'full_track'


class Node(object):
    def __init__(self, **kwargs):
        self.uuid = uuid.uuid4()
        self.proc = None
        self.feeder = sarge.Feeder()
        self.cmd = '/bin/false'
        self.full_track = kwargs.get(FULL_TRACK, False)

    @property
    def base_log_path(self):
        return '%s/%s/%s/' % (config['log_path'], current_test(), self.uuid)

    def run(self):
        makedirs(self.base_log_path)
        if self.full_track:
            self.cmd = ' '.join([
                'valgrind',
                '--trace-children=yes',
                '--tool=memcheck', '--leak-check=full',
                '--track-fds=yes',
                '--xml=yes --xml-file=%s' % self.valgrind_xml_path,
                '--log-file=%s' % self.valgrind_log_path,
                '%s' % self.cmd,
            ])
        self.cmd = 'stdbuf -oL -eL %s' % self.cmd
        with open('%s/cmd' % self.base_log_path, 'w') as cmd_file:
            print >> cmd_file, self.cmd
        self.cmd = '%s 2>%s/stderr | tee %s/stdout' % (self.cmd, self.base_log_path, self.base_log_path)
        self.proc = sarge.run(
            self.cmd,
            input=self.feeder,
            stdout=sarge.Capture(),
            async=True,
        )

    def kill(self):
        p = self.proc.commands[0].process
        if p is not None:
            p.kill()

    def write_stdin(self, data):
        self.feeder.feed(data)

    def capture_stdout(self, duration):
        sleep(duration)
        out = self.proc.stdout.read(block=False)
        return out

    def ignore_stdout(self):
        self.capture_stdout(0)

    @property
    def valgrind_xml_path(self):
        return '%s/valgrind.xml' % self.base_log_path

    @property
    def valgrind_log_path(self):
        return '%s/valgrind.log' % self.base_log_path

    def open_sockets(self):
        with open(self.valgrind_log_path, 'r') as log_file:
            log = log_file.read()
        open_fds = log[log.rfind('FILE DESCRIPTORS: '):]
        return re.findall(r'Open AF_INET socket[^\n]*', open_fds)

    def memleak_amount(self):
        doc = parse(self.valgrind_xml_path)

        sum = 0
        for error in doc.getElementsByTagName('error'):
            kind = error.getElementsByTagName('kind')[0]
            if kind.firstChild.nodeValue == 'Leak_DefinitelyLost':
                leakedbytes = int(error \
                                  .getElementsByTagName('xwhat')[0] \
                                  .getElementsByTagName('leakedbytes')[0] \
                                  .firstChild.nodeValue)
                sum += leakedbytes
        return sum


class NodePool(object):
    def __init__(self):
        self.nodes = []

    def teardown(self):
        for node in self.nodes:
            try:
                node.kill()
            except:
                pass

    def extend(self, nodes):
        self.nodes.extend(nodes)
