import sqlite3

DB_NAME = "stories.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS stories")

        # create base table 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT,
            is_favorite INTEGER,
            tags TEXT
        )
    """)

    # safe migration blocks
    #prevents crashes if columns already exist

    try:
        cursor.execute("ALTER TABLE stories ADD COLUMN created_at TEXT DEFAULT (datetime('now'))")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE stories ADD COLUMN updated_at TEXT DEFAULT (datetime('now'))")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE stories ADD COLUMN is_favorite INTEGER DEFAULT 0")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE stories ADD COLUMN tags TEXT DEFAULT ''")
    except:
        pass


    conn.commit()
    conn.close()