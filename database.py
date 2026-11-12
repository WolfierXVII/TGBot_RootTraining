import aiosqlite

DB_NAME = 'bot_database.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                full_name TEXT,
                tasks INTEGER,
                correct_answers INTEGER,
                uncorrect_answers INTEGER
            )
        ''')
        await db.commit()

async def add_user(telegram_id: int, full_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR IGNORE INTO users (telegram_id, full_name, tasks, correct_answers, uncorrect_answers)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, full_name, 0, 0, 0))
        await db.commit()
