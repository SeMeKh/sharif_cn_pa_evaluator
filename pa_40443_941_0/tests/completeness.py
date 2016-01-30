import random
from functools import partial

from framework.grader import grade
from framework.node import FULL_TRACK
from framework.test import test
from ..test_utils import build_tree, binary_tree, gen_token
from .tricky import msg_to_nowhere
from .leave import change_parent, explicit_exit
from .messaging import simple_sendmsg


@test(requires=[simple_sendmsg, change_parent, explicit_exit, msg_to_nowhere])
def mixed_scenario(nodes):
    node_count = 3
    nodes.extend(build_tree(
        binary_tree(node_count),
        opts={i: {FULL_TRACK: True} for i in range(1, node_count + 1)},
    ))

    cmds = [nodes[i].exit for i in range(1, node_count + 1)]
    for _ in range(node_count):
        fr, to = random.randint(1, node_count), random.randint(1, node_count)
        cmds.append(partial(nodes[fr].setparent_node, nodes[to]))
    for _ in range(10 * node_count):
        fr, to, m = random.randint(1, node_count), random.randint(1, node_count), gen_token()
        cmds.append(partial(nodes[fr].sendmsg, to, m))
    random.shuffle(cmds)
    for cmd in cmds:
        cmd()

    if nodes.verify_clean_exit():
        grade(4, True)
        grade(8, nodes.verify_no_memory_leak())
        grade(8, nodes.verify_no_open_sockets())
