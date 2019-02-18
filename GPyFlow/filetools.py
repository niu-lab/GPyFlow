import os
import shutil
import json


def dir_create(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def package(workflow_dir):
    if not os.path.isabs(workflow_dir):
        workflow_dir = os.path.join(os.curdir, workflow_dir)
        workflow_dir = os.path.abspath(workflow_dir)
    basename = os.path.basename(workflow_dir)
    shutil.make_archive(basename, 'zip', workflow_dir)


def get_file_firstname(filename):
    filename = os.path.basename(filename)
    if isinstance(filename, str) and len(filename) > 0:
        splits = filename.split('.')
        return splits[0]
    raise Exception("can't get {filename} fisrtname.".format(filename=filename))


def extract_macros(_workflow_file, _macros_file):
    with open(_workflow_file, 'r') as workflow_file:
        workflow_dict = json.load(workflow_file)
        macros = workflow_dict.get("macros")
        with open(_macros_file, "w+") as macro_file:
            for macro in macros:
                line = "{}=".format(macro) + os.linesep
                macro_file.write(line)
