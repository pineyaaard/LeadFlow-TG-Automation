cat <<EOF > scheduler.py
from apscheduler.schedulers.asyncio import AsyncioScheduler
from aiogram import Bot
import aiosqlite
import db
import config
from datetime import datetime

scheduler = AsyncioScheduler()

async def send_reminders(bot: Bot):
    async with aiosqlite.connect(db.DB_NAME) as database:
        # Ищем тех, кто зашел более 1 минуты назад (для теста), но статус еще 'started_bot'
        query = """
            SELECT user_id FROM users 
            WHERE status = 'started_bot' 
            AND created_at <= datetime('now', '-1 minute')
        """
        async with database.execute(query) as cursor:
            users_to_remind = await cursor.fetchall()

        for (user_id,) in users_to_remind:
            try:
                await bot.send_message(
                    user_id, 
                    "🔔 Эй! Твой AI-гайд скучает. Подпишись на канал, чтобы забрать его!"
                )
                await db.update_status(user_id, 'reminder_sent')
                print(f"Отправлено напоминание юзеру {user_id}")
            except Exception as e:
                print(f"Ошибка отправки напоминания {user_id}: {e}")

def setup_scheduler(bot: Bot):
    # Проверка каждые 30 секунд (для теста, потом поставишь 10 минут)
    scheduler.add_job(send_reminders, "interval", seconds=30, args=[bot])
    scheduler.start()
EOF