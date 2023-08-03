from pydantic import BaseModel


class RequestUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    password: str
    role: int


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    role: int
    is_active: bool
    created_at: str
    updated_at: str
