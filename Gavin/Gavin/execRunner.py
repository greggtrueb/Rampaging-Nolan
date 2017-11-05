import subprocess
import sys
import time
from threading import Thread

class execRun:

    ENCODING_KEY = 'encoding'
    DEFAULT_ENCODING = 'UTF-8'
    NO_ENCODING = 'NONE'
    SHELL_ARGUMENT = 'SHELL'

    @staticmethod
    def runAsync(execRun):
        ret = None
        if execRun is not None:
            ret = Thread(target = execRun.runCommand)
            ret.start()

        return ret
    # End run

    def __init__(self, cmd, args = None, state = {}):
        self._output = ""
        self._output_index = 0
        self._state = state
        self._cmd = cmd
        self._retCode = None
        self._process = None
        self._encoding = execRun.NO_ENCODING
    # End __init__

    def _set_encoding(self, encoding = None, args = {}):
        self._encoding = encoding
        if self._encoding is None:
            try:
                self._encoding = args[execRun.ENCODING_KEY]
            except:
                self._encoding = execRun.DEFAULT_ENCODING

        if self._encoding == execRun.NO_ENCODING:
            self._encoding = None
    # End _set_encoding

    def _start_process(self):
        if self._cmd is None:
            raise Exception("No command spcified in exec runner")

        shell = False
        try:
            if self._state[SHELL_ARGUMENT]:
                shell = True
        except:
            shell = False

        self._process = subprocess.Popen(self._cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = shell)

        if self._process is None:
            raise Exception("Could not start process {0}".format(self._cmd))

        return self._process
    # End _start_process

    def runCommand(self, encoding = None, read_size = 256, args = {}):
        self._set_encoding(encoding = encoding, args = args)

        self._start_process()

        terminate = False
        while self._retCode is None:
            self._retCode = self._process.poll()
            
            nextChunk = self._process.stdout.read(read_size)
            if nextChunk is not None:
                if self._encoding is not None:
                    nextChunk = nextChunk.decode(self._encoding)
                self._output += nextChunk

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

    def get_pid(self):
        if self._process is not None:
            return self._process.pid
        return None
    # End get_pid

    def has_exited(self):
        return self.get_ret_code() is not None
    # End has_exited

# End execRun

 
