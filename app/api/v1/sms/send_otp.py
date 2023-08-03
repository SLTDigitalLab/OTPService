import services.sms as send_sms


def send_otp(
    user: User,
    tenent_id: str,
    mobile_number: str,
):
    otp = "1234"
    send_sms.send_sms("SLT", mobile_number, otp)
    return otp
