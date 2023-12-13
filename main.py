from typing import List,Optional
from time import sleep
from datetime import datetime, time
from .command import CommandUtilities, Command  # add
from .shutdown import Shutdown
from .disableWifi import DisableWifi

# @repeat(every().day.at("13:30"))
def equal_time(time1 : time, time2 : time) -> bool:
    # checks time equality to the minute
    return time1.hour == time2.hour and time1.minute == time2.minute

def example_run():
    os_name = CommandUtilities.detect_os()
    sched_time = time(16,30) # 16:30
    shutdown_task = Task("Shutdown", Shutdown(),sched_time,os_name)
    no_wifi_task = Task("DisableInternet", DisableWifi(),time(16,20),os_name)
    tr = TaskRunner()
    tr.add_task(shutdown_task)
    while True:
        tr.check_tasks()
        sleep(20) # sleep 20 seconds 

class Task:
    # sequence of commands with a schedule
    def __init__(self, name: str, cmd: Optional[Command] = None, sched: Optional[time] = None, os_name: Optional[str] = None) -> None:
        self.cmd: Optional[Command] = cmd
        self.sched: Optional[time] = sched
        self.os_name: Optional[str] = os_name        
        self.task_name: str = name

    def execute(self): # run cmd seq
        self.cmd.execute()

#want to execute Task objects but task objects have commands which depend on operating system (so factory for commands not task?)

class TaskRunner:

    def __init__(self, tasks : List[Task] = []):
        self.tasks = tasks
        for task in self.tasks:
            task.initialize()
        
    def add_task(self, task : Task):
        self.tasks.append(task)
        task.initialize() 

    def check_tasks(self):
        cur_time : time = datetime.now().time()
        for task in self.tasks:
            if equal_time(task.sched, cur_time):
                task.execute()





