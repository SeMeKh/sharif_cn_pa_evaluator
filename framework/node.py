import re
import uuid
import sarge
from time import sleep
from xml.dom.minidom import parse

FULL_TRACK = 'full_track'


class Node(object):
    def __init__(self, **kwargs):
        self.uuid = uuid.uuid4()
        self.proc = None
        self.feeder = sarge.Feeder()
        self.cmd = '/bin/false'
        self.full_track = kwargs.get(FULL_TRACK, False)

    def run(self):
        if self.full_track:
            self.cmd = ' '.join([
                'valgrind',
                '--trace-children=yes',
                '--tool=memcheck', '--leak-check=full',
                '--track-fds=yes',
                '--xml=yes --xml-file=%s' % self.valgrind_xml_path,
                # '--log-file=%s' % self.valgrind_log_path,
                '%s' % self.cmd,
            ])
        self.cmd = 'stdbuf -oL -eL %s' % self.cmd

        self.proc = sarge.run(
            self.cmd,
            input=self.feeder,
            stdout=sarge.Capture(),
            stderr=sarge.Capture(),
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
        return './tmp/valgrind_%s.xml' % self.uuid

    @property
    def valgrind_log_path(self):
        return './tmp/valgrind_%s.log' % self.uuid

    def open_sockets(self):
        log = self.proc.stderr.text
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
