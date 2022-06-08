import uuid
from app.api.ledger.dto.schema import (
    CreateAccount,
    FundDebitAccount,
    GetAccount,
    TransferFund,
    TransferSameUser,
    UpdateAccount,
)
from app.api.models.db import ledger, database
from typing import Any, List, Union
from sqlalchemy import update, select
from app.api.user.views.view_users import get_user
from app.api.utils.not_found import base_response
from app.api.utils.constants import (
    ACCOUNT_NOT_FOUND,
    INSUFFICIENT_FUNDS,
    DUPLICATE_ACCOUNT_IDS,
    NO_LINKED_ACCOUNTS,
    ACCOUNT_CREATION_LIMIT,
    NOT_USER_ACCOUNTS,
    SOURCE_ACCOUNT_NOT_FOUND,
    DESTINATION_ACCOUNT_NOT_FOUND,
    USER_NOT_FOUND,
)


async def create_account(payload: CreateAccount):
    """
    this method creates a user account
    """
    user = await get_user(payload.user)
    if user == base_response(USER_NOT_FOUND):
        return user
    check_user_limit = await get_accounts(payload.user)
    # if check_user_limit == base_response(NO_LINKED_ACCOUNTS):
    #     return check_user_limit
    if len(check_user_limit) == 10:
        return {"message": ACCOUNT_CREATION_LIMIT}
    query = ledger.insert().values(
        user=payload.user, account_id=str(uuid.uuid4()), balance=0.0, active=True
    )
    return await database.execute(query)


async def get_single_account(account_id: int) -> GetAccount:
    """
    this method gets the detail of a single account
    """
    query = select(ledger).where(ledger.c.id == account_id)
    result = await database.fetch_one(query)
    if not result:
        return base_response(ACCOUNT_NOT_FOUND)
    return result


async def get_accounts(user_id: int) -> Union[List[GetAccount], List]:
    """
    this method gets all the accounts linked to a particular user
    """
    query = select(ledger).where(ledger.c.user == user_id)
    result = await database.fetch_all(query)
    if not len(result):
        return base_response(NO_LINKED_ACCOUNTS)
    return result


async def check_account_balance(account_id: int, amount: Union[int, float]) -> bool:
    """
    this method ensures the user does not exceed his transfer or debit limit
    """
    account = await get_single_account(account_id)
    if account == base_response(ACCOUNT_NOT_FOUND):
        return account
    # check if the user's account has at least 10 tokens
    if int(account.balance - amount) < 10:
        return False
    return True


def check_duplicating_account_ids(source_id: str, receiving_id: str) -> bool:
    """
    this helper ensures the source and destination account during transaction are not the same
    """
    return source_id == receiving_id


async def fund_account(payload: FundDebitAccount):
    """
    this method helps to fund an account
    """
    account = await get_single_account(payload.account_id)
    if account == base_response(ACCOUNT_NOT_FOUND):
        return account
    # update the account
    updated_balance = {"balance": account.balance + payload.amount}
    funded_account = await update_account(account.id, updated_balance)
    return {"message": "account funded successfully"}


async def debit_account(payload: FundDebitAccount):
    """
    this method helps to debit account
    """
    account = await get_single_account(payload.account_id)
    if account == base_response(ACCOUNT_NOT_FOUND):
        return account
    # update the account
    # check the account balance to ensure the user did not withdraw pass the specified limit
    check_amount = await check_account_balance(payload.account_id, payload.amount)
    if not check_amount:
        return {"message": INSUFFICIENT_FUNDS}
    # update the account
    updated_balance = {"balance": account.balance - payload.amount}
    debited_account = await update_account(account.id, updated_balance)
    return {"message": "account debited successfully"}


async def transfer_funds(payload: TransferFund):
    """
    this method helps to facilitate transactions between two accounts, from different users
    """
    check_balance = await check_account_balance(payload.account_id, payload.amount)
    if not check_balance:
        return {"message": INSUFFICIENT_FUNDS}
    query_first_account = await get_single_account(payload.account_id)
    if query_first_account == base_response(ACCOUNT_NOT_FOUND):
        return base_response(SOURCE_ACCOUNT_NOT_FOUND)
    query_second_account = await get_single_account(payload.destination_id)
    if query_second_account == base_response(ACCOUNT_NOT_FOUND):
        return base_response(DESTINATION_ACCOUNT_NOT_FOUND)

    if check_duplicating_account_ids(payload.account_id, payload.destination_id):
        return {"message": DUPLICATE_ACCOUNT_IDS}
    # update the first and second account
    first_account_amount = {"balance": query_first_account.balance - payload.amount}
    second_account_amount = {"balance": query_second_account.balance - payload.amount}
    update_first_account = await update_account(
        query_first_account.id, first_account_amount
    )
    update_second_account = await update_account(
        query_first_account.id, second_account_amount
    )
    return {"message": "transfer success"}


async def transfer_funds_same_user(payload: TransferSameUser):
    """
    this method helps to facilitate transactions between two accounts, from the same user
    """
    check_balance = await check_account_balance(payload.account_id, payload.amount)
    if not check_balance:
        return {"message": INSUFFICIENT_FUNDS}
    # get all the accounts linked to that user
    user_accounts = await get_accounts(payload.user_id)
    if user_accounts == base_response(NO_LINKED_ACCOUNTS):
        return user_accounts
    query_first_account = await get_single_account(payload.account_id)
    if query_first_account == base_response(ACCOUNT_NOT_FOUND):
        return base_response(SOURCE_ACCOUNT_NOT_FOUND)
    query_second_account = await get_single_account(payload.destination_id)
    if query_second_account == base_response(ACCOUNT_NOT_FOUND):
        return base_response(DESTINATION_ACCOUNT_NOT_FOUND)

    # ensure the accounts are linked to one user
    if (
        all(acc in user_accounts for acc in [query_first_account, query_second_account])
        == False
    ):
        return {"message": NOT_USER_ACCOUNTS}

    if check_duplicating_account_ids(payload.account_id, payload.destination_id):
        return {"message": DUPLICATE_ACCOUNT_IDS}

    # update the first and second account
    first_account_amount = {"balance": query_first_account.balance - payload.amount}
    second_account_amount = {"balance": query_second_account.balance - payload.amount}
    update_first_account = await update_account(
        query_first_account.id, first_account_amount
    )
    update_second_account = await update_account(
        query_first_account.id, second_account_amount
    )
    return {
        "message": "transfer success",
        "data": {update_first_account["data"], update_second_account["data"]},
    }


async def update_account(id: int, payload: UpdateAccount):
    """
    this method helps to update the information of an account
    """
    account = await get_single_account(id)
    # payload = payload.dict(exclude_unset=True)
    query = update(ledger).where(ledger.c.id == account.id).values(**payload)
    await database.execute(query)
    return {"message": "account updated successfully !"}
