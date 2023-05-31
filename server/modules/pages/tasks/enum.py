from enum import Enum


class TaskStatus(Enum):
    todo = "To Do"
    In_processing = "In Processing"
    pause = "Pause"
    done = "Done"


enum_dict = {e.value: e.name for e in TaskStatus}

