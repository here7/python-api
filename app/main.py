from fastapi import FastAPI
from routers import users, articles, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers to have all the APIs in the main APP
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(jwt_auth_users.router) # jwt is before included so, basic_auth is not used
app.include_router(basic_auth_users.router)

# static resources (images, etc.)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def hello():
    return {"Hello":"API :)"}