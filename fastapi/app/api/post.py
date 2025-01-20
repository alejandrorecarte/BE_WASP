from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from models.user import User
from database import get_db_connection
import logging
from controllers.post import create_post, update_post, delete_post, get_post, get_post_last, get_post_last_pages, get_post_user, get_post_user_pages
from models.post import Post
from utils import get_token_from_cookie

logger = logging.getLogger(__name__)

router = APIRouter()

class CreatePostRequest(BaseModel):
    title: str
    description: str

@router.post("/create", status_code=status.HTTP_201_CREATED)
def post_create_post(body: CreatePostRequest, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    user_email = token["user_email"]
    try:
        post = Post(title = body.title, description = body.description, user_email = user_email)
        post = create_post(post, db_connection)
        return {"post": post.model_dump()}
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.post("/update", status_code=status.HTTP_200_OK)
def post_update_post(post: Post, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    user_email = token["user_email"]
    try:
        post = update_post(post, user_email, db_connection)
        return {"post": post.model_dump()}
    except HTTPException as error:
        logger.warning(str(error.detail))
        raise HTTPException(
            status_code=error.status_code,
            detail=error.detail
        )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    
class DeletePostRequest(BaseModel):
    post_id: str

@router.post("/delete", status_code=status.HTTP_200_OK)
def post_delete_post(body: DeletePostRequest, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    user_email = token["user_email"]
    try:
        delete_post(body.post_id, user_email, db_connection)
        return {}
    except HTTPException as error:
        logger.warning(str(error.detail))
        raise HTTPException(
            status_code=error.status_code,
            detail=error.detail
        )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
 
@router.get("/get", status_code=status.HTTP_200_OK)
def get_post_by_id(post_id: int, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    try:
        post = get_post(post_id, db_connection=db_connection)
        return {"post": post}
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error)
                )
        
@router.get("/user", status_code=status.HTTP_200_OK)
def get_user_post(user_email: str, page: int, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    try:
        posts = get_post_user(user_email, page, db_connection)
        posts_json = [post.model_dump() for post in posts]
        
        max_pages = get_post_user_pages(user_email, db_connection)
        return { "page": page, "max_pages": max_pages,"last_posts": posts_json }
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error)
                )
        
@router.get("/last", status_code=status.HTTP_200_OK)
def get_last_post(page: int, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    try:
        posts = get_post_last(page, db_connection)
        posts_json = [post.model_dump() for post in posts]
        
        max_pages = get_post_last_pages(db_connection)
        return {"page": page, "max_pages": max_pages, "last_posts": posts_json}
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error)
                )
