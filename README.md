🚇 DMRC Ticket Booking Bot

A Telegram bot for booking Delhi Metro tickets, selecting source/destination stations, and paying via UPI/GPay.
Built using Python and the python-telegram-bot library.

✨ Features

/start → Select Source Station and Destination Station

/pay → Get a UPI/GPay link for payment

/id → Get your Telegram Chat ID

/help → Show all available commands

Admin receives ticket booking notifications automatically

📦 Requirements

Python 3.9+

python-telegram-bot==20.3

Install dependencies:

pip install python-telegram-bot==20.3

⚙️ Setup

Clone the repo:

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>


Edit bot.py and set your credentials:

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_CHAT_ID = 123456789  # Replace with your own Telegram User ID


Run the bot:

python bot.py

📸 Payment (UPI/GPay)

The bot sends a UPI payment link like this:

upi://pay?pa=lakshaydeepv-1@okaxis&pn=Lakshaydeep%20verma%20Serial%20-%2056


Replace it with your own UPI ID inside the /pay command if needed:

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Pay using UPI / GPay:\n"
        "`upi://pay?pa=YOUR_UPI_ID@bank&pn=YourName`",
        parse_mode="Markdown"
    )

💻 Commands
Command	Description
/start	Book ticket (choose Source & Destination)
/pay	Show UPI/GPay link
/id	Get your chat ID
/help	Show available commands
🔔 Admin Notifications

Whenever a user books a ticket, the bot sends a message to the admin with details:

📩 New Ticket Request:
User: <user_id>
Source: <station>
Destination: <station>

🌍 Hosting

Local testing:

python bot.py


Deploy online (for 24/7 uptime):

Use Render, Railway.app, or Heroku.

Push your repo → Connect to hosting → Add environment variable BOT_TOKEN.

📌 Example Flow

/start → User selects Rajiv Chowk as source

Bot asks for Destination

User selects Noida City Centre

Bot confirms ticket + notifies admin
