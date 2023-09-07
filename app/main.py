from fastapi import Depends, FastAPI, status, Request, Response

# Auth
from auth.api_key_handler import APIKeyManager
from auth.auth_bearer import JWTBearer, APIKey
from auth.auth_handler import AuthHandler, decode_key
from auth.auth_handler import (
    AuthHandler,
    get_current_active_user_jwt as get_current_active_user,
    get_current_active_user_api_key,
    decode_key,
)

# Types
from type_def.auth import (
    APIKeyReq,
    ChangePasswordModel,
    LoginUserModel,
    RegisterUserModel,
    User,
)
from type_def.common import Error, Success
from type_def.tenent import Tenent
from type_def.requests import SMSOTPSendRq, EmailOTPSendRq
from type_def.keys import DecodedKey


# API
from api.v1.sms.send_otp import send_sms_otp
from api.v1.email.send_otp import send_email_otp


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to OTP service"}


#########################
#      AUTH ROUTES     #
########################
@app.post("/auth/login", tags=["auth"])
async def login(login_model: LoginUserModel):
    res = await AuthHandler().login(login_model)
    return res.response()


@app.post("/auth/register", tags=["auth"])
async def register(register_model: RegisterUserModel):
    res = await AuthHandler().register(register_model)
    return res.response()


@app.get("/auth/users/me", tags=["auth"], dependencies=[Depends(JWTBearer())])
async def read_users_me(
    response: Response,
    current_user: User = Depends(get_current_active_user),
):
    return (
        Success("Successfull", status.HTTP_200_OK, current_user.pub()).resp(response)
        if current_user
        else Error("User not found", 4004, 404).resp(response)
    )


@app.get("/auth/logout", tags=["auth"], dependencies=[Depends(JWTBearer())])
async def logout(current_user: User = Depends(get_current_active_user)):
    return {"msg": "Logout"}


@app.put(
    "/auth/change-password/{user_id}",
    tags=["auth"],
    dependencies=[Depends(JWTBearer())],
)
async def change_password(
    user_id: str,
    body: ChangePasswordModel,
    current_user: User = Depends(get_current_active_user),
):
    return (
        await AuthHandler(current_user).change_password(
            user_id, body.new_password, body.curr_password
        )
    ).response()


@app.get("/auth/delete/{user_id}", dependencies=[Depends(JWTBearer())])
async def delete_user(
    response: Response,
    user_id: str,
    current_user: User | None = Depends(get_current_active_user),
):
    return (
        Success("User deleted successfully", status.HTTP_200_OK, {}).resp(response)
        if AuthHandler(current_user).delete_user(user_id)
        else Error(
            "Something went wrong, while deleting user",
            4005,
            status.HTTP_400_BAD_REQUEST,
        ).resp(response)
    )


@app.post("/auth/token/api/new", tags=["auth"], dependencies=[Depends(JWTBearer)])
async def new_api_token(
    response: Response, body: APIKeyReq, user: User = Depends(get_current_active_user)
):
    try:
        return APIKeyManager(user).issue_new(body).resp(response)
    except Exception as e:
        return Error("Error Occured: " + str(e), 4000, 400).resp(response)


@app.post("/auth/token/api/check/{api_key}", tags=["auth"])
async def check_api_token(api_key: str, scope: str = None):
    origin = None
    valid = APIKeyManager().safe_check(api_key, scope=scope, origin=origin)
    if valid:
        return Success("Validation passed", 200, {})
    return Error("Validation failed", 401, 4001)


@app.delete(
    "/auth/token/api/delete/{api_key}", tags=["auth"], dependencies=[Depends(JWTBearer)]
)
async def delete_api_token(api_key: str):
    return {"msg": "Delete API Token"}


@app.get("/auth/token/api/list", tags=["auth"], dependencies=[Depends(JWTBearer)])
async def list_api_token(
    response: Response, user: User = Depends(get_current_active_user)
):
    return APIKeyManager(user).get_my_token_list().resp(response)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

#  decoded_key: DecodedKey=Depends(decode_key)
# dependencies=[Depends(APIKey())]
@app.post("/api/v1/sms/send-otp")
def api_send_sms_otp(response: Response, body: SMSOTPSendRq):
    # print(decode_key)
    user = User(
        id="65de47e9-dbf1-47b3-8a11-d9b0f0014cd7",
        first_name="Navindu",
        last_name="Dananga",
        password="test",
        email="email@gmail.com",
    )
    tenent = Tenent(
        id="123",
        name='OTP Service Test',
        owner=user
    )
    return send_sms_otp(user=user, tenent=tenent, send_to=body.mobile).resp(response)


@app.post("/api/v1/email/send-otp")
def api_send_email_otp(response: Response, body: EmailOTPSendRq):
    user = User(
        id="65de47e9-dbf1-47b3-8a11-d9b0f0014cd7",
        first_name="Navindu",
        last_name="Dananga",
        password="test",
        email="email@gmail.com",
    )
    tenent = Tenent(
        id="123",
        name='OTP Service Test',
        owner=user
    )
    return send_email_otp(user=user, tenent=tenent, send_to=body.email).resp(response)



@app.get("/health/db")
def test_db():
    from db.psql_connector import DB, default_config

    db = DB(default_config())
    try:
        if db.get_conn():
            return {"msg": "Database connection succeed"}
        else:
            return {"msg": "Database connection failed"}
    except:
        return {"msg": "Database connection failed"}


@app.get("/health/cache")
def test_cache():
    from db.redis_connector import redis_connection

    cache = redis_connection
    try:
        if cache.ping():
            return {"msg": "Cache connection succeed"}
        else:
            return {"msg": "Cache connection failed"}
    except:
        return {"msg": "Cache connection failed"}
