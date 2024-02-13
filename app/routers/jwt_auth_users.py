from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

app = FastAPI()
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
        "password": "$2a$12$tk1Aa0hZXeVxOwfdHuFEEegTdPFILSCu8dtaad4j7RpLW589hYRiK" 
    },
    "dani_2": {
        "username": "dani_2",
        "full_name": "Dani Heredia 2",
        "email": "dani2@gmail.com",
        "disabled": True,
        "password": "$2a$12$nnye8Yp32y/Du2C4fKlcb.gJs3q03KO91rgqFYJIMXx8d93XQJA7e" 
    }
}


# with passwd
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


# authentication implementation
@app.post("/login")
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
    return {"access_token": access_token, "token_type": "bearer"}