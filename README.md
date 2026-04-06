# LeadFlow TG Automation 🚀

High-performance Telegram Lead Capture Bot built with **aiogram 3.x**. This bot is designed to automate marketing funnels by verifying channel subscriptions and tracking lead sources with deep precision.

## 🌟 Key Features
* **Deep Link Analytics:** Track exact traffic sources (YouTube, Instagram, TikTok) using unique start parameters.
* **Subscription Guard:** Mandatory Telegram channel join verification before unlocking content.
* **Automated Lead Capture:** Saves user data and interaction status into a local SQLite database.
* **Digital Asset Delivery:** Instant delivery of PDF guides or exclusive links upon successful verification.
* **Multi-Admin Dashboard:** Dedicated `/admin` command for real-time statistics accessible by authorized personnel.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** [Aiogram 3.x](https://github.com/aiogram/aiogram)
* **Database:** Aiosqlite (Asynchronous SQLite)
* **Environment:** Python-dotenv for secure configuration

## 🚀 Quick Setup
1. **Clone the repo:**
   \`\`\`bash
   git clone https://github.com/pineyaaard/LeadFlow-TG-Automation.git
   cd LeadFlow-TG-Automation
   \`\`\`
2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. **Configure Environment:**
   Create a \`.env\` file based on \`.env.example\` and fill in your Bot Token, Admin IDs, and Channel details.
4. **Run the bot:**
   \`\`\`bash
   python main.py
   \`\`\`
