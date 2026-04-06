cat <<EOF > config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Чистим данные от случайных пробелов и мусора
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()
CHANNEL_URL = os.getenv("CHANNEL_URL", "").strip()

# Проверяем ID админа: если не число - будет 0
admin_raw = os.getenv("ADMIN_ID", "0").strip()
try:
    ADMIN_ID = int(admin_raw)
except:
    ADMIN_ID = 0
EOF