import firebase_admin
from firebase_admin import credentials, db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import time
import os
import json

# =======================
# Bot Token
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"
# Firebase Initialization
FIREBASE_KEY_JSON = os.environ['FIREBASE_AUTH']
PORT = int(os.environ.get("PORT", 10000))
cred_dict = json.loads(FIREBASE_KEY_JSON)
cred = credentials.Certificate(cred_dict)  # path to Firebase key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jahanara-ef632-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# =======================
# Save chat_id to Firebase
def save_chat_id(chat_id):
    try:
        ref = db.reference('users')
        ref.child(str(chat_id)).set({
            'chat_id': chat_id,
            'status': 'active'
        })
        print(f"[+] Saved user {chat_id}")
    except Exception as e:
        print(f"[!] Firebase save error: {e}")

# =======================
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    save_chat_id(chat_id)

    keyboard = [[KeyboardButton("BUY OTP PRO")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 আসসালামু আলাইকুম \n✅ Sell4U তে আপনাকে স্বাগতম \n🟢 Join Official Channel For Updates",
        reply_markup=reply_markup
    )

# =======================
# Handle user text
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "BUY OTP PRO":
        keyboard = [
            [InlineKeyboardButton("🔗 GO TO BUY", url="https://t.me/sell4upay_bot")],
            [InlineKeyboardButton("👍 Normal Button", callback_data="normal_btn")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ OTP BOT Premium কিনতে নিতে দেওয়া বাটনে ক্লিক করুন",
            reply_markup=reply_markup
        )

# =======================
# Handle inline button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "normal_btn":
        await query.edit_message_text(text="👉 আপনি Normal Button চাপছেন!")

# =======================
# Broadcast with retry
def broadcast_message(app, text: str):
    ref = db.reference('users')
    users = ref.get()
    if not users:
        print("⚠️ No users found")
        return

    for uid, info in users.items():
        for attempt in range(3):  # try max 3 times
            try:
                app.bot.send_message(chat_id=int(uid), text=text)
                print(f"✅ Sent to {uid}")
                break
            except Exception as e:
                print(f"[!] Failed to send to {uid} (attempt {attempt+1}): {e}")
                time.sleep(2)  # wait before retry

# =======================
# /broadcast command (admin only)
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 6893452352  # replace with your Telegram ID
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /broadcast Your message here")
        return

    message = " ".join(context.args)
    broadcast_message(context.application, message)
    await update.message.reply_text("✅ Note sent!")

# =======================
# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("note", broadcast_command))

    print("🚀 Bot is running...")
    app.run_polling()

# =======================
if __name__ == "__main__":
    main()



