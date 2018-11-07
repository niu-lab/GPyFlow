from multiprocessing import Process
from subprocess import Popen, PIPE, STDOUT
from GPyFlow.errors import RunCmdException


def run_cmd(cmdline):
    outs_str = ""
    errs_str = ""
    with Popen("bash", stdin=PIPE, stdout=PIPE, stderr=STDOUT) as proc:
        outs, errs = proc.communicate(cmdline.encode('utf-8'))
        return_code = proc.returncode
        if proc.returncode != 0:
            if outs:
                outs_str = outs.decode('utf-8')
            if errs:
                errs_str = errs.decode('utf-8')
            raise RunCmdException(cmdline, outs_str, errs_str)
    return return_code, outs_str, errs_str


def worker(func, *args, **kwargs):
    proc = Process(target=func, args=args, kwargs=kwargs)
    return proc


def cmdworker(cmdline):
    return worker(func=run_cmd, cmdline=cmdline)
