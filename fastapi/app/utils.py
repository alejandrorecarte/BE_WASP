import bcrypt
import jwt
import os
from fastapi import HTTPException, status, Request
from datetime import datetime, timedelta, timezone

def hash(value):
    if value:
        hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

def verify_hash(value, stored_hash):
    return bcrypt.checkpw(value.encode('utf-8'), stored_hash.encode('utf-8'))

def get_token_from_cookie(request: Request):
    """
    Esta función extrae el token de la cookie 'access_token'.
    Si no se encuentra o es inválido, lanza una excepción HTTP.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found"
        )
    return verify_token(access_token)

def verify_token(token: str) -> dict:
    """
    Verifica la validez del token, comprueba su expiración y decodifica el payload.
    Si el token es inválido o ha expirado, lanza una excepción HTTP.
    """
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp).replace(tzinfo=timezone.utc)
        current_datetime = datetime.now(timezone.utc)
        if current_datetime > exp_datetime:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")
    
def create_token(email: str):
    
        expiration_time = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("EXPIRATION_MINUTES")))
        payload = {
            "user_email": email,
            "exp": expiration_time
        }
        return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")