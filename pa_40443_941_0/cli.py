import os
import click
import traceback
import random
from time import sleep

import psutil
import sarge
import shutil
from tqdm import tqdm
from framework.grader import config, scores
from pa_40443_941_0.tests import all
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
        sarge.run(
            './run.py pa_40443_941_0 run --student_bin %s --model_bin %s --log_path logs/%s' % (
                student_bin, model_bin, line)
        )
        sleep(1)


@pa_40443_941_0.command()
@click.option('--student_bin', prompt="Path to student's binary", type=click.Path(exists=True))
@click.option('--model_bin', type=click.Path(exists=True))
@click.option('--log_path', type=click.Path(file_okay=False, writable=True), default='logs')
def run(student_bin, model_bin, log_path):
    config['student_bin'] = student_bin
    if model_bin is not None:
        config['model_bin'] = model_bin
    config['log_path'] = log_path
    shutil.rmtree(log_path, ignore_errors=True)
    os.makedirs(log_path)

    with open('%s/result' % log_path, 'w') as result:
        try:
            for test in all:
                sleep(1)
                for p in psutil.process_iter():
                    cmd = ' '.join(p.cmdline())
                    if 'sdp.out' in cmd and 'python' not in cmd:
                        click.secho("Existing instances of `sdp` app detected. `killall -9 sdp.out` maybe?\n%s" % cmd,
                                    fg='red')
                        print >> result, 'FATAL ERROR'
                        exit(1)
                random.seed(777)
                nodes = IrcNodePool()
                try:
                    test(nodes)
                except:
                    traceback.print_exc()
                finally:
                    nodes.teardown()
        finally:
            total = sum(scores.values())
            click.secho(str(scores), fg='yellow', bold=True)
            print >> result, total
