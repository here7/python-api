from  fastapi import APIRouter

router = APIRouter()

@router.get("/books", status_code=200)
async def books():
    return ["Book1", "Book2", "Book3"]