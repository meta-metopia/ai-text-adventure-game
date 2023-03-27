import os
import secrets
from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasicCredentials, HTTPBasic
from jose import jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
security = HTTPBasic()


def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encode_jwt


def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(username, "utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(password, "utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme.")
            if not self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return self.decode_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verfity_jwt(Self, jwt_token: str):
        is_token_valid: bool = False
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

    def decode_jwt(self, jwt_token: str):
        payload = jwt.decode(jwt_token, SECRET_KEY)
        return payload
