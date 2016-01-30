from time import sleep
import random

from pa_40443_941_0.node import IrcNode


def gen_token():
    return 'msg%d' % random.randint(1, 100)


def build_tree(tree, opts=None, parent=None):
    if opts is None:
        opts = {}
    out = []

    for key, value in tree.iteritems():
        node = IrcNode(key, **opts.get(key, {}))
        node.run()
        sleep(0.5)
        if parent is not None:
            node.setparent_node(parent)
        out.append(node)
        out.extend(build_tree(value, opts, node))

    return out


def binary_tree(size):
    d = {0: {}}
    for i in range(1, size + 1):
        d[i] = {}
        d[i / 2][i] = d[i]
    return d[0]
