from fastapi import APIRouter
from typing import Any, List, Union
from app.api.ledger.dto.schema import (
    CreateAccount,
    FundDebitAccount,
    GetAccount,
    TransferFund,
    TransferSameUser,
)
from app.api.ledger.views import view_ledger

ledger = APIRouter()


@ledger.post("/create", status_code=201)
async def create_user_account(payload: CreateAccount):
    account_id = await view_ledger.create_account(payload)
    response = {"id": account_id, **payload.dict()}
    return response


@ledger.get("/single", response_model=Union[GetAccount, Any], status_code=200)
async def get_single_account_detail(account_id: int):
    response = await view_ledger.get_single_account(account_id)
    return response


@ledger.get("/user", response_model=Union[List[GetAccount], Any], status_code=200)
async def get_user_accounts_detail(user_id: int):
    response = await view_ledger.get_accounts(user_id)
    return response


@ledger.post("/fund", status_code=200)
async def fund_user_account(payload: FundDebitAccount):
    response = await view_ledger.fund_account(payload)
    return response


@ledger.post("/withdraw", status_code=200)
async def debit_user_account(payload: FundDebitAccount):
    response = await view_ledger.debit_account(payload)
    return response


@ledger.post("/transfer", status_code=200)
async def initiate_transfer(payload: TransferFund):
    response = await view_ledger.transfer_funds(payload)
    return response


@ledger.post("/transfer/me", status_code=200)
async def initiate_transfer_user(payload: TransferSameUser):
    response = await view_ledger.transfer_funds_same_user(payload)
    return response
