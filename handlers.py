cat << 'EOF' > handlers.py
import os
import db
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

GUIDES = {
    "default": "https://theaisignal.online/files/yourguide.pdf"
}

def get_onboarding_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=os.getenv("CHANNEL_URL"))],
        [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_sub")]
    ])

def get_success_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Открыть гайд", url=GUIDES["default"])],
        [InlineKeyboardButton(text="🔥 Получить ещё материалы", url=os.getenv("CHANNEL_URL"))]
    ])

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    args = command.args if command.args else "organic_none"
    source = args.split('_')[0] if '_' in args else args
    topic = args.split('_')[1] if '_' in args else "general"
    
    await db.add_user(message.from_user.id, source, topic)
    
    text = (
        "Привет. Ты пришёл за бесплатным AI-гайдом.\n\n"
        "Доступ к нему открывается после подписки на основной Telegram-канал. "
        "Подпишись и потом нажми кнопку проверки."
    )
    await message.answer(text, reply_markup=get_onboarding_kb())

@router.callback_query(F.data == "check_sub")
async def verify_subscription(cb: CallbackQuery, bot: Bot):
    try:
        user = await bot.get_chat_member(os.getenv("CHANNEL_ID"), cb.from_user.id)
        if user.status in ['member', 'creator', 'administrator']:
            await db.mark_as_subscribed(cb.from_user.id)
            await cb.message.answer(
                "Отлично, подписка подтверждена.\nВот твой бесплатный гайд. 👇",
                reply_markup=get_success_kb()
            )
            await cb.answer()
        else:
            await cb.message.answer(
                "Пока не вижу подписку на канал.\n"
                "Сначала подпишись, потом нажми «Проверить подписку», и я сразу выдам гайд.",
                reply_markup=get_onboarding_kb()
            )
            await cb.answer()
    except Exception as e:
        await cb.answer("Ошибка! Проверьте права бота в канале.", show_alert=True)

@router.message(F.text == "/admin")
async def admin_stats(message: Message):
    allowed_admins = os.getenv("ADMIN_IDS", "").split(",")
    if str(message.from_user.id) in [a.strip() for a in allowed_admins]:
        import aiosqlite
        async with aiosqlite.connect('bot_database.db') as conn:
            async with conn.execute('SELECT source, COUNT(*) FROM users GROUP BY source') as c:
                rows = await c.fetchall()
        
        stats = "📊 **Статистика по источникам:**\n"
        for row in rows:
            stats += f"- {row[0]}: {row[1]} чел.\n"
        await message.answer(stats, parse_mode="Markdown")
EOF