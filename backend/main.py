from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

#  MUST BE HERE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stories = []

class Story(BaseModel):
    title: str
    content: str

@app.get("/")
def home():
    return {"message": "backend is Alive"}

@app.post("/stories")
def create_story(story: Story):
    stories.append(story)
    return {"message": "Story created", "story": story}

@app.get("/stories")
def get_stories():
    return stories