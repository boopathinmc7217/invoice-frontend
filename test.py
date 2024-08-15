

from enum import Enum

class data(Enum):

    done = "one",1
    done1 = "two",1
    done2 = "three",1
    __slots__    = ("name", "value")

    def __init__(self,name,value) -> None:
        self.name=name
        self.value=value
        super().__init__(name,value)

print(data.done.name)