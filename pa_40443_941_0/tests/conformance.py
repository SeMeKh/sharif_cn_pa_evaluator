from framework.grader import grade
from framework.test import test
from pa_40443_941_0.test_utils import build_tree, gen_token
from pa_40443_941_0.tests.basics import join
from pa_40443_941_0.tests.leave import explicit_exit
from pa_40443_941_0.tests.messaging import sendmsg, broadcast


@test(requires=[join, explicit_exit])
def type1x(nodes):
    nodes.extend(build_tree({1: {}, 2: {}}, {1: {'bin': 'model'}}))
    nodes[2].setparent_node(nodes[1])
    grade(
        2,
        nodes.verify_structure({
            1: [-1, {2: []}],
        })
    )

    nodes[2].exit()
    grade(
        2,
        nodes.verify_structure({
            1: [-1, {}],
        })
    )


@test(requires=[type1x, sendmsg, broadcast])
def type2x_30(nodes):
    nodes.extend(build_tree({1: {2: {3: {}}}}, {2: {'bin': 'model'}}))

    m1 = gen_token()
    nodes[1].sendmsg(3, m1)
    grade(
        2,
        nodes.verify_output({
            1: [],
            2: [],
            3: [m1],
        })
    )

    m2 = gen_token()
    nodes[3].sendmsg(1, m2)
    grade(
        2,
        nodes.verify_output({
            1: [m2],
        })
    )
    grade(
        2,
        nodes.verify_output({
            2: [m2],
            3: [m2],
        })
    )
