from datetime import datetime
from fastapi import Response


class Base:
    success: bool
    msg: str
    status_code: int
    error_code: int | None
    result: dict | None
    gen_at: datetime

    def __init__(
        self,
        success: bool,
        msg: str,
        status_code: int,
        error_code: int | None,
        result: dict | None,
    ):
        self.success = success
        self.msg = msg
        self.status_code = status_code
        self.error_code = error_code
        self.result = result
        self.gen_at = datetime.now()

    def resp_code(self):
        return self.status_code

    def resp(self, response: Response):
        response.status_code = self.resp_code()
        return {
            "success": self.success,
            "msg": self.msg,
            "error_code": self.error_code,
            "result": self.result,
            "gen_at": self.gen_at,
        }


class Error(Base):
    def __init__(self, error: str, error_code: int, status_code: int):
        super().__init__(False, error, status_code, error_code, None)


class Success(Base):
    def __init__(self, msg: str, status_code: int, result: dict):
        super().__init__(True, msg, status_code, None, result)
