from services.sms import send_sms
from db.psql_connector import DB, default_config
from type_def.auth import User
from type_def.tenent import Tenent
from type_def.common import Success, Error
from type_def.configs import SMPP


def send_sms_marketing(
    user: User,
    tenent: Tenent,
    send_to: str,
    msg: str,
):
    db = DB(default_config())
    body = str(msg)
    if len(body) > 160:
        return Error("Message is too long. Max 160 characters", 1000, 400)
    if not tenent.disabled and not tenent.verified:
        try:
            send_sms(
                str("SLT"),
                str(send_to),
                msg,
                smpp_config=SMPP(),
            )
            db.exec(
                "INSERT INTO marketing_logs (tenent_id, user_id, type, sent_to, body) VALUES (%s, %s, %s, %s, %s)",
                (tenent.id, user.id, "sms", send_to, body),
            )
            db.commit()
            return Success(
                "SMS sent successfully",
                200,
                None,
            )
        except Exception as e:
            return Error("Failed to send SMS. Reason: " + str(e), 1000, 400)
    else:
        reason = None
        if tenent.disabled:
            reason = "Tenent is disabled. Please contact administrator for activation"
        elif not tenent.verified:
            reason = (
                "Tenent is not verified. Please contact administrator for verification"
            )
        return Error(reason, 1000, 400)
