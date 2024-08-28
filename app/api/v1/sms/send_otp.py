from datetime import datetime, timedelta
from services.sms import send_sms
from db.psql_connector import DB, default_config
from libs.otp import gen_otp
from uuid import uuid4

from type_def.auth import User
from type_def.tenent import Tenent
from type_def.common import Success, Error
from type_def.configs import SMPP

import os

def send_sms_otp(
    user: User,
    tenent: Tenent,
    send_to: str,
):
    db = DB(default_config())
    otp = gen_otp(tenent.sms_otp_size)
    created_at = datetime.now()
    expired_at = datetime.now() + timedelta(seconds=tenent.sms_otp_expired_in_s)
    secret = str(uuid4())
    # db.exec(
    #     "DELETE FROM sms_otp WHERE tenent_id = %s AND sent_to = %s",
    #     (
    #         tenent.id,
    #         otp,
    #     ),
    # )

    # db.commit()
    db.exec(
        "INSERT INTO sms_otp (tenent_id, user_id, sent_to, otp, client_secret, created_at, expired_at, validated, validated_at, tries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
    db.commit()
    try:
        send_sms(
            os.environ.get("SMPP_SOURCE_NAME"),
            str(send_to),
            tenent.sms_otp_template.format(
                otp=otp, created_at=created_at, expired_at=expired_at
            ),
            smpp_config=SMPP(),
        )
        return Success(
            "Verification SMS sent",
            200,
            {
                "send_to": send_to,
                "client_secret": secret,
                "created_at": created_at,
                "expired_at": expired_at,
            },
        )
    except Exception as e:
        return Error("Failed to send verification SMS. Reason: " + str(e), 1000, 400)
