from framework.grader import grade
from framework.test import test
from ..test_utils import build_tree, binary_tree
from .basics import join


@test(requires=join)
def explicit_exit(nodes):
    nodes.extend(build_tree(binary_tree(7)))
    nodes[7].exit()
    grade(
        4,
        nodes.verify_structure({
            1: [-1, {2: [4, 5], 3: [6]}],
            3: [1, {6: []}],
        })
    )

    nodes[3].exit()
    grade(
        3,
        nodes.verify_structure({
            6: [-1, {}],  # expect 6 to reset its parent
            1: [-1, {2: [4, 5]}],
        })
    )


@test(requires=join)
def change_parent(nodes):
    nodes.extend(build_tree({
        1: {
            2: {
                3: {},
                4: {},
            },
        },
        5: {},
    }))
    nodes[3].setparent_node(nodes[5])
    nodes[2].setparent_node(nodes[3])
    grade(
        3,
        nodes.verify_structure({
            1: [-1, {}],
            2: [3, {4: []}],
            3: [5, {2: [4]}],
            4: [2, {}],
            5: [-1, {3: [2, 4]}],
        })
    )
