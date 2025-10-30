from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECURITY_KEY = "387a1c28dadb9e87d81679a24d2dd033fcf300feac0a48c12db1ca7e90812e6d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 120


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(userpass, hashedpass):
    return pwd_context.verify(userpass, hashedpass)


def create_acces_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    data_copy.update({"exp": expire})
    return jwt.encode(data_copy, SECURITY_KEY, algorithm=ALGORITHM)

