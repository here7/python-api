from fastapi import FastAPI
from routers import books, users

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(books.router)

@app.get("/")
async def hello():
    return {"Hello":"world"}