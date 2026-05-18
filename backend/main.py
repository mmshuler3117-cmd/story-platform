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

from datetime import datetime, timezone

@app.post("/stories")
def create_story(story: Story):
    conn = get_connection()
    cursor = conn.cursor()

    

    now = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        """INSERT INTO stories (title, content, created_at, updated_at, is_favorite, tags) VALUES (?, ?, ?, ?, 0, '')""",
        (story.title, story.content, now, now)
    )

    conn.commit()

    story_id = cursor.lastrowid
    conn.close()

    return {
        "id": story_id,
        "title": story.title,
        "content": story.content,
        "created_at": now,
        "updated_at": now,
        "is_favorite": 0,
        "tags": ""


    }

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

@app.patch("/stories/{story_id}/favorite")
def toggle_favorite(story_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE stories
        SET is_favorite = CASE is_favorite
            WHEN 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
    """, (story_id,))

    conn.commit()

    # fetch new value
    cursor.execute("SELECT is_favorite FROM stories WHERE id = ?", (story_id,))
    row = cursor.fetchone()

    conn.close()

    return {
        "id": story_id,
        "is_favorite": bool(row[0])
    }