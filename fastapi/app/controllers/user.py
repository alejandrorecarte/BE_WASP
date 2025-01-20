from models.user import User
from controllers.queries import register_query, login_query
from controllers.exceptions import ControlledException
from database import execute, execute_query
from utils import verify_hash, create_token


def register(user: User, db_connection):

    query = register_query()
    params = (user.email, user.name, user.last_name, user.hashed_password)
    
    execute(query, params, db_connection)
    
def login(email: str, password: str, db_connection):
    params = (email)
    users = execute_query(login_query(), params, db_connection)
    
    if users:
        if verify_hash(password, users[0][3]):
            
            token = create_token(email)
            return token
        else:
            raise ControlledException("Credentials could not be verified")
    else:
        raise ControlledException("User not found")