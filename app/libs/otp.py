import numpy as np

from db.psql_connector import DB


def gen_otp(size):
    rng = np.random.default_rng()
    return "".join([str(rng.integers(0, 10)) for _ in range(size)])


def otp_to_logs(
    db: DB,
    db_r,
    type,
    validated=False,
    validated_at=None,
):
    db.exec(
        "INSERT INTO otp_logs(tenent_id, user_id, type, sent_to, otp, otp_client_secret, otp_created_at, otp_expired_at, otp_validated, otp_validated_at, otp_tries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
        (
            db_r.get("tenent_id"),
            db_r.get("user_id"),
            type,
            db_r.get("sent_to"),
            db_r.get("otp"),
            db_r.get("client_secret"),
            db_r.get("created_at"),
            db_r.get("expired_at"),
            validated,
            validated_at,
            db_r.get("tries"),
        ),
    )
    db.commit()
    return db.fetchone()
