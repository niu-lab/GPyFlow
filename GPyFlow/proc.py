from multiprocessing import Process, Lock
from subprocess import Popen, PIPE, STDOUT
from GPyFlow.errors import RunCmdException
from GPyFlow.log import getlogger


class OutWriter(object):
    def __init__(self, filename):
        self.logger = getlogger("out", file=filename)
        self._lock = Lock()

    def write(self, s):
        self._lock.acquire()
        self.logger.info(s)
        self._lock.release()


def run_cmd(cmdline, writer):
    with Popen("bash", stdin=PIPE, stdout=PIPE, stderr=STDOUT) as proc:
        outs, errs = proc.communicate(cmdline.encode('utf-8'))
        return_code = proc.returncode
        if outs:
            outs_str = outs.decode('utf-8')
            writer.write(outs_str)
        if errs:
            errs_str = errs.decode('utf-8')
            writer.write(errs_str)

        if proc.returncode != 0:
            raise RunCmdException(cmdline)
    return return_code


def worker(func, *args, **kwargs):
    proc = Process(target=func, args=args, kwargs=kwargs)
    return proc


def cmdworker(cmdline, out_writer):
    return worker(func=run_cmd, cmdline=cmdline, writer=out_writer)
