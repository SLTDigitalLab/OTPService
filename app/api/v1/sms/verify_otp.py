from libs.otp import otp_to_logs
from type_def.tenent import Tenent
from db.psql_connector import DB, default_config
from type_def.common import Success, Error
from datetime import datetime


def verify_sms_otp(
    tenent: Tenent, otp: str, mobile: str, client_secret: str
) -> Success | Error:
    db = DB(default_config())
    db.exec(
        "SELECT * FROM sms_otp WHERE tenent_id = %s AND sent_to = %s AND client_secret = %s LIMIT 1",
        (
            tenent.id,
            mobile,
            client_secret,
        ),
    )
    result = db.fetchone()
    if result:
        print(result)
        real_otp = result.get("otp")
        if real_otp and real_otp == str(otp):
            if result.get("validated"):
                return Error("OTP is already validated.", 1000, 400)
            elif (
                result.get("expired_at")
                and (
                    datetime.timestamp(result.get("expired_at"))
                    - datetime.timestamp(datetime.now())
                )
                <= 0
            ):
                otp_to_logs(db, result, "sms")
                db.exec(
                    "DELETE FROM sms_otp WHERE id = %s",
                    (result.get("id"),),
                )
                db.commit()
                return Error("OTP is expired.", 1000, 400)
            elif (
                result.get("tries") and result.get("tries") >= tenent.sms_otp_max_tries
            ):
                otp_to_logs(db, result, "sms")
                db.exec(
                    "DELETE FROM sms_otp WHERE id = %s",
                    (result.get("id"),),
                )
                db.commit()
                return Error("OTP is expired.", 1000, 400)
            else:
                log = otp_to_logs(db, result, "sms", True, datetime.now())
                db.exec(
                    "DELETE FROM sms_otp WHERE id = %s",
                    (result.get("id"),),
                )
                db.commit()
                return Success("OTP verified.", 200, {})
        else:
            db.exec(
                "UPDATE sms_otp SET tries = %s WHERE id = %s",
                (
                    result.get("tries") + 1,
                    result.get("id"),
                ),
            )
            db.commit()
            return Error("Invalid OTP.", 1000, 400)
    return Error(
        "Invalid request, please check client secret and the mobile number is valid",
        1000,
        400,
    )
