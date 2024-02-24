import os
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_DURATION = 5

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

#simulating a DB
users_db = {
    "dani_1": {
        "username": "dani_1",
        "full_name": "Dani Heredia",
        "email": "dani@gmail.com",
        "disabled": False,
        "password": os.environ.get("USER1_PWD") 
    },
    "dani_2": {
        "username": "dani_2",
        "full_name": "Dani Heredia 2",
        "email": "dani2@gmail.com",
        "disabled": True,
        "password": os.environ.get("USER2_PWD") 
    }
}

# ** -> indicates that the BaseModel could have multiple params
# data with no passwd
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# with passwd
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Token Validation function
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Not valid Credentials",
                    headers={"WWW-Authenticate": "Bearer"}
                )
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)

# criterio de dependecia para /me (por eso es async tb)
async def current_user(user: User = Depends(auth_user)):  
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User disabled"
        ) 
    
    return user

# authentication implementation
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="error: user wasn't correct")
    
    user = search_user_db(form.username)

    # check if passwd in the form coincides with my user
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="error: password not correct")
    
    # jwt payload definition
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) }

    # if all good, return access_token (example with no encryption)
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user