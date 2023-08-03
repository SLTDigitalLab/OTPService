from fastapi import FastAPI
from services.sms import send_sms
from services.email import send_mail

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to OTP service"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/v1/sms/send-otp")
def send_sms_otp():
    pass
