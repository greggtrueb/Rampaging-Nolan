import subprocess
import sys
import time
from threading import Thread

class execRun:

    ENCODING_KEY = 'encoding'
    DEFAULT_ENCODING = 'UTF-8'
    NO_ENCODING = 'NONE'

    @staticmethod
    def runAsync(execRun):
        ret = None
        if execRun is not None:
            ret = Thread(target = execRun.runCommand)
            ret.start()
    # End run

    def __init__(self, cmd, args = None, state = {}):
        self._output = ""
        self._output_index = 0
        self._state = state
        self._cmd = cmd
        self._retCode = None
    # End __init__

    def _getCmd(self):
        return self._cmd

    def runCommand(self, encoding = None, args = {}):
        cmd = self._getCmd()

        enc = encoding
        if enc is None:
            try:
                enc = args[execRun.ENCODING_KEY]
            except:
                enc = execRun.DEFAULT_ENCODING

        if enc == execRun.NO_ENCODING:
            enc = None

        process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        terminate = False
        while self._retCode is None:
            self._retCode = process.poll()

            nextline = process.stdout.readline()
            if nextline is not None:
                if enc is not None:
                    nextline = nextline.decode(enc)
                self._output += nextline
    # End run

    def get_output(self):
        return self._output
    # End get_output

    def get_next_output(self):
        ret = None
        if len(self._output) > self._output_index:
            ret = self._output[self._output_index:]
            self._output_index = len(self._output)
        return ret
    # End get_next_output

    def get_ret_code(self):
        return self._retCode
    # End get_ret_code

    def has_exited(self):
        return self.get_ret_code() is not None
    # End has_exited

# End execRunner

 
