from framework.grader import grade
from framework.test import test
from pa_40443_941_0.test_utils import build_tree


@test()
def basic_print(nodes):
    nodes.extend(build_tree({1: {}}))
    grade(2, nodes.verify_structure({1: [-1, {}]}))


@test(requires=basic_print)
def join(nodes):
    nodes.extend(build_tree({i: {} for i in range(1, 8)}))
    nodes[2].setparent_node(nodes[1])
    grade(
        3,
        nodes.verify_structure({
            1: [-1, {2: []}],
            2: [1, {}],
        })
    )

    nodes[3].setparent_node(nodes[2])
    nodes[4].setparent_node(nodes[2])
    grade(
        5,
        nodes.verify_structure({
            1: [-1, {2: [3, 4]}],
            2: [1, {3: [], 4: []}],
            3: [2, {}],
            4: [2, {}],
        })
    )

    nodes[6].setparent_node(nodes[5])
    nodes[7].setparent_node(nodes[5])
    nodes[5].setparent_node(nodes[1])
    grade(
        5,
        nodes.verify_structure({
            1: [-1, {2: [3, 4], 5: [6, 7]}],
        })
    )
