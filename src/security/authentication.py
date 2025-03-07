import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Request, Response, status

from app.controllers.exceptions.exceptions import ControlledException


def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise ControlledException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not found"
        )
    return verify_token(access_token)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        current_datetime = datetime.now(timezone.utc)
        if current_datetime > exp_datetime:
            raise ControlledException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise ControlledException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise ControlledException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise ControlledException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )


def create_token(response: Response, user_id: str):
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("EXPIRATION_MINUTES"))
    )
    payload = {"user_id": user_id, "exp": expiration_time}
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )
    return response


def invalidate_token(response: Response):
    response.set_cookie(
        key="access_token",
        max_age=-1,
        httponly=True,
        secure=True,
        samesite="Strict",
    )

    return response
