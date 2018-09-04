import os
import json
from .proc import cmdworker


class Step(object):
    def __init__(self, workflow, name):
        self.name = name
        self.workflow = workflow
        self.pres = None
        self.input = None
        self.output = None
        self.olddir = ""
        self.workdir = ""
        self.command = None
        self.runcmd = ""
        self.finished = False
        self.error = None
        self.worker = None

    def load_from_dict(self, content):
        self.pres = content.get("pres") if content.get("pres") else list()
        self.input = content.get("input") if content.get("input") else list()
        self.output = content.get("output") if content.get("output") else list()
        self.workdir = content.get("workdir") if content.get("workdir") else ""
        self.command = content.get("command") if content.get("command") else ""

    def __replace(self):
        self.command = json.dumps(self.command)

        # input replace
        for index, value in enumerate(self.input):
            repalce_str = "#IN[{}]#".format(index)
            self.command = self.command.replace(repalce_str, value)
        # output replace
        for index, value in enumerate(self.output):
            repalce_str = "#OUT[{}]#".format(index)
            self.command = self.command.replace(repalce_str, value)

        self.command = json.loads(self.command)

    def __generate(self):
        self.__replace()
        path = self.command.get("path")
        params = self.command.get("parameters")

        def f(parameter):
            return parameter.get("prefix") \
                   + parameter.get("key") \
                   + parameter.get("sep") \
                   + parameter.get("value")

        flags = " ".join(list(map(f, params)))
        cmd = "{path} {flags}".format(path=path, flags=flags)
        return cmd

    def run(self):
        if len(self.workdir) > 0:
            if os.path.exists(self.workdir):
                self.olddir = os.path.abspath(os.path.curdir)
                os.chdir(self.workdir)
            else:
                raise Exception("{} not exist".format(self.workdir))
        # 生成运行命令
        self.runcmd = self.__generate()
        self.worker = cmdworker(self.runcmd)
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
