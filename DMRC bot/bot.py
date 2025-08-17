from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Your Bot Info ---
BOT_TOKEN = "6599915520:AAGBgqojJvVmrk_ZFwJW8HUsVfzubDOLdAE"
ADMIN_CHAT_ID = 5377150697   # Your Telegram User ID

# Example DMRC stations (you can expand this list)
stations = ["Rajiv Chowk", "Kashmere Gate", "Dwarka", "Noida City Centre", "Huda City Centre"]

# Store user booking data temporarily
user_data = {}

# ---------- COMMAND HANDLERS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(st, callback_data=f"source_{st}")] for st in stations]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚇 Welcome to *DMRC Ticket Booking Bot*!\n\nPlease select your **Source Station**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Pay using UPI / GPay:\n`upi://pay?pa=lakshaydeepv-1@okaxis&pn=Lakshaydeep%20verma%20Serial%20-%2056&aid=uGICAgMCcvb-LLw`", parse_mode="Markdown")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    await update.message.reply_text(f"🆔 Your Chat ID is: `{user_id}`", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = (
        "/start - Book ticket 🎟\n"
        "/pay - UPI/GPay 💰\n"
        "/id - Get your chat ID 🆔\n"
        "/help - Show this help 📖"
    )
    await update.message.reply_text(commands)

# ---------- BUTTON HANDLER ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("source_"):
        source_station = query.data.replace("source_", "")
        user_data[user_id] = {"source": source_station}

        # Show destination options
        keyboard = [[InlineKeyboardButton(st, callback_data=f"dest_{st}")] for st in stations if st != source_station]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"✅ Source Station: *{source_station}*\n\nNow select your **Destination Station**:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data.startswith("dest_"):
        dest_station = query.data.replace("dest_", "")
        source_station = user_data[user_id]["source"]

        # Send details to user
        await query.edit_message_text(
            f"🎟 Ticket Booking Details:\n\n"
            f"➡️ Source: *{source_station}*\n"
            f"➡️ Destination: *{dest_station}*\n\n✅ Ticket Confirmed!",
            parse_mode="Markdown"
        )

        # Notify admin (you)
        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"📩 New Ticket Request:\nUser: {user_id}\nSource: {source_station}\nDestination: {dest_station}"
        )

# ---------- MAIN ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("help", help_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
