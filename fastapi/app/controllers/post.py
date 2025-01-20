from models.post import Post
from fastapi import HTTPException, status
from controllers.queries import create_post_query, update_post_query, delete_post_query, get_post_query, get_post_last_query ,get_last_id, get_post_last_pages_query, check_post_access_query, get_post_user_query, get_post_user_pages_query
from database import execute_query, execute
from models.user import User
from controllers.exceptions import ControlledException
import os

def check_post_access(user_email, post_id, db_connection):
    query = check_post_access_query()
    params = (post_id)
    
    results = execute_query(query, params, db_connection)
    
    if results:
        if user_email == results[0][0]:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access not granted for that document"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )
    
def post_formatter(post_nf) -> Post:
    is_sold = 0
    if post_nf[4] == 1:
        is_sold = 1
        
    post_timestamp = int(post_nf[3].timestamp())
    
    return Post(post_id=post_nf[0], title=post_nf[1], description=post_nf[2], post_timestamp=post_timestamp, is_sold=is_sold, user_email=post_nf[5])
    

def create_post(post: Post, db_connection) -> Post:

    query = create_post_query()
    params = (post.title, post.description, post.is_sold, post.user_email)
    
    execute(query, params, db_connection)
    
    query = get_last_id()
    params = ()
    post_id = execute_query(query, params, db_connection)[0][0]

    query = get_post_query()
    results = execute_query (query, post_id, db_connection)
    
    if results:
        post = post_formatter(results[0])
        return post
    else:
        raise ControlledException("Could not create the post into BBDD")
    
def update_post(post: Post, user_email: str, db_connection) -> Post:
    
    check_post_access(user_email, post.post_id, db_connection)
    
    query = update_post_query()
    params = (post.title, post.description, post.is_sold, post.post_id)
    
    execute(query, params, db_connection)
    
    return post

def delete_post(post_id: int, user_email: str, db_connection):
    # TODO: Eliminar los vehículos asociados en cascada
    check_post_access(user_email, post_id, db_connection)
    
    query = delete_post_query()
    params = (post_id)
    
    execute(query, params, db_connection)
    
def get_post(post_id: int, db_connection):
    
    query = get_post_query()
    
    result = execute_query(query, post_id, db_connection)
    
    return post_formatter(result[0])

def get_post_user(user_email: str, page: int, db_connection):
    page_size = int(os.getenv("PAGE_SIZE"))
    page = page * page_size
    
    query = get_post_user_query()
    params = (user_email, page_size, page)
    
    result = execute_query(query, params, db_connection)
    
    posts = []
    for post_nf in result:
        posts.append(post_formatter(post_nf))
        
    return posts

def get_post_user_pages(user_email:str,  db_connection) -> int:
    
    query = get_post_user_pages_query()
    
    result = execute_query(query, user_email, db_connection)
    
    return int(result[0][0] / int(os.getenv("PAGE_SIZE")))
    
def get_post_last(page: int, db_connection):
    page_size = int(os.getenv("PAGE_SIZE"))
    page = page * page_size
    
    query = get_post_last_query()
    params = (page_size, page)
    
    result = execute_query(query, params, db_connection)
    
    posts = []
    for post_nf in result:
        posts.append(post_formatter(post_nf))
        
    return posts

def get_post_last_pages(db_connection) -> int:
    query = get_post_last_pages_query()
    
    result = execute_query(query, None, db_connection)
    
    return int(result[0][0] / int(os.getenv("PAGE_SIZE")))