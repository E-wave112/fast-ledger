from datetime import date
from pydantic import BaseModel
from typing import Optional, Union
from app.api.utils.optional_model import AllOptional


class TransferFund(BaseModel):
    account_id: int
    destination_id: str
    amount: float


class TransferSameUser(TransferFund):
    user_id: int
    destination_id: int


class GetAccount(BaseModel):
    id: int
    account_id: str
    balance: float
    active: bool
    user: Union[int, None]
    created_at: date
    updated_at: date


class CreateAccount(BaseModel):
    user: Union[int, None]


class FundDebitAccount(BaseModel):
    account_id: int
    amount: Union[int, float]


class UpdateAccount(BaseModel):
    balance: Optional[Union[int, float]]
    active: Optional[bool]
