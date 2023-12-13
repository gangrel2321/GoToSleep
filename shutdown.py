from dataclasses import dataclass
from .command import CommandFactory, CommandExecutor, CommandArgs, Command

class ShutdownFactory(CommandFactory):
    def get_cmd_executor(self, os_name):
        if os_name == "Windows":
            return ShutdownWindows()
        elif os_name == "Darwin":
            return ShutdownMac()
        elif os_name == "Linux":
            return ShutdownLinux()
        else:
            raise RuntimeError("Unsupported OS.")

@dataclass(eq=False)
class Shutdown(Command):
    cmd_factory : ShutdownFactory = ShutdownFactory()

    def execute(self, os_name : str):
        shutdown_executor = self.cmd_factory.get_cmd_executor(os_name)
        shutdown_executor.execute()

@dataclass
class ShutdownWindows(CommandExecutor):
    cmd: CommandArgs = CommandArgs("shudown /s /t 1")

@dataclass
class ShutdownMac(CommandExecutor):
    cmd: CommandArgs = CommandArgs("sudo shutdown now")

@dataclass
class ShutdownLinux(CommandExecutor):
    cmd: CommandArgs = CommandArgs("sudo shutdown now")