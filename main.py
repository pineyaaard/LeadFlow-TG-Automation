cat << 'EOF' > main.py
import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import db, handlers

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    await db.init_db()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    print("🚀 БОТ ЗАПУЩЕН (Production Mode)")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
EOF