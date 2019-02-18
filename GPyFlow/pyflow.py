import argparse
from GPyFlow.workflow import run_target
from GPyFlow.filetools import package, extract_macros

args = dict()


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def handle_commandline():
    global args
    parser = argparse.ArgumentParser(prog="pyflow")
    subparsers = parser.add_subparsers(dest='sub-command')
    subparsers.required = True
    run_parser = subparsers.add_parser("run")
    tar_parser = subparsers.add_parser("tar")
    extract_parser = subparsers.add_parser("extract")

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

    run_parser.add_argument("--preview",
                            default=False,
                            type=str2bool,
                            required=False,
                            help="preview to run commands"
                            )

    run_parser.add_argument("workflow",
                            help="workflow directory or workflow.json")

    tar_parser.add_argument("workflow_dir",
                            help="workflow directory")

    extract_parser.add_argument("-f", "--workflow",
                                type=str,
                                required=True,
                                help="workflow file")
    extract_parser.add_argument("macros",
                                help="extract macros")

    args = vars(parser.parse_args())


def tar(workflow_dir):
    package(workflow_dir)


def run(preview, inputs, out_dir, workflow):
    run_target(preview, workflow, inputs, out_dir)


def extract(workflow_file, macro_file):
    extract_macros(workflow_file, macro_file)


def main():
    handle_commandline()
    if args.get("sub-command") == "run":
        run(args.get("preview"),
            args.get("input"),
            args.get("output"),
            args.get('workflow'))
    if args.get("sub-command") == "tar":
        tar(args.get("workflow_dir"))

    if args.get("sub-command") == "extract":
        extract(args.get("workflow"),
                args.get("macros"))


if __name__ == '__main__':
    main()
