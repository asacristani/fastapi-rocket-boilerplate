from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.settings import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password
    # return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(
        password=password_byte_enc,
        hashed_password=hashed_password.encode("utf-8"),
    )
    # return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expiration_delta: timedelta) -> str:
    expiration = datetime.utcnow() + expiration_delta
    data.update({"exp": expiration})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(username: str) -> str:
    return create_jwt_token(
        {"sub": username, "scopes": "access_token"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )


#  TODO: def create_refresh_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_admin(token: str = Depends(oauth2_scheme)) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="No autorizado")
        return username
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token expirado") from err
    except jwt.JWTError as err:
        raise HTTPException(status_code=401, detail="Token invalid") from err


def verify_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("scopes") == "refresh_token":
            return payload
        else:
            # Refresh token invalid
            return None
    except jwt.ExpiredSignatureError:
        # Refresh token expired
        return None
    except jwt.JWTError:
        # Refresh token invalid
        return None
