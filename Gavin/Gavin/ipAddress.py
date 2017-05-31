import execRunner
import os

class interfaces:

    LINUX_IF_COMMAND = "ifconfig"
    WINDOWS_IF_COMMAND = "ipconfig /all"

    def __init__(self):
        self.adapters = []
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
            blankLines = 0
            for line in lines:
                if line.startswith("Ethernet adapter"):
                    currentAdapter = adapter(line.lstrip("Ethernet adapter ").rstrip(":"))
                elif currentAdapter is not None:
                    if line is not None:
                        split = line.split(":")
                        if len(split) == 2:
                            if split[0].strip().startswith("Physical"):
                                currentAdapter.MAC_address = split[1].strip()
                            elif split[0].strip().startswith("IPv4"):
                                currentAdapter.ip_address = split[1].strip()
                        else:
                            blankLines += 1
                if blankLines == 2:
                    blankLines = 1
                    self.adapters.append(currentAdapter)
                    currentAdapter = None

    # End _parse_windows_if_command

    def print(self):
        for adp in self.adapters:
            adp.print()

# End interfaces

class adapter:

    def __init__(self, name):
        self.name = name
        self.MAC_address = None
        self.ip_address = None
    # End __init__

    def print(self):
        print(self.name)
        print("MAC -> {0}".format(self.MAC_address))
        print("IPv4 Address -> {0}".format(self.ip_address))
# End adapter

i = interfaces() 
i.print()