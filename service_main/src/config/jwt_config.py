from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException

from src.config.settings_for_main import settings


def create_jwt_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    payload.update({"exp": expire})

    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
