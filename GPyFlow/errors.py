class MacroError(Exception):
    def __init__(self, macro):
        self.macro = macro

    def __str__(self):
        return "{} value error.".format(self.macro)


class CycleInWorkflowError(Exception):
    def __init__(self, step_names):
        self.step_names = step_names
        pass

    def __str__(self):
        return "cycle in workflow: {}".format(",".join(self.step_names))


class RunCmdException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd
        pass

    def __str__(self):
        return "CMDERR:{cmd}".format(cmd=self.cmd)
