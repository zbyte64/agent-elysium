from pydantic import BaseModel


class UserState(BaseModel):
    biography: str = "A citizen"
    money: float = 10
    income: float = 1000
    rent_cost: float = 2000
    rent_paid: bool = False
    has_job: bool = True
    housed: bool = True
    robbed: bool = False
    warrant: bool = False
    day: int = 0
    leaving: str = ""
