from pydantic import BaseModel, PositiveInt, validator
from typing import Optional

class ConnectFourGameSettings(BaseModel):
    width: Optional[PositiveInt]
    height: Optional[PositiveInt]
    player_num: Optional[PositiveInt]


class UserInput(BaseModel):
    max_value: int
    value: int

    @validator('value')
    def validate_value(cls, value: int, values):
        if value < 0 or value > values['max_value']:
            raise ValueError(f"Value must be a positive integer and not bigger than {values['max_value']}")
        return value