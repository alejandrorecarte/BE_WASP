import os

import bcrypt


def hash(value):
    if value:
        salt = os.getenv("SALT")
        hashed = bcrypt.hashpw(value.encode("utf-8"), salt.encode("utf-8")).decode("utf-8")
        return hashed
    return None


def verify_hash(value, hashed_value):
    return bcrypt.checkpw(value.encode("utf-8"), hashed_value.encode("utf-8"))
