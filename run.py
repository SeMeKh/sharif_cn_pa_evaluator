#!/usr/bin/env python2

import click
from pa_40443_941_0.cli import pa_40443_941_0


@click.group()
def cli():
    pass


cli.add_command(pa_40443_941_0)

if __name__ == '__main__':
    cli()
