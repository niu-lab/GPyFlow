#! /usr/bin/env python3

import click
from flow.filetools import package
from flow.workflow import run_target


@click.group()
def cli():
    pass


@click.command()
@click.argument('dirpath')
def tar(dirpath):
    """tar workflow directory to zip file"""
    package(dirpath)


@click.command()
@click.option('--inputs', '-i', help="defined macros")
@click.option('--output_dir', '-o', required=True, help="output dir")
@click.argument('workflow')
def run(inputs, output_dir, workflow):
    """run workflow"""
    run_target(workflow, inputs, output_dir)


cli.add_command(tar)
cli.add_command(run)


def main():
    cli()


if __name__ == '__main__':
    main()
