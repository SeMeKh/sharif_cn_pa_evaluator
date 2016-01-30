from time import sleep

from framework.grader import config
from framework.node import Node
from pa_40443_941_0.utils import PrintOutput

SUFFICIENT_TIME = 0.01


class IrcNode(Node):
    def __init__(self, id, **kwargs):
        super(IrcNode, self).__init__(**kwargs)
        self.id = id
        self.address = kwargs.get('address', '127.0.0.1')
        bin = kwargs.get('bin', 'student')
        if bin == 'model':
            bin = config.get('model_bin', config['student_bin'])
        else:
            bin = config['student_bin']
        self.cmd = '%s %s' % (bin, id)

    def capture_lines(self, duration=0.01):
        out = self.capture_stdout(duration)
        if out == '':
            out = []
        else:
            out = out.strip('\n').split('\n')
        return out

    def run_command(self, cmd):
        self.write_stdin(cmd + '\n')
        sleep(SUFFICIENT_TIME)

    def setparent(self, name, id):
        self.run_command('setparent %s %s' % (name, id))

    def setparent_node(self, irc_node):
        self.setparent(irc_node.address, irc_node.id)

    def sendmsg(self, dst, msg):
        self.run_command('sendmessage %s %s' % (dst, msg))

    def exit(self):
        self.run_command('exit')

    def do_print(self):
        self.ignore_stdout()
        self.run_command('print')
        out = self.capture_lines(SUFFICIENT_TIME)
        try:
            ret = PrintOutput(out)
        except:
            ret = None
        return ret
