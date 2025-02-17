from datetime import datetime, timedelta, timezone
import os

from fastapi import HTTPException, status
import jwt
from api.users.databases.models import User

# Create JWT Access Token
def create(user: User):
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("EXPIRATION_MINUTES"))
    )
    payload = {"id": user.id, "user_email": user.email, "exp": expiration_time}
    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
        
# Verify JWT Access Token
def verify(token: str) -> dict:
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )