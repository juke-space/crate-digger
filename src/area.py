from typing import Optional
from pydantic import BaseModel
from enum import Enum

class AreaType(Enum):
    COUNTRY = 0
    STATE_PROVINCE = 1
    MUNICIPALITY = 2

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self.value < other.value
        return NotImplementedError

    def __gt__(self, other):
        if self.__class__ == other.__class__:
            return self.value > other.value
        return NotImplementedError

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.value == other.value
        return NotImplementedError

class Area(BaseModel):
    name: Optional[str] = None
    type: Optional[AreaType] = None
    municipality: Optional[str] = ""
    state_province: Optional[str] = ""
    country: Optional[str] = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO: Additional verification that if you put a level that is not country you must put the higher levels as well.
        if not self.municipality and not self.state_province and not self.country:
            raise ValueError("One of the arguments: municipality, state_province, or country must be passed.")

        if not self.type:
            if self.municipality:
                self.type = AreaType(0)
            elif self.state_province:
                self.type = AreaType(1)
            elif self.country:
                self.type = AreaType(2)

        if not self.name:
            self.name = ""
            if self.municipality:
                self.name += self.municipality
            if self.state_province:
                self.name += f", {self.state_province}"
            if self.country:
                self.name += f", {self.country}"
