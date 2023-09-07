from redis.asyncio import Redis
from typing import Optional, Union
import secrets
from db.redis_connector import redis_connection
import json
from datetime import datetime, timedelta
from db.psql_connector import DB, default_config
from type_def.common import Success, Error
from type_def.auth import APIKeyReq
from type_def.keys import DecodedKey
from type_def.auth import User
from type_def.tenent import Tenent

class Scope:
    def __init__(self) -> None:
        pass

    def new():
        pass

    def check(scope: Optional[list]):
        pass


class APIKeyManager:
    def __init__(self, current_user: Optional[User] = None) -> None:
        self.redis: Redis = redis_connection
        self.user: User = current_user
        self.db = DB(default_config())

    def issue_new(self, body: APIKeyReq) -> Union[Success, Error]:
        try:
            api_key = f"otpapi_{secrets.token_urlsafe(16)}"
            now = datetime.now()
            exp = now + timedelta(days=body.expire_in)
            self.redis.set(
                api_key,
                json.dumps(
                    {
                        "user": self.user.id,
                        "name": body.name,
                        "expire_ts": datetime.timestamp(exp),
                        "allowed_origins": body.allowed_origins,
                        "scope": body.scope,
                        "created_ts": datetime.timestamp(now),
                    }
                ),
            )
            self.db.exec(
                "INSERT INTO api_keys (api_key, name, user_id, expire_ts, allowed_origins, scope, created_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    api_key,
                    body.name,
                    self.user.id,
                    exp,
                    body.allowed_origins,
                    body.scope,
                    now,
                ),
            )
            self.db.commit()
            return Success("API Key issued successfully", 200, {"X-Api-Key": api_key})
        except Exception as e:
            return Error(str(e), 4000, 400)

    def get_my_token_list(self) -> dict:
        if self.user:
            self.db.exec(
                "SELECT name, allowed_origins, scope, expire_ts, last_used, disabled, date_disabled, created_ts FROM api_keys WHERE user_id = %s",
                (self.user.id,),
            )
            result = self.db.fetchall()
            if result:
                return Success("Token fetching success", 200, result)
            return Error("No API Keys found", 4001, 404)
        return Error("User not found", 4002, 404)

    def safe_get(
        self, api_key: str, scope: Optional[str] = None, origin: Optional[str] = None
    ) -> DecodedKey:
        data = self.redis.get(api_key)
        if data:
            data = json.loads(data)
            if scope:
                if scope not in data["scope"]:
                    raise Exception("Scope not allowed")
            if origin:
                if origin not in data["allowed_origins"]:
                    raise Exception("Origin not allowed")
            if data["expire_ts"] < datetime.timestamp(datetime.now()):
                raise Exception("API Key expired")
            user_id = data.get("user", None)
            tenent_id = data.get("tenent", None)

            if user_id and tenent_id:
                self.db.exec("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,))
                user_result = self.db.fetchone()
                self.db.exec("SELECT * FROM tenents WHERE id = %s AND owner = %s LIMIT 1", (tenent_id, user_id))
                tenent_result = self.db.fetchone()
                if user_result and tenent_result:
                    return DecodedKey(tenent_id=Tenent(**tenent_id), user=User(**user_result))
                else:
                    raise Exception("User associated with API key not found" if not user_result else "Tenent associated with API key not found")
            else:
                raise Exception("User associated with API key not found" if not user_id else "Tenent associated with API key not found")
        raise Exception("API Key not found")

    def safe_check(
        self, api_key: str, scope: Optional[str] = None, origin: Optional[str] = None
    ) -> dict:
        res = self.safe_get(api_key, scope, origin)
        if res:
            return True
        return False

    def delete(self, api_key) -> bool:
        if self.user:
            data = self.redis.get(api_key)
            if data:
                data = json.loads(data)
                if data["user"] == self.user.id:
                    self.redis.delete(api_key)
                    return True
        return False
