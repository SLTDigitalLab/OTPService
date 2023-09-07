from datetime import datetime, timedelta
from services.email import send_email
from db.psql_connector import DB, default_config
from libs.otp import gen_otp

from type_def.auth import User
from type_def.tenent import Tenent
from type_def.common import Success, Error
from type_def.configs import SMTP


def send_email_otp(
    user: User,
    tenent: Tenent,
    send_to: str,
):
    db = DB(default_config())
    otp = gen_otp(tenent.email_otp_size)
    created_at = datetime.now()
    expired_at = datetime.now() + timedelta(seconds=tenent.email_otp_expired_in_s)
    print(
        tenent.id,
        user.id,
        send_to,
        otp,
        created_at,
        expired_at,
        False,
        None,
        0,
    )
    db.exec(
        "INSERT INTO email_otp (tenent, user_id, sent_to, otp, created_at, expired_at, validated, validated_at, tries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING (id, tenent, user_id, sent_to, created_at, expired_at)",
        (
            tenent.id,
            user.id,
            send_to,
            otp,
            created_at,
            expired_at,
            False,
            None,
            0,
        ),
    )

    result = db.fetchone()
    print(result)

    try:
        send_email(
            str(tenent.name),
            str(send_to),
            tenent.sms_otp_template.format(
                otp=otp, created_at=created_at, expired_at=expired_at
            ),
            smtp_config=SMTP()
        )
        return Success(
            "Verification email sent",
            200,
            {"send_to": send_to, "created_at": created_at, "expired_at": expired_at},
        )
    except Exception as e:
        return Error("Failed to send verification email. Reason: " + str(e), 1000, 400)
