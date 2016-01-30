from time import sleep
from framework.grader import grade
from framework.test import test
from ..test_utils import build_tree, binary_tree, gen_token
from .messaging import sendmsg


@test(requires=sendmsg)
def msg_to_nowhere(nodes):
    nodes.extend(build_tree(binary_tree(7)))
    nodes[3].sendmsg(8, gen_token())
    grade(
        2,
        nodes.verify_output({i: [] for i in nodes.ids()}) and \
        nodes.verify_structure({
            1: [-1, {2: [4, 5], 3: [6, 7]}],
        })
    )


@test()
def sudden_leave(nodes):
    nodes.extend(build_tree({1: {2: {3: {}}}}))
    nodes[2].kill()
    sleep(0.5)
    grade(
        2,
        nodes.verify_structure({
            1: [-1, {}],
            3: [-1, {}],
        })
    )


@test()
def setparent_cycle(nodes):
    nodes.extend(build_tree({1: {2: {3: {}}}}))
    nodes[1].setparent_node(nodes[3])
    grade(
        2,
        nodes.verify_structure({
            1: [-1, {2: [3]}],
            2: [1, {3: []}],
            3: [2, {}],
        })
    )


@test()
def self_message(nodes):
    nodes.extend(build_tree({1: {2: {3: {}, 4: {}}}}))
    m = gen_token()
    nodes[1].sendmsg(1, m)
    grade(
        2,
        nodes.verify_output({
            1: [m],
        })
    )
    grade(
        2,
        nodes.verify_output({
            2: [m],
            3: [m],
            4: [m],
        })
    )
