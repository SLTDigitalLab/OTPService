from type_def.tenent import Tenent
from db.psql_connector import DB, default_config
from type_def.common import Success, Error
from datetime import datetime

def verify_email_otp(tenent: Tenent, otp: str, mobile_number: str, client_secret: str) -> Success | Error:
    db = DB(default_config())
    db.exec(
        "SELECT * FROM email_otp WHERE tenent_id = %s AND sent_to = %s AND client_secret = %s LIMIT 1",
        (
            tenent.id,
            mobile_number,
            otp,
            client_secret,
        ),
    )
    result = db.fetchone()
    if result:
        real_otp = result.get('otp')
        if real_otp and real_otp == str(otp):
            if result.get('validated'):
                return Error("OTP is already validated.", 1000, 400)
            elif result.get('expired_at') and result.get('expired_at') < datetime.now():
                return Error("OTP is expired.", 1000, 400)
            elif result.get('tries') and result.get('tries') >= tenent.sms_otp_max_tries:
                return Error("OTP is expired.", 1000, 400)
            else:
                db.exec("UPDATE email_otp SET validated = %s, validated_at = %s WHERE id = %s",
                    (
                        True,
                        datetime.now(),
                        result.get('id'),
                    )
                )
                return Success("OTP verified.", 200, result)
        else:
            db.exec("UPDATE email_otp SET tries = %s WHERE id = %s",
                (
                    result.get('tries') + 1,
                    result.get('id'),
                )
            )
            return Error("Invalid OTP.", 1000, 400)
    return Error("Invalid request, please check client secret and the email is valid", 1000, 400)
