import uuid
from db.psql_connector import DB, default_config
from datetime import datetime
import bcrypt
from .jwt_handler import JWTHandler
from types_rae.auth import (
    AuthSuccess,
    AuthError,
    RegisterUserModel,
    LoginUserModel,
    User,
    UserModel,
)
from typing import Optional, Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from auth.api_key_handler import APIKeyManager
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash


class AuthHandler:
    def __init__(self, user: Union[User, None] = None):
        self.db = DB(default_config())
        self.user = user

    async def register(self, reg: RegisterUserModel) -> Union[AuthSuccess, AuthError]:
        try:
            password = reg.password.encode("utf-8")
            # enc_password = bcrypt.hashpw(password, bcrypt.gensalt())
            enc_password = PasswordHasher().hash(password)
            # check email already exists
            user_exist = await self.check_email_exist(reg.email)
            if user_exist:
                return AuthError("User is already exist. Please login")

            self.db.exec(
                "INSERT INTO users(id, first_name, last_name, email, password, tel, created_ts, updated_ts, last_login_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
                (
                    str(uuid.uuid4()),
                    reg.first_name,
                    reg.last_name,
                    reg.email,
                    enc_password,
                    reg.tel,
                    datetime.now(),
                    None,
                    None,
                ),
            )
            self.db.commit()
            result = self.db.fetchone()
            if result:
                return AuthSuccess("User registered successfully", User(**result).pub())
            return AuthError("User not created")
        except Exception as e:
            return AuthError(str(e))

    async def login(self, cred: LoginUserModel) -> Union[AuthSuccess, AuthError]:
        try:
            self.db.exec("SELECT * FROM users WHERE email = %s LIMIT 1", (cred.email,))
            result = self.db.fetchone()

            if result:
                if PasswordHasher().verify(result["password"], cred.password):
                    jwt_handler = JWTHandler(aud=f"rae:web")
                    token = jwt_handler.encode(
                        {
                            "id": result["id"],
                            "email": result["email"],
                        }
                    )
                    self.db.exec(
                        "UPDATE users SET last_login_ts = %s WHERE id = %s",
                        (datetime.now(), result["id"]),
                    )
                    return AuthSuccess(
                        "User logged in successfully",
                        {
                            "jwt": token,
                            "user": User(**result).pub(),
                            "gen_ts": datetime.now().timestamp(),
                        },
                    )
                return AuthError("Invalid Credentials")
            return AuthError("User not found. Please register")
        except VerifyMismatchError as e:
            return AuthError("Invalid Credentials")
        except Exception as e:
            return AuthError(f"{str(e)}")

    async def logout():
        pass

    async def get_user(self, user_id):
        pass

    async def update_user():
        pass

    async def delete_user(self, user_id: str):
        if self.user and (self.user.id == user_id or self.user.is_super_admin):
            self.db.exec("DELETE FROM users WHERE id = %s", (user_id,))
            return True
        return False

    async def get_all_users():
        pass

    async def reset_password():
        pass

    async def change_password(
        self, user_id, new_password, curr_password=None
    ) -> AuthSuccess | AuthError:
        try:
            if self.user and (self.user.id == user_id or self.user.is_super_admin):
                self.db.exec("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,))
                result = self.db.fetchone()
                if result:
                    if self.user.is_super_admin:
                        enc_password = PasswordHasher().hash(new_password)
                        self.db.exec(
                            "UPDATE users SET password = %s WHERE id = %s",
                            (enc_password, user_id),
                        )
                        return AuthSuccess("Password Changed Successfully", {})
                    else:
                        if PasswordHasher().verify(result["password"], curr_password):
                            enc_password = PasswordHasher().hash(new_password)
                            self.db.exec(
                                "UPDATE users SET password = %s WHERE id = %s",
                                (enc_password, user_id),
                            )
                            return AuthSuccess("Password Changed Successfully", {})
                return AuthError("User not found")
            return AuthError("No permission to change password")
        except VerifyMismatchError as e:
            return AuthError("Invalid Credentials")
        except InvalidHash as e:
            return AuthError("Invalid Credentials")
        except Exception as e:
            return AuthError(f"Error: {str(e)}")

    async def send_verification_email():
        pass

    async def verify_email():
        pass

    async def check_email_exist(self, email: str) -> bool:
        self.db.exec("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        if self.db.cursor.fetchone():
            return True
        return False


async def get_current_user_jwt(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
) -> Optional[dict]:
    jwt_handler = JWTHandler(aud=f"rae:web")
    user_dict = jwt_handler.decode(token)
    return user_dict


def get_current_active_user_jwt(
    current_user: Optional[dict] = Depends(get_current_user_jwt),
) -> Optional[User]:
    if current_user:
        db = DB(default_config())
        db.exec(
            "SELECT * FROM users WHERE id = %s LIMIT 1",
            (current_user["id"],),
        )
        result = db.fetchone()
        user = User(**result)
        if not user.disabled:
            return user
    return None


async def get_current_active_admin_user_jwt(
    current_user: User = Depends(get_current_user_jwt),
) -> Optional[User]:
    if not current_user.disabled and current_user.is_super_admin:
        return current_user
    return None


async def get_current_user_api_key(
    token: str = Depends(APIKeyHeader(name="X-Api-Key")),
) -> Optional[User]:
    result = APIKeyManager().safe_get(token)
    user = User(**result)
    return user


def get_current_active_user_api_key(
    current_user: Optional[dict] = Depends(get_current_user_api_key),
) -> Optional[User]:
    if not current_user.disabled:
        return current_user
    return None
