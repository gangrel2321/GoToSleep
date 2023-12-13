from dataclasses import dataclass
from .command import CommandFactory, CommandExecutor, CommandArgs, Command

class DisableWifiFactory(CommandFactory):
    def get_cmd_executor(self, os_name):
        if os_name == "Windows":
            return DisableWifiWindows()
        elif os_name == "Darwin":
            return DisableWifiMac()
        elif os_name == "Linux":
            return DisableWifiLinux()
        else:
            raise RuntimeError("Unsupported OS.")

@dataclass(eq=False)
class DisableWifi(Command):
    cmd_factory : DisableWifiFactory = DisableWifiFactory()

    def execute(self, os_name : str):
        shutdown_executor = self.cmd_factory.get_cmd_executor(os_name)
        shutdown_executor.execute()

@dataclass
class DisableWifiWindows(CommandExecutor):
    cmd: CommandArgs = CommandArgs("STUFF")

@dataclass
class DisableWifiMac(CommandExecutor):
    cmd: CommandArgs = CommandArgs("STUFF")

@dataclass
class DisableWifiLinux(CommandExecutor):
    cmd: CommandArgs = CommandArgs("STUFF")
