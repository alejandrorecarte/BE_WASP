import bcrypt


def hash(value):
    if value:
        hashed = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed


def verify_hash(value, stored_hash):
    return bcrypt.checkpw(value.encode("utf-8"), stored_hash.encode("utf-8"))
