from framework.grader import grade
from framework.test import test
from .basics import join
from ..test_utils import build_tree, binary_tree, gen_token


@test(requires=join)
def simple_sendmsg(nodes):
    nodes.extend(build_tree(binary_tree(7)))
    m1 = gen_token()

    nodes[1].sendmsg(4, m1)
    grade(
        5,
        nodes.verify_output({
            4: [m1],
        })
    )

    m2 = gen_token()
    nodes[7].sendmsg(5, m2)
    grade(
        5,
        nodes.verify_output({
            5: [m2],
        })
    )
