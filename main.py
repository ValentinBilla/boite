from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users")
async def get_users() -> list[str]:
    with open('users', 'r', encoding='utf-8') as f:
        return list(map(str.strip, f.readlines()))

class Retrieval(BaseModel):
    hour: datetime
    name: str

@app.post("/retrievals")
async def post_retrieval(name: str) -> None:
    with open('hours.csv', 'a', encoding='utf-8') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ', ' + name.strip() + '\n')

@app.get("/retrievals")
async def get_retrievals() -> list[Retrieval]:
    with open('hours.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    retrievals = list(map(line_to_retrieval, lines))
    retrievals.reverse()
    return retrievals

def line_to_retrieval(line: str) -> Retrieval:
    hour, name = line.split(', ')
    return Retrieval(
        hour=datetime.strptime(hour, '%Y-%m-%d %H:%M:%S'),
        name=name.strip()
    )
