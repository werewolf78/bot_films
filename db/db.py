
import os
import aiosqlite
from config import ADMINS_IDS
DB_PATH = "data/users.db"

async def init_db():
    os.makedirs("data", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS known_users (
                user_id INTEGER PRIMARY KEY
            )
        """)
        await db.commit()

async def add_known_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO known_users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def is_known_user(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM known_users WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def remove_known_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM known_users WHERE user_id = ?", (user_id,))
        await db.commit()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
