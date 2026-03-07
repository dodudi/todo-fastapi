from enum import Enum


class TodoStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TodoPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
