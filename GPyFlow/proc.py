from multiprocessing import Process, Lock
from subprocess import Popen, PIPE
from GPyFlow.errors import RunCmdException
import os


class Writer(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            file = open(filename, "w+")
            file.close()
        self._filename = filename
        self._lock = Lock()

    def write(self, s):
        self._lock.acquire()
        with open(self._filename, "a") as write_file:
            write_file.write(s)
            write_file.flush()
        self._lock.release()


def run_cmd(cmdline, out_writer, err_writer):
    with Popen("bash", stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        outs, errs = proc.communicate(cmdline.encode('utf-8'))
        return_code = proc.returncode
        if outs:
            outs_str = outs.decode('utf-8')
            out_writer.write(outs_str)
        if errs:
            errs_str = errs.decode('utf-8')
            err_writer.write(errs_str)

        if proc.returncode != 0:
            raise RunCmdException(cmdline)
    return return_code


def worker(func, *args, **kwargs):
    proc = Process(target=func, args=args, kwargs=kwargs)
    return proc


def cmdworker(cmdline, out_writer, err_writer):
    return worker(func=run_cmd, cmdline=cmdline, out_writer=out_writer, err_writer=err_writer)
