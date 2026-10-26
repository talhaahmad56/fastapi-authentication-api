from datetime import datetime , timedelta , timezone
from fastapi.security import OAuth2PasswordBearer
from config import settings
from jose import jwt , JWTError
from passlib.context import CryptContext
from fastapi import HTTPException , Depends
from database import get_db
from sqlalchemy.orm import Session
from models import User

secret_key = settings.secret_key
alg = settings.algorithm
EXPIRE_TIME_TOKEN_MINUTES = 60

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = "auto"
)

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password : str , hashed_password : str):
    return pwd_context.verify(plain_password , hashed_password)

oauth_schema = OAuth2PasswordBearer(tokenUrl = "login")

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME_TOKEN_MINUTES)
    to_encode.update({
        "exp" : expire
    })

    token = jwt.encode(to_encode , secret_key , algorithm=alg)


    return token

def verify_token(token :str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token , secret_key , algorithms=[alg])
        return payload
    except JWTError:
        raise HTTPException(status_code=401 , detail="Unauthorized")

    

def get_current_user(payload: dict = Depends(verify_token),db: Session = Depends(get_db)):
    user_id = payload.get("sub")

    if not user_id or not user_id.isdigit():
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
