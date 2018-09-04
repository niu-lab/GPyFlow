class MacroError(Exception):
    def __init__(self, macro):
        self.macro = macro

    def __str__(self):
        return "macro {} value can't be empty.".format(self.macro)


class StepNameError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "step name can't be empty."


class StepLoopError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "step pres can't include it's self."


class StepPresError(Exception):
    def __init__(self, step_name, pre_name):
        self.step_name = step_name
        self.pre_name = pre_name
        pass

    def __str__(self):
        return "in step {step_name}, {pre_name} prestep not found.".format(step_name=self.step_name,
                                                                           pre_name=self.pre_name)


class StepRunError(Exception):
    def __init__(self, step_name):
        self.step_name = step_name
        pass

    def __str__(self):
        return "run command or run config  not found in step {step_name}.".format(step_name=self.step_name)


class PlaceHolderNotMatchedError(Exception):
    def __init__(self, step_name):
        self.step_name = step_name
        pass

    def __str__(self):
        return "{} placeholder not match input or output.".format(self.step_name)


class PathError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "not found {}".format(self.path)


class RunCmdException(Exception, ):
    def __init__(self, cmd, outinfo, errinfo):
        self.cmd = cmd
        self.outinfo = outinfo
        self.errinfo = errinfo
        pass

    def __str__(self):
        return "\nCMDERR:{cmd}\nERRINFO:{outinfo}\n{errinfo}".format(cmd=self.cmd,
                                                                     outinfo=self.outinfo,
                                                                     errinfo=self.errinfo)
