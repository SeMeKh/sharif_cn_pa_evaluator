from framework.grader import grade
from framework.test import test
from ..test_utils import build_tree, binary_tree, gen_token
from .messaging import simple_sendmsg


@test(requires=simple_sendmsg)
def propagate(nodes):
    nodes.extend(build_tree(binary_tree(7)))

    m1 = gen_token()
    nodes[3].sendmsg(2, m1)
    grade(
        5,
        nodes.verify_output({
            1: [],
            2: [m1],
            3: [],
            4: [m1],
            5: [m1],
            6: [],
            7: []
        })
    )

    m2 = gen_token()
    nodes[3].sendmsg(1, m2)
    grade(
        5,
        nodes.verify_output({
            1: [m2],
            2: [m2],
            3: [m2],
            4: [m2],
            5: [m2],
            6: [m2],
            7: [m2],
        })
    )