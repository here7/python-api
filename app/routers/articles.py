import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # take environment variables from .env

router = APIRouter(prefix="/articles", 
                   tags=["articles"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})


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

    return create_article_chatgpt(topic)


def create_article_chatgpt(topic: str):
    # Setting OpenAI
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Context for ChatGpt
    messages = [{
                "role": "system",
                "content": "Please, I want you to write an article about the topic that the user will specify",
            }]
    
    # Topic defined by the User
    messages.append({
                        "role": "user",
                        "content": "Write an article about {topic}",
                    })
    try:
        response = client.chat.completions.create(
                messages,
                model="gpt-3.5-turbo",
            )
        return response.choices[0].message.content
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="error: error connection to chatGPT API")

def search_article(id: int):
    article = filter(lambda article: article.id == id, articles_list)
    
    try:
        return list(article)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error: Article doesn't exist")
