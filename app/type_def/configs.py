from pydantic import BaseModel
import os
from dotenv import load_dotenv


load_dotenv()


class SMPP(BaseModel):
    host: str = os.environ.get("SMPP_HOST")
    port: str = os.environ.get("SMPP_PORT")
    sys_id: str | None = os.environ.get("SMPP_SYS_ID")
    password: str | None = os.environ.get("SMPP_PASSWORD")


class SMTP(BaseModel):
    ssl: bool = os.environ.get("SMTP_SSL")
    host: str = os.environ.get("SMTP_HOST")
    port: int = os.environ.get("SMTP_PORT")
    sender_email: str | None = os.environ.get("SMTP_SENDER_EMAIL")
    password: str | None = os.environ.get("SMTP_PASSWORD")
