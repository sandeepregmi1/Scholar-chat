# /home/sandeep/Projects/ScholarChat /app/core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

from fastapi import HTTPException, status



# PASSWORD SECURITY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ACCESS TOKEN

def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()

    if "sub" not in to_encode:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Token must include 'sub'")
    
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "type": "access",
        "role": data.get("role") 
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# REFRESH TOKEN

def create_refresh_token(data: dict):

    to_encode = data.copy()

    if "sub" not in to_encode:
        raise ValueError("Token must include 'sub'")

    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "role": data.get("role")
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# VERIFY TOKEN

def verify_token(token: str, credentials_exception, token_type: str = "access"):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != token_type:
            raise credentials_exception

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        return {"email": email,   "type": payload.get("type"), "role": payload.get("role")  }

    except JWTError:
        raise credentials_exception