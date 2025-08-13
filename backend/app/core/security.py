import jwt, datetime
from app.core.config import settings

ALGO = "HS256"

def create_jwt(sub: int):
    payload = {"sub": sub, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGO)

def verify_jwt(token: str):
    data = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])
    return int(data["sub"])