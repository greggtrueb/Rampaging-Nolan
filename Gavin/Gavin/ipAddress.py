import execRunner
import os

class interfaces:

    LINUX_IF_COMMAND = "ifconfig"
    WINDOWS_IF_COMMAND = "ipconfig /all"

    def __init__(self):
        self.ipAddresses = []
        self._load()
    # End __init__

    def _load(self):
        isWindows = False
        ipCommand = interfaces.LINUX_IF_COMMAND
        if os.name == 'nt':
            isWindows = True
            ipCommand = interfaces.WINDOWS_IF_COMMAND

        e = execRunner.execRun(ipCommand)
        e.runCommand()
        output = e.get_output()
        if output is None or e.get_ret_code() != 0:
            raise Exception("Could not run {0}\n Unable to load ip addresses".format(ipCommand))

        if isWindows:
            self._parse_windows_if_command(output)
        else:
            self._parse_linux_if_command(output)
    # End _load

    def _parse_windows_if_command(self, output):
        if output is not None:
            lines = output.split("\n")

            currentAdapter = None
            for line in lines:
                if currentAdapter is not None:
                    pass
                else:
                    if line.startswith("Ethernet adapter"):
                        currentAdapter = adapter(line.rstrip("Ethernet adapter ").lstrip(":"))
    # End _parse_windows_if_command


# End interfaces

class adapter:

    def __init__(self, name):
        self.name = name
    # End __init__
# End adapter

i = interfaces() 