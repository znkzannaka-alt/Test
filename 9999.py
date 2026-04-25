from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import datetime

TOKEN = "8619655248:AAEKCgDE_tujEDNo5b5_pqVDVlCLDHRdU5M"
ADMIN_ID = 8590875587

user_keys = {}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    info = f"""
👤 Bot User

Name: {user.first_name}
Username: @{user.username}
User ID: {user.id}
Time: {datetime.datetime.now()}
"""

    # Only admin receives info
    await context.bot.send_message(chat_id=ADMIN_ID, text=info)

    keyboard = [[InlineKeyboardButton("🚀 Login", callback_data="start_btn")]]

    await update.message.reply_text(
        "Key ဖြင့် Login ဝင်ပါ ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "start_btn":
        await query.message.reply_text("🔑 Key ပို့ပေးပါ")

    elif data.startswith("accept_"):
        uid = int(data.split("_")[1])

        keyboard = [[InlineKeyboardButton("Enter", callback_data="enter")]]

        await context.bot.send_message(
            chat_id=uid,
            text="✅ Login ဝင်ခြင်းအောင်မြင်ပါသည်",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("reject_"):
        uid = int(data.split("_")[1])
        await context.bot.send_message(chat_id=uid, text="❌ Admin မှ မလက်ခံပါ")

    elif data == "Hack Item":
        await query.message.reply_text("🎉 99999 အောင်မြင်ပါသည်")

# ---------------- MESSAGE HANDLER ----------------
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # ---------------- ADMIN SEND MESSAGE ----------------
    if user.id == ADMIN_ID:
        try:
            if text[0].isdigit():
                parts = text.split(" ", 1)
                uid = int(parts[0])
                msg = parts[1]

                await context.bot.send_message(chat_id=uid, text=msg)
                await update.message.reply_text("✅ User ဆီပို့ပြီးပါပြီ")
                return
        except:
            await update.message.reply_text("❌ Format: 8590875587 Hello")
            return

    # ---------------- USER KEY ----------------
    user_keys[user.id] = text

    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    msg = f"""
🔑 Key Request

Name: {user.first_name}
Username: @{user.username}
User ID: {user.id}
Key: {text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=msg,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text("⏳ Loding.....")

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

app.run_polling()