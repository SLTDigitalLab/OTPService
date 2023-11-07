from pydantic import BaseModel


class SMSOTPSendRq(BaseModel):
    mobile: str


class SMSOTPVerifyRq(BaseModel):
    mobile: str
    otp: str
    client_secret: str


class SMSMarketingSendRq(BaseModel):
    mobile: str
    msg: str


class EmailOTPSendRq(BaseModel):
    email: str


class EmailOTPVerifyRq(BaseModel):
    email: str
    otp: str
    client_secret: str


class EmailMarketingSendRq(BaseModel):
    email: str
    msg: str
