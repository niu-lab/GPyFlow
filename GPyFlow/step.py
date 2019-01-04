import os
from GPyFlow.proc import cmdworker


class Step(object):
    def __init__(self, workflow, name):
        self.name = name
        self.workflow = workflow
        self.pres = list()
        self.olddir = ""
        self.workdir = ""
        self.command = ""
        self.finished = False
        self.error = None
        self.worker = None

    def load_from_dict(self, content):
        self.pres = content.get("pres") if content.get("pres") else list()
        self.workdir = content.get("workdir") if content.get("workdir") else ""
        self.command = content.get("cmd") if content.get("cmd") else ""

    def run(self):
        if len(self.workdir) > 0:
            if os.path.exists(self.workdir):
                self.olddir = os.path.abspath(os.path.curdir)
                os.chdir(self.workdir)
            else:
                raise Exception("{} not exist".format(self.workdir))
        # 生成运行命令
        self.worker = cmdworker(self.command, self.workflow.out_writer, self.workflow.err_writer)
        self.worker.start()
        if self.olddir:
            os.chdir(self.olddir)

    def join(self):
        self.worker.join()
        self.finished = True
        if self.worker.exitcode != 0:
            self.error = True
        else:
            self.error = False
