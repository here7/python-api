import datetime
import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(prefix="/articles", 
                   tags=["articles"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})

# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
client_chatgpt = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)

class Article(BaseModel):
    id: int
    title: str
    content: str
    image: str

# simulating DB objects
articles_list = [
            Article(id=1, title="1on1 Meetings", content="Hello this article is about effective 1on1 meetings", image="../assets/images/python.jpg"),
            Article(id=2, title="Scaling your team up", content="Hello this article is about scaling your team Up", image="../assets/images/python.jpg")]


@router.get("/all", status_code=status.HTTP_200_OK)
async def articles():
    return articles_list

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def article(id: int):
    return search_article(id)


@router.get("/chatgpt/{topic}", status_code=status.HTTP_200_OK)
async def article(topic: str):
    if not topic:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Topic wasn't defined properly")

    article_chatgpt = Article()

    return create_article_chatgpt(topic)


def create_article_chatgpt(topic: str):
    pass
def search_article(id: int):
    article = filter(lambda article: article.id == id, articles_list)
    
    try:
        return list(article)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: Article doesn't exist")
    

