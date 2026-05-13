from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db, get_connection

app = FastAPI()

init_db()

#  MUST BE HERE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Story(BaseModel):
    title: str
    content: str

@app.get("/")
def home():
    return {"message": "backend is Alive"}

@app.post("/stories")
def create_story(story: Story):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "Insert into stories (title, content) VALUES (?, ?)",
        (story.title, story.content)
    )

    conn.commit()
    conn.close()

@app.get("/stories")
def get_stories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, content FROM stories")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": r[0], "title": r[1], "content": r[2]}
        for r in rows 
    ]

@app.delete("/stories/{story_id}")
def delete_story(story_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stories WHERE id = ?", (story_id,))
    conn.commit()
    conn.close()

    return {"message": "Deleted"}