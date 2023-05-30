from enum import Enum


class TokenType(Enum):
    access = "Access"
    reset = "Reset"
    active = "Active"

    def enum_dict(self):
        return {e.value: e.name for e in TokenType}


enum_dict = {e.value: e.name for e in TokenType}
