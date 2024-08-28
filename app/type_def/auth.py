from pydantic import BaseModel
from datetime import datetime


class RegisterUserModel(BaseModel):
    id: str | None = None
    first_name: str
    last_name: str
    password: str
    email: str
    tel: str | None = None
    created_ts: datetime | None = None
    updated_ts: datetime | None = None
    last_login_ts: datetime | None = None


class LoginUserModel(BaseModel):
    email: str
    password: str


class UserModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    tel: str | None = None
    is_super_admin: bool = False
    disabled: bool = False
    created_ts: datetime | None = None
    updated_ts: datetime | None = None
    last_login_ts: datetime | None = None


class ChangePasswordModel(BaseModel):
    new_password: str
    curr_password: str | None = None


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    password: str
    email: str
    is_super_admin: bool = False
    disabled: bool = False
    email_verified: bool = False
    tel_verified: bool = False
    tel: str | None = None
    company: str | None = None
    company_id_number: str | None = None
    company_id_url: str | None = None
    created_ts: datetime | None = None
    updated_ts: datetime | None = None
    last_login_ts: datetime | None = None


class UserXp:
    id: str
    first_name: str
    last_name: str
    password: str
    email: str
    is_super_admin: bool = False
    disabled: bool = False
    email_verified: bool = False
    tel_verified: bool = False
    tel: str | None = None
    company: str | None = None
    company_id_number: str | None = None
    company_id_url: str | None = None
    created_ts: datetime | None = None
    updated_ts: datetime | None = None
    last_login_ts: datetime | None = None

    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        password: str,
        email: str,
        is_super_admin: bool = False,
        disabled: bool = False,
        email_verified: bool = False,
        tel_verified: bool = False,
        tel: str | None = None,
        company: str | None = None,
        company_id_number: str | None = None,
        company_id_url: str | None = None,
        created_ts: datetime | None = None,
        updated_ts: datetime | None = None,
        last_login_ts: datetime | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_super_admin = is_super_admin
        self.disabled = disabled
        self.password = password
        self.email_verified = email_verified
        self.tel_verified = tel_verified
        self.tel = tel
        self.company = company
        self.company_id_number = company_id_number
        self.company_id_url = company_id_url
        self.created_ts = created_ts
        self.updated_ts = updated_ts
        self.last_login_ts = last_login_ts

    def pub(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_super_admin": self.is_super_admin,
            "disabled": self.disabled,
            "email_verified": self.email_verified,
            "tel_verified": self.tel_verified,
            "tel": self.tel,
            "company": self.company,
            "company_id_number": self.company_id_number,
            "company_id_url": self.company_id_url,
            "created_ts": self.created_ts,
            "updated_ts": self.updated_ts,
            "last_login_ts": self.last_login_ts,
        }

    def pvt(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "email": self.email,
            "is_super_admin": self.is_super_admin,
            "email_verified": self.email_verified,
            "disabled": self.disabled,
            "tel": self.tel,
            "company": self.company,
            "company_id_number": self.company_id_number,
            "company_id_url": self.company_id_url,
            "created_ts": self.created_ts,
            "updated_ts": self.updated_ts,
            "last_login_ts": self.last_login_ts,
        }


class APIKeyReq(BaseModel):
    name: str
    tenent: str
    expire_in: float
    allowed_origins: list | None = None
    scope: dict | None = None


class AuthError:
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "success": False,
            "msg": self.message,
            "result": None,
        }


class AuthSuccess:
    def __init__(self, message, result):
        self.message = message
        self.result = result

    def response(self):
        return {
            "success": True,
            "msg": self.message,
            "result": self.result,
        }
