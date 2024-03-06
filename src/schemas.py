from datetime import datetime
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    birthday: datetime
    additional_info: str = Field(max_length=150)


class ContactModel(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
