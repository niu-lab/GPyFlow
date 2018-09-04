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
@click.option('--macros', '-m', help="defined macros")
@click.option('--exclude', '-x', help="exclude steps")
@click.option('--output_dir', '-o', required=True, help="output dir")
@click.argument('flow')
def run(macros, exclude, output_dir, flow):
    """run workflow"""
    run_target(flow, output_dir, macros, exclude)


cli.add_command(tar)
cli.add_command(run)


def main():
    cli()


if __name__ == '__main__':
    main()
