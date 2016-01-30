import re
from time import sleep
from framework.node import NodePool


def match_helper(regex, line):
    line = ''.join(line.split())
    match = re.search(regex, line)
    return match.groups()


class PrintOutput(object):
    def __init__(self, lines):
        self.parent = int(match_helper(r'Parent:(-?\d+)', lines[0])[0])
        self.children = {}
        for line in lines[1:]:
            id, tree = match_helper(r'C\((\d+)\):(.*)', line)
            id = int(id)
            self.children[id] = sorted([int(x) for x in tree.split(',')])
            if id in self.children[id]:
                self.children[id].remove(id)

    def __repr__(self):
        return [self.parent, self.children]

    def __str__(self):
        return str(self.__repr__())

    def __eq__(self, other):
        return str(self) == str(other)


class IrcNodePool(NodePool):
    def verify_structure(self, tree):
        ok = True
        for node_id, structure in tree.iteritems():
            print_out = self[node_id].do_print()
            ok &= (print_out == structure)
        return ok

    def verify_output(self, exp):
        ok = True
        for node_id, expected_output in exp.iteritems():
            captured_lines = self[node_id].capture_lines()
            ok &= (captured_lines == expected_output)
        return ok

    def verify_no_open_sockets(self):
        for node in self.nodes:
            if len(node.open_sockets()) > 0:
                return False
        return True

    def verify_clean_exit(self):
        sleep(1)
        for node in self.nodes:
            node.proc.commands[0].poll()
            if node.proc.commands[0].returncode != 0:
                return False
        return True

    def verify_no_memory_leak(self):
        for node in self.nodes:
            if node.memleak_amount() > 0:
                return False
        return True

    def ids(self):
        return [node.id for node in self.nodes]

    def __getitem__(self, index):
        for node in self.nodes:
            if node.id == index:
                return node
        raise KeyError
