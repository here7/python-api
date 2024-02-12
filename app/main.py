from fastapi import FastAPI
from routers import books, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(books.router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def hello():
    return {"Hello":"world"}