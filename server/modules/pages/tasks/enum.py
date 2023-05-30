from enum import Enum


class TaskStatus(Enum):
    todo = "To Do"
    In_processing = "In Processing"
    pause = "Pause"
    done = "Done"


enum_dict = {e.value: e.name for e in TaskStatus}
# print(enum_dict)

# print(enum_dict)
# for k, y in enum_dict.items():
#     print(y)



# print(TaskStatus["todo"])

