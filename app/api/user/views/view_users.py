from app.api.user.dto.schema import AddUser, EmailPhone, GetUser, UpdateUser
from app.api.models.db import users, database
from typing import Any, List, Union
from sqlalchemy import update, select, or_
from app.api.utils.not_found import base_response
from app.api.utils.constants import (
    USER_ALREADY_EXISTS,
    USER_NOT_FOUND,
    EMPTY_USER_TABLE,
)


async def add_users(payload: AddUser):
    """
    this method assumes that the user is not already present in the database
    """
    # check if the user is already present in the database
    check_user = await find_user_by_email_or_phone(
        {"email": payload.email, "phone": payload.phone}
    )
    print(check_user)
    if check_user:
        return base_response(USER_ALREADY_EXISTS)
    query = users.insert().values(**payload.dict())
    return await database.execute(query)


async def find_user_by_email_or_phone(payload: EmailPhone) -> Union[GetUser, None]:
    query = users.select().where(
        or_(users.c.phone == payload["phone"], users.c.email == payload["email"])
    )
    result = await database.fetch_one(query)
    return result


async def get_users() -> Union[List[GetUser], List]:
    query = select(users)
    result = await database.fetch_all(query)
    if len(result) == 0:
        return [{"message": EMPTY_USER_TABLE}]
    return result


async def get_user(id: int) -> GetUser:
    query = select(users).where(users.c.id == id)
    result = await database.fetch_one(query)
    if not result:
        return base_response(USER_NOT_FOUND)
    return result


async def update_user(id: int, payload: UpdateUser):
    user = await get_user(id)
    if user == base_response(USER_NOT_FOUND):
        return base_response(USER_NOT_FOUND)

    payload_data = payload.dict(exclude_unset=True)
    query = update(users).where(users.c.id == user.id).values(**payload_data)

    await database.execute(query)
    return {"message": "user updated successfully!"}
