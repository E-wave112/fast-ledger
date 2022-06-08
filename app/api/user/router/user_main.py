from fastapi import APIRouter
from typing import List, Union, Dict, Any
from app.api.user.dto.schema import GetUser, AddUser, UpdateUser
from app.api.user.views import view_users


users = APIRouter()


@users.post("/create", response_model=Union[GetUser, Any], status_code=201)
async def create_user(payload: AddUser):
    user_id = await view_users.add_users(payload)
    response = {"id": user_id, **payload.dict()}
    return response


@users.get("/all", response_model=Union[List[GetUser], List], status_code=200)
async def get_all_users():
    users = await view_users.get_users()
    return users


@users.get("/{id}", response_model=Union[GetUser, Dict], status_code=200)
async def get_single_user(id: int):
    user = await view_users.get_user(id)
    return user


@users.patch("/update/{id}", status_code=200)
async def update_user(id: int, payload: UpdateUser):
    user_update = await view_users.update_user(id, payload)
    return user_update
