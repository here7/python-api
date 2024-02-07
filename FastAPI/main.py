from fastapi import FastAPI
from routers import users

app = FastAPI()

# Routers
app.include_router(users.router)

@app.get("/")
async def hello():
    return {"Hello":"world"}