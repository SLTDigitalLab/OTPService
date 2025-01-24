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
from type_def.tenent import Tenent, TenentRq, TenentRenameRq
from type_def.requests import (
    SMSOTPSendRq,
    EmailOTPSendRq,
    SMSOTPVerifyRq,
    EmailOTPVerifyRq,
    SMSMarketingSendRq,
    EmailMarketingSendRq,
)
from type_def.keys import DecodedKey


# API
from api.v1.sms.send_otp import send_sms_otp
from api.v1.sms.verify_otp import verify_sms_otp
from api.v1.sms.sms_marketing import send_sms_marketing

from api.v1.email.send_otp import send_email_otp
from api.v1.email.verify_otp import verify_email_otp
from api.v1.email.email_marketing import send_email_marketing

from api.v1.management.tenent import TenentAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# @app.get("/auth/logout", tags=["auth"], dependencies=[Depends(JWTBearer())])
# async def logout(current_user: User = Depends(get_current_active_user)):
#     return {"msg": "Logout"}


@app.put(
    "/auth/change-password/{user_id}",
    tags=["auth"],
    dependencies=[Depends(JWTBearer())],
)
async def change_password(
    body: ChangePasswordModel,
    user_id: str | None = None,
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
    current_user: User = Depends(get_current_active_user),
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
        return APIKeyManager(body.tenent, user).issue_new(body).resp(response)
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
    print("User")
    print(user)
    return APIKeyManager(current_user=user).get_my_token_list().resp(response)


#########################
#       SMS ROUTES     #
########################
@app.post("/api/v1/sms/send-otp", tags=["sms"], dependencies=[Depends(APIKey())])
def api_send_sms_otp(
    response: Response,
    body: SMSOTPSendRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return send_sms_otp(
        user=decoded_key.user, tenent=decoded_key.tenent, send_to=body.mobile
    ).resp(response)


@app.post("/api/v1/sms/verify-otp", tags=["sms"], dependencies=[Depends(APIKey())])
def api_verify_sms_otp(
    response: Response,
    body: SMSOTPVerifyRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return verify_sms_otp(
        decoded_key.tenent, body.otp, body.mobile, body.client_secret
    ).resp(response)


@app.post("/api/v1/sms/send-marketing", tags=["sms"], dependencies=[Depends(APIKey())])
def api_send_sms_otp(
    response: Response,
    body: SMSMarketingSendRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return send_sms_marketing(
        user=decoded_key.user,
        tenent=decoded_key.tenent,
        send_to=body.mobile,
        msg=body.msg,
    ).resp(response)


#########################
#      Email ROUTES    #
########################
@app.post("/api/v1/email/send-otp", tags=["email"], dependencies=[Depends(APIKey())])
def api_send_email_otp(
    response: Response,
    body: EmailOTPSendRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return send_email_otp(
        decoded_key.user, decoded_key.tenent, body.email
    ).resp(response)


@app.post("/api/v1/email/verify-otp", tags=["email"], dependencies=[Depends(APIKey())])
def api_verify_sms_otp(
    response: Response,
    body: EmailOTPVerifyRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return verify_sms_otp(
        decoded_key.tenent, body.otp, body.email, body.client_secret
    ).resp(response)


@app.post(
    "/api/v1/email/send-marketing", tags=["email"], dependencies=[Depends(APIKey())]
)
def api_send_email_marketing(
    response: Response,
    body: EmailMarketingSendRq,
    decoded_key: DecodedKey = Depends(decode_key),
):
    return send_email_marketing(
        decoded_key.user, decoded_key.tenent, body.email, body.msg
    ).resp(response)


#########################
#      TENENT ROUTES   #
########################
@app.post(
    "/api/v1/management/tenents/new",
    tags=["tenents"],
    dependencies=[Depends(JWTBearer)],
)
def new_tenent(
    response: Response, body: TenentRq, user: User = Depends(get_current_active_user)
):
    print(user)
    return TenentAPI(user).new(body).resp(response)


@app.get(
    "/api/v1/management/tenents/{id}",
    tags=["tenents"],
    dependencies=[Depends(JWTBearer)],
)
def get_tenent(
    response: Response, id: str, user: User = Depends(get_current_active_user)
):
    return TenentAPI(user).get(id).resp(response)


@app.get(
    "/api/v1/management/tenents", tags=["tenents"], dependencies=[Depends(JWTBearer)]
)
def list_tenent(response: Response, user: User = Depends(get_current_active_user)):
    return TenentAPI(user).list().resp(response)


@app.put(
    "/api/v1/management/tenents/{id}/rename",
    tags=["tenents"],
    dependencies=[Depends(JWTBearer)],
)
def rename_tenent(
    response: Response,
    id: str,
    body: TenentRenameRq,
    user: User = Depends(get_current_active_user),
):
    return TenentAPI(user).rename(id, body.name).resp(response)

@app.delete(
    "/api/v1/management/tenents/{id}",
    tags=["tenents"],
    dependencies=[Depends(JWTBearer)],
)
def delete_tenent(
    response: Response,
    id: str,
    user: User = Depends(get_current_active_user),
):
    return TenentAPI(user).delete(id).resp(response)


#########################
#      HEALTH ROUTES   #
########################
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
