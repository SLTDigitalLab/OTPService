from pydantic import BaseModel
from datetime import datetime
from type_def.auth import User

class Tenent(BaseModel):
    id: str
    user_id: str
    name: str
    email_otp_size: int = 6
    email_otp_expired_in_s: int = 300
    email_otp_max_tries: int = 3
    sms_otp_size: int = 6
    sms_otp_expired_in_s: int = 300
    sms_otp_max_tries: int = 3
    sms_otp_template: str = (
        "Your OTP is {otp}. It's expired at {expired_at}. (Created: {created_at}))"
    )
    email_otp_template: str = (
        "Your OTP is {otp}. It's expired at {expired_at}. (Created: {created_at}))"
    )
    verified: bool = False
    disabled: bool = False
    created_ts: datetime | None = None
    updated_ts: datetime | None = None

class TenentRq(BaseModel):
    name: str
    email_otp_size: int = 6
    email_otp_expired_in_s: int = 300
    email_otp_max_tries: int = 3
    sms_otp_size: int = 6
    sms_otp_expired_in_s: int = 300
    sms_otp_max_tries: int = 3
    sms_otp_template: str = (
        "Your OTP is {otp}. It's expired at {expired_at}. (Created: {created_at}))"
    )
    email_otp_template: str = (
        "Your OTP is {otp}. It's expired at {expired_at}. (Created: {created_at}))"
    )

class TenentRenameRq(BaseModel):
    name: str