import aiosqlite

DB_NAME = 'bot_database.db'


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                full_name TEXT,
                correct_answers INTEGER DEFAULT 0,
                incorrect_answers INTEGER DEFAULT 0,
                learned BOOLEAN DEFAULT 0,
                current_number INTEGER DEFAULT NULL,
                current_precision REAL DEFAULT NULL
            )
        ''')
        await db.commit()


async def add_user(telegram_id: int, full_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR IGNORE INTO users (telegram_id, full_name)
            VALUES (?, ?)
        ''', (telegram_id, full_name))
        await db.commit()


async def get_user(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            'SELECT * FROM users WHERE telegram_id = ?',(telegram_id,)
        ) as cursor:
            return await cursor.fetchone()


async def get_user_rank(telegram_id:int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row

        async with db.execute(
            '''SELECT COUNT(*) AS better
                FROM users
                WHERE correct_answers > (
                SELECT correct_answers FROM users WHERE telegram_id = ?)''',(telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row['better'] + 1 if row else None


async def get_total_users():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT COUNT(*) AS total FROM users') as cursor:
            row = await cursor.fetchone()
            return row['total'] if row else 0


async def get_top_users(limit: int=10):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            '''SELECT telegram_id, full_name, correct_answers
                FROM users
                ORDER BY correct_answers DESC, telegram_id ASC
                LIMIT ?''',(limit,)
        ) as cursor:
            return await cursor.fetchall()


async def set_learned(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE users SET learned = 1 WHERE telegram_id = ?',
            (telegram_id,)
        )
        await db.commit()


async def is_learned(telegram_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            'SELECT learned FROM users WHERE telegram_id = ?',(telegram_id,)
        ) as cursor: 
            row = await cursor.fetchone()
            return bool(row['learned']) if row else False


async def set_current_task(telegram_id: int, number: int, presicion: float):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE users SET current_number = ?, current_precision = ? WHERE telegram_id = ?',(number,presicion,telegram_id)
        )
        await db.commit()


async def get_current_task(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            'SELECT current_number, current_precision FROM users WHERE telegram_id = ?',(telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row and row['current_number'] is not None:
                return{
                    'number': row['current_number'],
                    'precision': row['current_precision'],
                }
            return None


async def crear_current_task(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE users SET current_number = NULL, current_precision = NULL WHERE telegram_id = ?',
            (telegram_id,)
        )
        await db.commit()


async def increment_stats(telegram_id: int, is_correct: bool):
    column = 'correct_answer' if is_correct else 'incorrect_answers'
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            f'UPDATE users SET {column} = {column} + 1 WHERE telegram_id = ?',(telegram_id,)
        )
        await db.commit()


