# coding: utf-8
import sys
import re
import json
import os
import io
from zipfile import ZipFile
import shutil
from GPyFlow.errors import MacroError, CycleInWorkflowError
from GPyFlow.step import Step
from GPyFlow.filetools import dir_create
from GPyFlow.log import getlogger
from GPyFlow.proc import Writer

# step name can only by numbers, letters and underscores
step_re_pattern = re.compile(r"Step-([a-z0-9_]+)")
# . for extension; / for path;
input_pattern = re.compile(r"<([A-Za-z0-9_./#]+)>")
output_pattern = re.compile(r"\[([A-Za-z0-9_./#]+)\]")


class WorkFlow(object, ):
    def __init__(self, workflow_dir, inputs):
        self.name = os.path.basename(workflow_dir)
        self.workflow_dir = os.path.abspath(workflow_dir)
        self.inputs = os.path.abspath(inputs)
        self.dicts = dict()
        self.status_filename = os.path.join(self.workflow_dir, "{}.ok.log".format(self.name))
        self.macros = dict()
        self.workflow = dict()
        self.console_logger = getlogger(__name__)
        self.file_logger = \
            getlogger("cmd", os.path.join(workflow_dir, "{}.command.log".format(self.name)))

        self.out_writer = Writer(os.path.abspath(os.path.join(workflow_dir, "{}.out".format(self.name))))
        self.err_writer = Writer(os.path.abspath(os.path.join(workflow_dir, "{}.err".format(self.name))))
        self.steps = list()
        self.to_runs = list()
        self.finished = False
        self.waits = list()
        pass

    @staticmethod
    def __get_step_name(step_string):
        matched = step_re_pattern.match(step_string)
        if matched:
            return matched.groups()[0]
        return ""

    def __render_workflow(self, origin_workflow):
        rendered = {}
        links = origin_workflow["links"]
        nodes = origin_workflow["nodes"]

        def find_index_of_step(step_name):
            for i, node in enumerate(nodes):
                if node["name"] == step_name:
                    return i

        # init
        for node in nodes:
            rendered[node["name"]] = {}
            rendered[node["name"]]["pres"] = []

        for link in links:
            from_step = self.__get_step_name(link["from"])
            from_index = find_index_of_step(from_step)
            to_step = self.__get_step_name(link["to"])
            to_index = find_index_of_step(to_step)

            if not (from_step in rendered[to_step]["pres"]):
                rendered[to_step]["pres"].append(from_step)

            if step_re_pattern.search(link["frompid"]) or \
                    step_re_pattern.search(link["topid"]):
                continue
            # remove out port []
            replace_str = "{}".format(link["frompid"])
            origin_str = "[{}]".format(link["frompid"])
            nodes[from_index]["cmd"] = nodes[from_index]["cmd"].replace(origin_str, replace_str)

            # connect port remove in port <>
            origin_str = "<{}>".format(link["topid"])
            nodes[to_index]["cmd"] = nodes[to_index]["cmd"].replace(origin_str, replace_str)

        for node in nodes:
            # remove in <>
            matched = input_pattern.findall(node["cmd"])
            if matched:
                for _input in matched:
                    origin_str = "<{}>".format(_input)
                    replace_str = "{}".format(_input)
                    node["cmd"] = node["cmd"].replace(origin_str, replace_str)

            # remove in []
            matched = output_pattern.findall(node["cmd"])
            if matched:
                for _input in matched:
                    origin_str = "[{}]".format(_input)
                    replace_str = "{}".format(_input)
                    node["cmd"] = node["cmd"].replace(origin_str, replace_str)

            rendered[node["name"]]["cmd"] = node["cmd"]
        return rendered

    def __load_from_file(self, filepath):
        with open(filepath, 'r') as open_file:
            self.dicts = json.load(open_file)
            self.macros = self.dicts.get("macros")
            origin_workflow = self.dicts.get("workflow")
            self.workflow = self.__render_workflow(origin_workflow)

    @staticmethod
    def __escape(origin_str):
        render = origin_str.replace("\"", "\\\"")
        render = render.replace("\\t", "\\\\t")
        return render

    def __read_inputs(self, inputs_filename):
        pattern = r'([A-Z0-9_]+)=(.+)\n'
        compiled = re.compile(pattern)
        with open(inputs_filename, "r") as inputs_file:
            for line in inputs_file:
                matched = compiled.match(line)
                if not matched:
                    continue
                else:
                    self.macros[matched.groups()[0]] = self.__escape(matched.groups()[1])

    def __skip_step(self):
        skip_steps = list()
        if os.path.exists(self.status_filename):
            with open(self.status_filename) as file:
                for line in file:
                    skip_steps.append(line.strip())
            for step in self.steps:
                if step.name in skip_steps:
                    step.finished = True
                for skip_step in skip_steps:
                    if skip_step in step.pres:
                        step.pres.remove(skip_step)

        pass

    def __run(self):
        self.to_runs = list()
        for step in self.steps:
            if not step.finished and len(step.pres) == 0:
                self.to_runs.append(step)
        for step in self.to_runs:
            try:
                step.run()
                self.console_logger.info("Step-{}:start.".format(step.name))
                self.file_logger.info("CMD:{}".format(step.command))
            except Exception as e:
                self.console_logger.error("Step-{}:failed.".format(step.name))
                self.console_logger.error("Workflow failed.")
                self.console_logger.exception(e)

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
        content_str = json.dumps(self.workflow)
        for key in self.macros:
            value = self.macros[key]
            marco_string = '#{}#'.format(key)
            content_str = content_str.replace(marco_string, value)
        self.workflow = json.loads(content_str)

    def __finished_check(self):
        for step in self.steps:
            if not step.finished:
                return False
        return True

    def __check(self, preview=False):

        output = io.StringIO()

        steps = list()
        stack = list()
        for step in self.steps:
            new_step = dict()
            new_step["name"] = step.name
            new_step["pres"] = list(step.pres)
            new_step["command"] = step.command
            steps.append(new_step)

        for step in steps:
            if len(step["pres"]) == 0:
                stack.append(step)
                steps.remove(step)

        no = 1
        while len(stack) > 0:
            pop_step = stack.pop()
            output.write(" [{}] ".format(no))
            output.write(pop_step["command"])
            output.write(os.linesep)
            no += 1

            for step in steps:
                if pop_step["name"] in step["pres"]:
                    step["pres"].remove(pop_step["name"])

            for step in steps:
                if len(step["pres"]) == 0:
                    stack.append(step)
                    steps.remove(step)

        if len(steps) > 0:
            cycles = list()
            for step in steps:
                cycles.append(step["name"])
            raise CycleInWorkflowError(cycles)

        if preview:
            content = output.getvalue()
            sys.stdout.write(content)
            sys.stdout.flush()
        output.close()

    @staticmethod
    def __set_environment():
        path = os.environ.get("PATH")
        path = path + ":{}".format(os.path.abspath(os.curdir))
        os.environ["PATH"] = path

    def __write_status(self, step_name):
        if not os.path.exists(self.status_filename):
            write_to_file = open(self.status_filename, "w")
        else:
            write_to_file = open(self.status_filename, "a")
        write_to_file.write(("{}" + os.linesep).format(step_name))
        write_to_file.close()

    def preview(self):
        self.__check(preview=True)

    def init(self):
        workflow_file = os.path.join(self.workflow_dir, "flow.json")
        self.__load_from_file(workflow_file)
        self.__read_inputs(self.inputs)
        os.chdir(self.workflow_dir)
        # 设置环境变量
        self.__set_environment()
        # 宏替换
        if self.macros:
            self.__macro_replace()
        # 加载步骤
        if self.workflow:
            for name in self.workflow:
                step = Step(self, name)
                step.load_from_dict(self.workflow[name])
                self.steps.append(step)

    def work(self):
        self.console_logger.info("Workflow start.")
        self.__check()
        self.__skip_step()
        while not self.__finished_check():
            self.__run()
            self.__wait()
        self.console_logger.info("Workflow end.")


# run workflow directory
def run_workflow(preview, workflow_dir, inputs):
    workflow = WorkFlow(workflow_dir, inputs)
    workflow.init()
    if preview:
        workflow.preview()
    else:
        workflow.work()


# run *.zip file
def run_target_zip(preview, flow, inputs, target_dir):
    dir_create(target_dir)
    with ZipFile(flow, 'r') as zipfile:
        zipfile.extractall(target_dir)
    run_workflow(preview, target_dir, inputs)


# run *.json file
def run_targe_json(preview, flow, inputs, target_dir):
    dir_create(target_dir)
    des = os.path.join(target_dir, "flow.json")
    shutil.copy(flow, des)
    run_workflow(preview, target_dir, inputs)


# run
def run_target(preview, flow, inputs, target_dir):
    ext = os.path.basename(flow).split(".")[-1]
    if ext == "zip":
        run_target_zip(preview, flow, inputs, target_dir)
    else:
        run_targe_json(preview, flow, inputs, target_dir)
