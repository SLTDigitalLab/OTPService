from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from auth.jwt_handler import JWTHandler
from auth.api_key_handler import APIKeyManager


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            return None

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            jwt = JWTHandler()
            payload = jwt.decode(jwtoken)
            return True if payload else False
        except Exception as e:
            return False


class APIKey(APIKeyHeader):
    def __init__(self, auto_error: bool = False):
        super(APIKey, self).__init__(auto_error=auto_error, name="X-Api-Key")

    async def __call__(self, request: Request):
        key: str | None = await super(APIKey, self).__call__(request)
        if key:
            try:
                info = APIKeyManager().safe_check(key)
                return info
            except Exception as e:
                raise HTTPException(401, str(e))
        else:
            return HTTPException(401, "Invalid API key")
