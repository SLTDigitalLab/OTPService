import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timezone, timedelta


class JWTHandler:
    def __init__(self, aud: str = "otp:web") -> None:
        pem_bytes = open("./auth/keys/key.pem", "rb").read()
        passphrase = b"otp-passwd"

        self.private_key = serialization.load_pem_private_key(
            pem_bytes, password=passphrase, backend=default_backend()
        )
        self.public_key = open("./auth/keys/key.pem.pub", "rb").read()
        self.aud = aud
        self.algorithm = "RS256"
        self.issuer = "otp-sys"

    def encode(
        self,
        payload: dict,
    ) -> str:
        #   “exp” (Expiration Time) Claim
        #   “nbf” (Not Before Time) Claim
        #   “iss” (Issuer) Claim
        #   “aud” (Audience) Claim
        #   “iat” (Issued At) Claim
        payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(days=90)
        payload["nbf"] = datetime.now(tz=timezone.utc) - timedelta(seconds=5)
        payload["iss"] = self.issuer
        payload["aud"] = self.aud
        payload["iat"] = datetime.now(tz=timezone.utc)
        encoded = jwt.encode(
            payload, self.private_key, self.algorithm, headers={"kid": "otp-service"}
        )
        return encoded

    def decode(self, token: str) -> dict | None:
        if token:
            try:
                decoded = jwt.decode(
                    token,
                    self.public_key,
                    self.algorithm,
                    audience=self.aud,
                    issuer=self.issuer,
                    options={"require": ["exp", "iss", "id"]},
                )
                return decoded
            except Exception as e:
                print(e)
                return None
        return None
