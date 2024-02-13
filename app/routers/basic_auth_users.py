from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456" 
    },
    "dani_2": {
        "username": "dani_2",
        "full_name": "Dani Heredia 2",
        "email": "dani2@gmail.com",
        "disabled": True,
        "password": "654321" 
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



 # criterio de dependecia para /me (por eso es async tb)
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not valid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User disabled"
        ) 
    
    return user

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
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="error: password not correct")
    
    # if all good, return access_token (example with no encryption)
    return {"access_token": user.username, "token_type": "bearer"}
    

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user