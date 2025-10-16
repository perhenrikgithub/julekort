import sqlite3

DB_PATH = "cards.db"

def reset_card_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS cards")

def init_card_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id TEXT PRIMARY KEY,
                text TEXT,
                image_url TEXT,
                display_on_board BOOLEAN DEFAULT 0,
                sender TEXT,
                sender_email TEXT,
                recipient TEXT
            )
        """)

# def init_user_db():
#     with sqlite3.connect(DB_PATH) as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 email TEXT PRIMARY KEY,
#                 name TEXT
#             )
#         """)

reset_card_db()
init_card_db()
# init_user_db()