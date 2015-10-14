
from subprocess import Popen, PIPE, STDOUT

class BashCommand(object):
    args = []
    status = None
    cmd_out = None
    data = None

    def __init__(self, arguments):
        self.args = arguments

    def run_command(self):
        assert isinstance(self.args,list)
        cmd = Popen(self.args, stdout = PIPE, stderr = STDOUT)
        try:
            self.cmd_out = cmd
        except Exception as e:
            return (False, e)
        return (True, None)

    def read_data(self):
        try:
            self.data = self.cmd_out.communicate()
        except Exception as e:
            return (False,e)
        return (True,None)

    def get_args(self):
        return self.args

    def set_args(self,new_args):
        assert isinstance(new_args,list)
        self.args=new_args

    def get_data(self):
        return self.data
