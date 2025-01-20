from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from pydantic import BaseModel
from models.user import User
from database import get_db_connection
import logging
from controllers.user import register, login
from utils import get_token_from_cookie

logger = logging.getLogger(__name__)

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    name: str
    last_name: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def post_register(variables: RegisterRequest, response: Response, db_connection=Depends(get_db_connection)):
    """Registrar un nuevo usuario y devolver el token"""
    try:
        user = User(email=variables.email, name=variables.name, last_name=variables.last_name, password=variables.password)
        register(user, db_connection)
        access_token = login(email=variables.email, password=variables.password, db_connection=db_connection)
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Strict')
        return {"message": "Register succesful", "token": access_token}
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def post_login(body: LoginRequest, response: Response, db_connection=Depends(get_db_connection)):
    try:
        access_token = login(email=body.email, password=body.password, db_connection=db_connection)
        if access_token:
            response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Strict')
            return {"message": "Login successful", "token": access_token}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
def post_logout(response: Response, request: Request, token: str = Depends(get_token_from_cookie)):
    try:
        response.set_cookie(key="access_token", max_age=-1, httponly=True, secure=True, samesite="Strict")

        return {"message": "Logout succesful"}

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
