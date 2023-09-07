from pydantic import BaseModel
from type_def.auth import UserModel
from type_def.tenent import Tenent

class DecodedKey(BaseModel):
    user: UserModel
    tenent: Tenent
