# Hashing
from passlib.context import CryptContext

# hashing for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):

    hashed_password = pwd_context.hash(password)

    return hashed_password


def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)
