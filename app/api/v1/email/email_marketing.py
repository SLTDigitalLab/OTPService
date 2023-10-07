from services.email import send_email
from db.psql_connector import DB, default_config
from type_def.auth import User
from type_def.tenent import Tenent
from type_def.common import Success, Error
from type_def.configs import SMTP

def send_email_marketing(
    user: User,
    tenent: Tenent,
    send_to: str,
    msg: str,
):
    db = DB(default_config()) 
    body = str(msg)
    if (not tenent.disabled and tenent.verified):
        try:
            send_email(
                str("SLT"),
                str(send_to),
                msg,
                smtp_config=SMTP(),
            )
            db.exec(
                "INSERT INTO marketing_logs (tenent_id, user_id, type, sent_to, body) VALUES (%s, %s, %s, %s, %s)",
                (
                    tenent.id,
                    user.id,
                    "email",
                    send_to,
                    body
                ),
            )
            db.commit()
            return Success(
                "Email sent successfully",
                200,
                None,
            )
        except Exception as e:
            return Error("Failed to send email. Reason: " + str(e), 1000, 400)
    else:
        reason = None
        if (tenent.disabled):
            reason = "Tenent is disabled. Please contact administrator for activation"
        elif (not tenent.verified):
            reason = "Tenent is not verified. Please contact administrator for verification"
        return Error(reason, 1000, 400)