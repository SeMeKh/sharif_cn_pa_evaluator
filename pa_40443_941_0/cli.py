import os
import click
import traceback
import random
from time import sleep
import sarge
from tqdm import tqdm

from framework.grader import config, scores
from pa_40443_941_0.tests.basics import basic_print, join
from pa_40443_941_0.tests.completeness import mixed_scenario
from pa_40443_941_0.tests.conformance import type1x, type2x_30
from pa_40443_941_0.tests.leave import explicit_exit, change_parent
from pa_40443_941_0.tests.messaging import sendmsg, broadcast
from pa_40443_941_0.tests.tricky import self_message, setparent_cycle, sudden_leave, msg_to_nowhere
from pa_40443_941_0.tests.violation import m20_from_parent, m21_from_child, m30_from_child, invalid_message
from pa_40443_941_0.utils import IrcNodePool


@click.group()
def pa_40443_941_0():
    pass


@pa_40443_941_0.command()
@click.argument('compiled_codes', type=click.File('r'))
@click.option('--model_bin', prompt="Path to model's binary", type=click.Path(exists=True))
def run_all(compiled_codes, model_bin):
    prg = tqdm(compiled_codes.readlines())
    base = os.path.dirname(compiled_codes.name)
    for line in prg:
        line = line.strip()
        prg.set_description(line)
        student_bin = '%s/%s/sdp.out' % (base, line)
        proc = sarge.capture_stdout(
            './run.py pa_40443_941_0 run --student_bin %s --model_bin %s' % (student_bin, model_bin))
        print line, proc.stdout.text.split('\n')[0]
        sleep(1)


@pa_40443_941_0.command()
@click.option('--student_bin', prompt="Path to student's binary", type=click.Path(exists=True))
@click.option('--model_bin', type=click.Path(exists=True))
def run(student_bin, model_bin):
    config['student_bin'] = student_bin
    if model_bin is not None:
        config['model_bin'] = model_bin
    tests = [
                basic_print,
                join,
            ] + [
                explicit_exit,
                change_parent,
            ] + [
                sendmsg,
                broadcast,
            ] + [
                self_message,
                setparent_cycle,
                sudden_leave,
                msg_to_nowhere,
            ] + [
                type1x,
                type2x_30,
            ] + [
                m20_from_parent,
                m21_from_child,
                m30_from_child,
                invalid_message,
            ] + [
                mixed_scenario,
            ]
    for test in tests:
        random.seed(777)
        nodes = IrcNodePool()
        try:
            test(nodes)
        except:
            traceback.print_exc()
        finally:
            nodes.teardown()
    print sum(scores.values())
    print scores
