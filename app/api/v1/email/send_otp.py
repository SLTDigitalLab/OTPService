from datetime import datetime, timedelta
from services.email import send_email
from db.psql_connector import DB, default_config
from libs.otp import gen_otp
from uuid import uuid4

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
    secret = str(uuid4())
    db.exec(
        "INSERT INTO email_otp (tenent_id, user_id, sent_to, otp, client_secret, created_at, expired_at, validated, validated_at, tries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING (id, tenent_id, user_id, sent_to, created_at, expired_at)",
        (
            tenent.id,
            user.id,
            send_to,
            otp,
            secret,
            created_at,
            expired_at,
            False,
            None,
            0,
        ),
    )

    # result = db.fetchone()
    try:
        send_email(
            str(tenent.name),
            str(send_to),
            tenent.email_otp_template.format(
                otp=otp, time_remaining=tenent.email_otp_expired_in_s, created_at=created_at, expired_at=expired_at
            ),
            smtp_config=SMTP()
        )
        return Success(
            "Verification email sent",
            200,
            {"send_to": send_to, "client_secret": secret, "created_at": created_at, "expired_at": expired_at},
        )
    except Exception as e:
        return Error("Failed to send verification email. Reason: " + str(e), 1000, 400)
