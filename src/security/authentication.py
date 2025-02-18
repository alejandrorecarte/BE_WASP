import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request, status


def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )


def create_token(user_id: str, email: str):
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("EXPIRATION_MINUTES"))
    )
    payload = {"user_id": user_id, "user_email": email, "exp": expiration_time}
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
