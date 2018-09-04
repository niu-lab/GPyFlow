# coding: utf-8

import re
import json
import os
from zipfile import ZipFile
from .errors import MacroError
from .step import Step
from .filetools import dir_create
from .log import getlogger


class WorkFlow(object):
    def __init__(self):
        self.dicts = dict()
        self.status_file = None
        self.macros = dict()
        self.workflow = dict()
        self.console_logger = getlogger(__name__)
        self.file_logger = getlogger("cmd", "cmd.log")
        self.steps = list()
        self.to_runs = list()
        self.finished = False
        self.waits = list()
        pass

    def load_from_file(self, filepath):
        with open(filepath, 'r') as open_file:
            self.dicts = json.load(open_file)
            self.macros = self.dicts.get("macros")
            self.workflow = self.dicts.get("workflow")

    def read_inputs(self, inputs_filename):
        pattern = r'([A-Z0-9_]+)=(\S+)'
        compiled = re.compile(pattern)
        if inputs_filename:
            with open(inputs_filename, "r") as inputs_filen:
                for line in inputs_filen:
                    matched = compiled.match(line.strip())
                    if matched:
                        self.macros[matched.groups()[0]] = matched.groups()[1]

    def __skip_step(self):
        skip_steps = list()
        if os.path.exists("workflow.status"):
            with open("workflow.status") as status_file:
                for line in status_file:
                    skip_steps.append(line.strip())
            for step in self.steps:
                if step.name in skip_steps:
                    step.finished = True
                for skip_step in skip_steps:
                    if skip_step in step.pres:
                        step.pres.remove(skip_step)

        pass

    def init(self):
        self.__set_environment()
        if self.macros:
            self.__macro_replace()
        if self.workflow:
            for name in self.workflow:
                step = Step(self, name)
                step.load_from_dict(self.workflow[name])
                self.steps.append(step)
        self.__skip_step()

    def work(self):
        self.console_logger.info("Workflow start.")
        self.__check()
        while not self.__finished_check():
            self.__run()
            self.__wait()
        self.console_logger.info("Workflow end.")
        if self.status_file:
            self.status_file.close()

    def __run(self):
        self.to_runs = list()
        for step in self.steps:
            if not step.finished and len(step.pres) == 0:
                self.to_runs.append(step)
        for step in self.to_runs:
            try:
                step.run()
                self.console_logger.info("Step-{}:start.".format(step.name))
                self.file_logger.info("CMD:{}".format(step.runcmd))
            except Exception as e:
                self.console_logger.error(e.with_traceback(e.__traceback__))
                self.console_logger.error("Step-{}:start failed.".format(step.name))
                self.console_logger.error("Workflow failed.")
                exit(1)

    def __wait(self):
        for finished_step in self.to_runs:
            finished_step.join()
            if finished_step.error:
                self.console_logger.error("Step-{}:error.".format(finished_step.name))
                self.console_logger.error("Workflow break off.")
                exit(1)
            else:
                self.console_logger.info("Step-{}:end.".format(finished_step.name))
                self.__write_status(finished_step.name)
                for step in self.steps:
                    if finished_step.name in step.pres:
                        step.pres.remove(finished_step.name)

    def __macro_replace(self):
        for key in self.macros:
            if len(self.macros[key]) == 0:
                raise MacroError(key)
        content_str = json.dumps(self.workflow)
        for key in self.macros:
            value = self.macros[key]
            marco_string = "#{}#".format(key)
            content_str = content_str.replace(marco_string, value)
        self.workflow = json.loads(content_str)

    def __finished_check(self):
        for step in self.steps:
            if not step.finished:
                return False
        return True

    def __check(self):
        steps = dict()
        # post-step of every step
        for step in self.steps:
            for step_pres_name in step.pres:
                if not steps.get(step_pres_name):
                    steps[step_pres_name] = list()
                steps[step_pres_name].append(step.name)
        found = dict()

        # width-first
        for i in steps:
            found[i] = True
            for j in steps[i]:
                if found.get(j):
                    raise Exception("cycle in workflow,from {i} to {j}".format(i=i, j=j))
                found[j] = True

    def __set_environment(self):
        path = os.environ.get("PATH")
        input_path = os.path.join(os.path.curdir, "input")
        path = path + ":{}".format(os.path.abspath(os.curdir)) + ":{}".format(os.path.abspath(input_path))
        os.environ["PATH"] = path

    def __write_status(self, stepname):
        if not self.status_file:
            self.status_file = open("workflow.status", "w+")
        self.status_file.write(("{}" + os.linesep).format(stepname))


# run workflow directory
def run_workflow(workflow_dir, inputs):
    os.chdir(workflow_dir)
    workflow = WorkFlow()
    workflow_file = os.path.join(workflow_dir, "flow.json")
    workflow.load_from_file(workflow_file)
    workflow.read_inputs(inputs)
    workflow.init()
    workflow.work()


# run *.zip file
def run_target(flow, inputs, target_dir):
    dir_create(target_dir)
    with ZipFile(flow, 'r') as zipfile:
        zipfile.extractall(target_dir)
    run_workflow(target_dir, inputs)
