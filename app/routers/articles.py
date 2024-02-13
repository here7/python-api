from  fastapi import APIRouter, status

router = APIRouter(prefix="/articles", 
                   tags=["articles"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})

@router.get("/", status_code=status.HTTP_200_OK)
async def articles():
    return ["article1", "article2", "article3"]