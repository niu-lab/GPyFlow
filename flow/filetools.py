import os
import shutil


def dir_create(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def package(dir_path):
    outfilename = "{}".format(dir_path)
    shutil.make_archive(outfilename, 'zip', dir_path)


def get_file_firstname(filename):
    filename = os.path.basename(filename)
    if isinstance(filename, str) and len(filename) > 0:
        splits = filename.split('.')
        return splits[0]
    raise Exception("can't get {filename} fisrtname.".format(filename=filename))
