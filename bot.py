import logging 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- BOT CONFIG ---
BOT_TOKEN = "6599915520:AAGBgqojJvVmrk_ZFwJW8HUsVfzubDOLdAE"
ADMIN_CHAT_ID = 5377150697  # Replace with your Telegram user ID

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Metro Stations ---
stations = [
    "Adarsh Nagar", "AIIMS", "Akshardham", "Alpha 1 Greater Noida", "Anand Vihar",
    "Arjan Garh", "Arthala", "Ashok Park Main", "Ashram", "Azadpur",
    "Badarpur Border", "Badkal Mor", "Bahdurgarh City", "Barakhamba",
    "Bata Chowk", "Belvedere Towers (Rapid Metro)", "Bhikaji Cama Place",
    "Botanical Garden", "Brigadier Hoshiar Singh", "Central Secretariat",
    "Vishwavidyalaya", "Welcome", "Yamuna Bank"
]

# --- Store User Data ---
user_data = {}

# --- START Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to DMRC Metro Ticket Bot!\n\n"
        "🚇 To book a ticket:\n"
        "1️⃣ Enter the *first letter* of your Source Station.\n"
        "2️⃣ Select Source → Then Destination.\n\n"
        "💳 Use /pay to view QR for payment.\n"
        "ℹ️ Use /help to contact admin.\n\n"
        "🔗 Fare Calculator: https://www.nearbymetro.com/metro/1/farecalculation/Delhi",
        parse_mode="Markdown"
    )

# --- TEXT Handler (Search Stations) ---
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()

    # If selecting source
    if user_id not in user_data or "source" not in user_data[user_id]:
        matches = [st for st in stations if st.lower().startswith(text)]
        if matches:
            keyboard = [[InlineKeyboardButton(st, callback_data=f"source_{st}")] for st in matches]
            await update.message.reply_text("📍 Select your Source Station:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text("❌ No station found. Try again.")

    # If source selected, now destination
    elif "source" in user_data[user_id] and "destination" not in user_data[user_id]:
        matches = [st for st in stations if st.lower().startswith(text)]
        if matches:
            keyboard = [[InlineKeyboardButton(st, callback_data=f"dest_{st}")] for st in matches]
            await update.message.reply_text("📍 Select your Destination Station:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text("❌ No station found. Try again.")

# --- BUTTON Handler (Station Selection) ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("source_"):
        source_station = query.data.replace("source_", "")
        user_data[user_id] = {"source": source_station}
        await query.edit_message_text(
            f"✅ Source Station set: *{source_station}*\n\nNow enter the *first letter* of your Destination Station:",
            parse_mode="Markdown"
        )

    elif query.data.startswith("dest_"):
        dest_station = query.data.replace("dest_", "")
        source_station = user_data[user_id]["source"]
        user_data[user_id]["destination"] = dest_station

        await query.edit_message_text(
            f"🎟 Ticket Booking:\n\n➡️ Source: *{source_station}*\n➡️ Destination: *{dest_station}*\n\n✅ Ticket Confirmed!",
            parse_mode="Markdown"
        )

        # Notify Admin
        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"📩 New Ticket Request:\nUser: {user_id}\nSource: {source_station}\nDestination: {dest_station}"
        )

# --- PAY Command ---
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_url = "https://drive.google.com/uc?export=download&id=1V0I7gJB1g3AEClAfZxlwAn_-0L44lyH4"
    await update.message.reply_photo(
        photo=qr_url,
        caption="💳 Scan QR to pay via UPI/GPay.\n⚡ Confirm your ticket after payment!"
    )

# --- HELP Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💬 Chat with Admin", url=f"tg://user?id={ADMIN_CHAT_ID}")]]
    await update.message.reply_text(
        "/start - Book ticket 🎟\n"
        "/pay - UPI/GPay 💰\n"
        "/id - Get your chat ID 🆔\n"
        "/help - Show help 📖\n\n"
        "Need more help? Contact admin below 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Get User ID ---
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    await update.message.reply_text(f"🆔 Your Chat ID is: `{user_id}`", parse_mode="Markdown")

# --- Forward Messages to Admin ---
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if update.message.photo:  # Photo case
        await context.bot.send_photo(
            ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"📩 Message from {user.first_name} ({user.id})",
        )
    else:  # Text or other
        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"📩 Message from {user.first_name} ({user.id}):\n\n{update.message.text}"
        )

# --- Admin Reply to User ---
async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("🚫 Only admin can use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    user_id = int(context.args[0])
    reply_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=user_id, text=f"💬 Admin: {reply_text}")
        await update.message.reply_text("✅ Message sent to user.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send. Error: {e}")

# --- MAIN ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("reply", reply_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Forward ALL user messages (text/photo) to Admin
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    app.add_handler(MessageHandler(filters.PHOTO, forward_to_admin))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
