import argparse
from flow.workflow import run_target
from flow.filetools import package

args = dict()


def handle_commadline():
    global args
    parser = argparse.ArgumentParser(prog="pyflow")
    subparsers = parser.add_subparsers(dest='sub-command')
    subparsers.required = True
    run_parser = subparsers.add_parser("run")
    tar_parser = subparsers.add_parser("tar")

    run_parser.add_argument("-i", "--input",
                            type=str,
                            required=True,
                            help="input lines"
                            )
    run_parser.add_argument("-o", "--output",
                            type=str,
                            required=True,
                            help="output directory"
                            )
    run_parser.add_argument("workflow",
                            help="workflow directory or workflow.json")

    tar_parser.add_argument("workflow_dir",
                            help="workflow directory")

    args = vars(parser.parse_args())


def tar(workflow_dir):
    package(workflow_dir)


def run(inputs, out_dir, workflow):
    run_target(workflow, inputs, out_dir)


def main():
    handle_commadline()
    if args.get("subparser") == "run":
        run(args.get("input"),
            args.get("output"),
            args.get('workflow'))
    if args.get("subparser") == "tar":
        tar(args.get("workflow_dir"))


if __name__ == '__main__':
    main()
