import time
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = "MY_SUPER_SECRET"
JWT_ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token(username: str, expires_in: int = 3600) -> str:
    """
    Создаём JWT-токен, который истечёт через expires_in секунд.
    """
    payload = {"sub": username, "exp": int(time.time()) + expires_in}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Проверяем токен из заголовка Authorization: Bearer <token>.
    Возвращаем username (sub) при успешной проверке.
    """
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
