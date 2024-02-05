from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

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
@app.get("/users")
async def users():
    return users_list


# Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    

# Query-Param
@app.get("/user/")
async def user(id: int):
    return search_user(id)


"""
GET specific user by PATH or QUERY_PARAM 

"""
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    
    try:
        return list(user)[0]
    except:
        return {"error: User doesn't exist"}