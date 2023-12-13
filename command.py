from abc import ABC
from dataclasses import dataclass
import os
import platform
from typing import Dict, List, Tuple, overload


class CommandArgs:
    """
    "Frozen" list data structure, all values are either frozen or
    variable and allows you to modify non-frozen values. Non-frozen
    values also have associated labels.
    NOTE: Not optimized for extremely long commands
    """

    def __init__(
        self, cmd_string: str, variable_args: List[int] = [], labels: List[str] = []
    ) -> None:
        self._storage: List[Tuple[str, bool]] = self._process_cmd_string(
            cmd_string, variable_args
        )
        self._labels: Dict[str, int] = self._process_labels(labels)

    def _process_cmd_string(
        self, cmd_string: str, variable_args: List[int]
    ) -> List[Tuple[str, bool]]:
        string_list: List[str] = cmd_string.split(" ")
        result = [
            (string_list[i], False) if i in variable_args else (string_list[i], True)
            for i in range(len(string_list))
        ]
        return result

    def _process_labels(self, labels: List[str]) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for i in range(len(self._storage)):
            if not self._is_frozen(i):
                result[labels[0]] = i
                labels.pop(0)
                if not len(labels):
                    break
        return result

    def _set_label(self, label: str, key: int) -> None:
        if self._is_frozen(key):
            raise ValueError("Cannot label frozen key")
        else:
            self._labels[label] = key

    def _is_frozen(self, key: int) -> bool:
        return self._storage[key][1]

    def __getitem__(self, key: int) -> str:
        return self._storage[key][0]

    @overload
    def __setitem__(self, key: int, value: str) -> None:
        if self._is_frozen(key):
            raise ValueError("Cannot set frozen key")
        else:
            self._storage[key][0] = value

    @overload
    def __setitem__(self, label: str, value: str) -> None:
        key: int = self._labels[label]
        self[key] = value

    def cmd(self) -> str:
        return " ".join(self._storage)

class CommandFactory(ABC):
    def get_cmd_executor(self, os_name):
        pass

@dataclass
class CommandExecutor():
    cmd: CommandArgs
    def execute(self):
        CommandUtilities.execute_command(self.cmd)

@dataclass(eq=False)
class Command:
    cmd_factory: CommandFactory

    def execute(self):
        pass

# collection of functions relating to processing commands
class CommandUtilities:
    
    @staticmethod
    def execute_command(cmd: CommandArgs):
        os.system(cmd.cmd())
    
    @staticmethod
    def get_os():
        os_name = platform.system() 
        return os_name