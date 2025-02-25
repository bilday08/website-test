import bcrypt
import jwt
# import logging
from datetime import datetime, timedelta


SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # logging.debug(f"Plain Password: {plain_password}")
    # logging.debug(f"Hashed Password: {hashed_password}")
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_jwt(email: str) -> str:
    payload = {"sub": email, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
