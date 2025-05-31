from pydantic import BaseModel


class UserState(BaseModel):
    money: float = 10
    income: float = 5000
    rent_cost: float = 2000
    rent_paid: bool = False
    has_job: bool = True
    housed: bool = True
    imprisoned: bool = False
    robbed: bool = False
    warrant: bool = False
