from datetime import datetime
from pydantic import BaseModel, constr
from app.api.utils.constants import EMAIL_REGEX, PHONE_NUMBER_REGEX
from app.api.utils.optional_model import AllOptional
from typing import Optional


class AddUser(BaseModel):
    firstName: constr(min_length=3, max_length=50)
    lastName: constr(min_length=3, max_length=50)
    email: constr(min_length=3, max_length=50, regex=EMAIL_REGEX)
    phone: constr(min_length=3, max_length=11, regex=PHONE_NUMBER_REGEX)


class GetUser(AddUser):
    id: int
    created_at: datetime
    updated_at: datetime


class EmailPhone(BaseModel):
    email: Optional[constr(min_length=3, max_length=50, regex=EMAIL_REGEX)]
    phone: Optional[constr(min_length=3, max_length=11, regex=PHONE_NUMBER_REGEX)]


class UpdateUser(BaseModel):
    firstName: Optional[constr(min_length=3, max_length=50)]
    lastName: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[constr(min_length=3, max_length=50, regex=EMAIL_REGEX)] = None
    phone: Optional[
        constr(min_length=3, max_length=11, regex=PHONE_NUMBER_REGEX)
    ] = None
