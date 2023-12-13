import os
import platform
from typing import Dict, List, Tuple, overload
import schedule
import logging
from datetime import datetime
from dataclasses import dataclass, field
from abc import ABC


#@repeat(every().day.at("13:30"))
class TaskFactory():
    def __init__(self) -> None:
        self._builders : Dict[str,TaskBuilder] = {}
    
    def register_builder(self, key : str, builder : TaskBuilder) -> None:
        self._builders[key] = builder

    def get_builders(self) -> List[str]:
        return list(self._builders.keys())

class TaskBuilder(ABC):
    def __init__(self) -> None:
        pass

class WindowsBuilder(TaskBuilder):
    def __init__(self):
        pass

class LinuxBuilder(TaskBuilder):
    def __init__(self) -> None:
        pass 

class MacBuilder(TaskBuilder):
    def __init__(self) -> None:
        pass

class Task():
    def __init__(self) -> None:
        self.factory = TaskFactory()
        self.factory.register_builder("WINDOWS", WindowsBuilder())
        self.factory.register_builder("LINUX",LinuxBuilder())
        self.factory.register_builder("MAC",MacBuilder())

    def create_task(self, os, cmd : Command):
        pass


# get OS and run a shutdown command

class CommandArgs:    
    '''
        "Frozen" list data structure, all values are either frozen or
        variable and allows you to modify non-frozen values. Non-frozen
        values also have associated labels. 
        NOTE: Not optimized for extremely long commands 
    '''
    def __init__(self, cmd_string : str, frozen_args : List[int] = [], labels : List[str] = []) -> None:
        self._storage : List[Tuple[str,bool]] = self._process_cmd_string(cmd_string, frozen_args)
        self._labels : Dict[str, int] = self._process_labels(labels)

    def _process_cmd_string(self, cmd_string : str, frozen_args : List[int]) -> List[Tuple[str, bool]]:
        string_list : List[str] = cmd_string.split(" ")
        result = [(string_list[i], True) if i in frozen_args else (string_list[i], False) for i in range(len(string_list))]
        return result 
    
    def _process_labels(self, labels : List[str]) -> Dict[str, int]:
        result : Dict[str,int] = {}
        for i in range(len(self._storage)):
            if not self._is_frozen(i):
                result[labels[0]] = i
                labels.pop(0)
                if not len(labels):
                    break
        return result
    
    def _set_label(self, label : str, key : int) -> None:
        if self._is_frozen(key):
            raise ValueError("Cannot label frozen key")
        else:
            self._labels[label] = key

    def _is_frozen(self, key : int) -> bool:
        return self._storage[key][1]

    def __getitem__(self, key : int) -> str:
        return self._storage[key][0]
    
    @overload
    def __setitem__(self, key : int, value : str) -> None:
        if self._is_frozen(key):
            raise ValueError("Cannot set frozen key")
        else:
            self._storage[key][0] = value

    @overload
    def __setitem__(self, label : str, value : str) -> None:
        key : int = self._labels[label]
        self[key] = value

    def cmd(self) -> str:
        return 

class ShutdownArgs(CommandArgs):
    def __init__(self) -> None:
        super(ShutdownArgs, self).__init__()




@dataclass(eq=False)
class Command:
    cmd_map : Dict[str, str] = {}

@dataclass(eq=False)
class Shutdown(Command):
    cmd_map : Dict[str, str] = {
        "WINDOWS" : "shudown /s /t 1",
        "LINUX" : "",
        "MAC" : ""
    }

    def execute(self):
        pass
        

os_name : str = platform.system()

if os_name == 'Windows': # windows 
    os.system('shutdown /s /t 1')
elif os_name == 'Linux' or os_name == 'Darwin': # linux & mac
    os.system('sudo shutdown now')
else:
    raise RuntimeError("Unsupported OS.")

