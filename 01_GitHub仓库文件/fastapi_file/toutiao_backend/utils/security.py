import bcrypt


# 密码加密
def get_hash_password(password: str):
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("密码不能超过72字节")

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


# 密码校验
def verify_password(password: str, hashed_password: str):
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        return False

    #密码匹配返回True   密码不匹配返回False
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
