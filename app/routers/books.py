from  fastapi import APIRouter

router = APIRouter(prefix="/books", 
                   tags=["books"],
                   responses={404: {"message": "Not Found"}})

@router.get("/", status_code=200)
async def books():
    return ["Book1", "Book2", "Book3"]