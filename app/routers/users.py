from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#app = FastAPI()
router = APIRouter()

# Class User --> BaseModel allows to creating an Entity. If not, the app would say that User() class needs parameters
class User(BaseModel):
    id: int
    name: str
    lastname: str
    age: int
    gender: str


# simulating DB objects
users_list = [User(id=1, name="Dani", lastname="Heredia", age=34, gender="male"),
            User(id=2, name="Juan Francisco", lastname="Gracia", age=40, gender="male"),              
            User(id=3, name="Marisa", lastname="López", age=25, gender="Female")]


# GET all users using BaseModel
@router.get("/users", status_code=200)
async def users():
    return users_list


# Path
@router.get("/user/{id}", status_code=200)
async def user(id: int):
    return search_user(id)
    

# Query-Param
@router.get("/user/", status_code=200)
async def user(id: int):
    return search_user(id)


@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="error: User already exists")
    else:
        users_list.append(user)
        return user


@router.put("/user/", status_code=200)
async def user(user: User):
    user_found = False

    for index, item in enumerate(users_list):
        if item.id == user.id:
            users_list[index] = user
            user_found = True

    if not user_found:
        raise HTTPException(status_code=404, detail="error: user wasn't found")
    

@router.delete("/user/{id}", status_code=200)
async def user(id: int):
    user_found = False

    for index, item in enumerate(users_list):
        if item.id == id:
            del users_list[index]
            user_found = True

    if not user_found:
        raise HTTPException(status_code=404, detail="error: user wasn't removed")


"""
GET specific user by PATH or QUERY_PARAM 

"""
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        raise HTTPException(status_code=404, detail="error: User doesn't exist")