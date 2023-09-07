from pydantic import BaseModel

class SMSOTPSendRq(BaseModel):
    mobile: str

class EmailOTPSendRq(BaseModel):
    email: str