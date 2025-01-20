from pydantic import BaseModel, root_validator
from utils import hash

class User(BaseModel):
    email: str
    name: str
    last_name: str
    password: str
    hashed_password: str = None  # Este atributo será generado automáticamente

    # Usamos un root_validator para asegurarnos de que se pueda acceder al hash de la contraseña
    @root_validator(pre=True)
    def hash_password(cls, values):
        password = values.get('password')
        values["hashed_password"] = hash(password)
        return values
