
import jwt
from fastapi import HTTPException, Request, Depends
from passlib.context import CryptContext
import secrets



JWT_SECRET = secrets.token_hex(16)
JWT_ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def sign(email):
    return jwt.encode({"email": email}, JWT_SECRET, algorithm=JWT_ALGORITHM)



def decode(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearar "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth.split(" ")[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)