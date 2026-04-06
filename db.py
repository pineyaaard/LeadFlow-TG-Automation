cat << 'EOF' > db.py
import aiosqlite

DB_NAME = 'bot_database.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                source TEXT,
                guide_topic TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_user(user_id, source, topic):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO users (user_id, source, guide_topic, status) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET guide_topic = excluded.guide_topic
        ''', (user_id, source, topic, 'pending'))
        await db.commit()

async def mark_as_subscribed(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE users SET status = ? WHERE user_id = ?', ('subscribed_and_received', user_id))
        await db.commit()
EOF