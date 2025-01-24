from type_def.common import Error, Success
from type_def.tenent import Tenent, TenentRq
from db.psql_connector import DB, default_config
from type_def.auth import User


class Tenents:
    db: DB = DB(default_config())
    user: User = None

    def __init__(self, user: User) -> None:
        self.user = user

    def new(self, t: TenentRq) -> Tenent | None:
        print(self.user)
        if self.user:
            self.db.exec(
                "INSERT INTO tenents (name, user_id, email_otp_size, email_otp_expired_in_s, sms_otp_size, sms_otp_expired_in_s, sms_otp_template, email_otp_template) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
                (
                    t.name,
                    self.user.id,
                    t.email_otp_size,
                    t.email_otp_expired_in_s,
                    t.sms_otp_size,
                    t.sms_otp_expired_in_s,
                    t.sms_otp_template,
                    t.email_otp_template,
                ),
            )
            self.db.commit()
            result = self.db.fetchone()
            if result:
                return Tenent(**result)
        return None

    def get(self, id) -> Tenent | None:
        self.db.exec(
            "SELECT * FROM tenents WHERE user_id = %s and id = %s LIMIT 1",
            (self.user.id, id),
        )
        result = self.db.fetchone()
        if result:
            return Tenent(**result)
        return None

    def list(self) -> list[Tenent] | None:
        print(self.user)
        self.db.exec("SELECT * FROM tenents WHERE user_id = %s", (self.user.id,))
        result = self.db.fetchall()
        if result:
            return [Tenent(**r) for r in result]
        return None

    def update():
        pass

    def delete(self, id: str, ):
        try:
            self.db.exec(
                "DELETE from tenents WHERE id = %s and user_id = %s",
                (id, self.user.id),
            )
            self.db.commit()
            return True
        except Exception as e:
            return False

    def rename(self, id: str, name: str) -> bool:
        try:
            self.db.exec(
                "UPDATE tenents SET name = %s, verified = %s WHERE id = %s and user_id = %s",
                (name, False, id, self.user.id),
            )
            self.db.commit()
            return True
        except Exception as e:
            return False

    def verify(self):
        self.db.exec(
            "UPDATE tenents SET verified = %s WHERE user_id = %s", (True, self.user.id, )
        )
        self.db.commit()

    def disable(self):
        self.db.exec(
            "UPDATE tenents SET disabled = %s WHERE user_id = %s", (True, self.user.id, )
        )
        self.db.commit()


class TenentsAdmin:
    def __init__(user: User) -> None:
        pass

    def verify(self):
        if self.user.is_admin:
            self.db.exec(
                "UPDATE tenents SET verified = %s WHERE user_id = %s",
                (True, self.user.id),
            )
            self.db.commit()
            return True
        return False

    def disable():
        pass
