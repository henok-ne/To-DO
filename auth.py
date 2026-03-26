from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET = "SUPERSECRET"
ALGO = "HS256"


def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    return jwt.encode(payload, SECRET, algorithm=ALGO)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return int(payload["sub"])
    except JWTError:
        return None
