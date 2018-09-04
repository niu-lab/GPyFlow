from multiprocessing import Process
from threading import Lock
import logging
from subprocess import Popen, PIPE, STDOUT
from .errors import RunCmdException
from .log import getlogger
from flow import DEBUG

# log_locker = Lock()
# logger = getlogger(__name__, 'flow.log')
# logger.setLevel(logging.INFO)


def run_cmd(cmdline):
    # log_locker.acquire()
    # logger.info("CMD:{}".format(cmdline))
    # log_locker.release()
    return_code = 0
    outs_str = ""
    errs_str = ""
    if not DEBUG:
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
