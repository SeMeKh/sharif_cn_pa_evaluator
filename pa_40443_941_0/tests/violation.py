from framework.grader import grade
from framework.test import test
from ..test_utils import build_tree, gen_token
from .conformance import type1x, type2x_30


@test(requires=[type1x, type2x_30])
def m20_from_parent(nodes):
    nodes.extend(build_tree({1: {2: {}}}, {1: {'bin': 'model'}}))
    nodes[1].run_command('sendcustom 20 2 %s' % gen_token())
    grade(2, nodes.verify_output({2: []}))
    grade(2, nodes.verify_structure({2: [-1, {}]}))


@test(requires=[type1x, type2x_30])
def m21_from_child(nodes):
    nodes.extend(build_tree({1: {2: {}}}, {2: {'bin': 'model'}}))
    nodes[2].run_command('sendcustom 21 1 %s' % gen_token())
    grade(2, nodes.verify_output({1: []}))
    grade(2, nodes.verify_structure({1: [-1, {}]}))


@test(requires=[type1x, type2x_30])
def m30_from_child(nodes):
    nodes.extend(build_tree({1: {2: {}}}, {2: {'bin': 'model'}}))
    nodes[2].run_command('sendcustom 30 1 %s' % gen_token())
    grade(2, nodes.verify_output({1: []}))
    grade(2, nodes.verify_structure({1: [-1, {}]}))


@test(requires=[type1x])
def invalid_message(nodes):
    nodes.extend(build_tree({1: {2: {}}}, {2: {'bin': 'model'}}))
    nodes[2].run_command('sendcustom 50 1 %s' % gen_token())
    grade(3, nodes.verify_structure({1: [-1, {}]}))
