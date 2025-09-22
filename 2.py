import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.error import Forbidden
import firebase_admin
from firebase_admin import credentials, db
import json

# --- নতুন যুক্ত করা অংশ (Render Health Check সমাধানের জন্য) ---
from flask import Flask
import threading
# -----------------------------------------------------------

# --- আপনার তথ্য (অপরিবর্তিত) ---
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"
ADMIN_ID = "6893452352"
FIREBASE_URL = 'https://jahanara-ef632-default-rtdb.asia-southeast1.firebasedatabase.app/'

# --- Firebase সেটআপ (অপরিবর্তিত) ---
try:
    creds_json_str = os.environ.get('BOT_JSON')
    if creds_json_str is None:
        print("Environment variable not found. Trying local file...")
        cred = credentials.Certificate("serviceAccountKey.json")
    else:
        print("Initializing Firebase from environment variable...")
        creds_dict = json.loads(creds_json_str)
        cred = credentials.Certificate(creds_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_URL})
    
    ref = db.reference('/')
    print("✅ Firebase successfully initialized.")
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    ref = None

# --- নতুন যুক্ত করা অংশ (Flask ওয়েব সার্ভার) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    """Render-কে জানানোর জন্য যে সার্ভিসটি সচল আছে"""
    return "Bot is alive!", 200

def run_flask():
    """Flask সার্ভারটি একটি নির্দিষ্ট পোর্টে চালানোর জন্য ফাংশন"""
    # Render তার PORT এনভায়রনমেন্ট ভেরিয়েবলের মাধ্যমে পোর্ট নম্বর পাঠায়
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# ----------------------------------------------------

# লগিং কনফিগার করা হচ্ছে (অপরিবর্তিত)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# /start কমান্ডের জন্য ফাংশন (অপরিবর্তিত)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    chat_id = update.effective_chat.id
    try:
        users_ref = ref.child('users')
        users_ref.child(str(user_id)).set(chat_id)
        logger.info(f"User {user.first_name} (ID: {user_id}) added/updated in the database.")
    except Exception as e:
        logger.error(f"Failed to add user to database: {e}")
    
    reply_keyboard = [["🛒 BUY PROXY", "☎ NUMBER BOT"], ["NEED HELP ❓"]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 আসসালামু আলাইকুম \n✅ Sell4U তে আপনাকে স্বাগতম \n🟢 Join Official Channel For Updates \n👉 @sell4u_market 👈",
        reply_markup=reply_markup
    )

# ইনলাইন বাটন ক্লিকের জন্য ফাংশন (অপরিবর্তিত)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'inline_1':
        await query.edit_message_text(text="👉 PROXY DETAILS \n NAME: USA(BUFALIO)[PRO] \n SPEED: 3MB ↓↑ \n ISSUE: ❌ NO ISSUE \n ID SUSPEND: ⛔ NO \n LIMIT: 1GB \n USES: 24/7 \n PRICE: 40 BDT/0.38 USD \n\n\n 🛒 FOR BUY 🛒\n PAY 40 BTD ON BKASH/NAGAD\n 01796095176\n GIVE SCREENSHOT OF PAYMENT\n BOT: @sell4ubd_bot\n CHANNEL: @sell4u_market")

# সাধারণ মেসেজ হ্যান্ডেল করার ফাংশন (অপরিবর্তিত)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message == "🛒 BUY PROXY":
        inline_keyboard = [[InlineKeyboardButton("🛒 BUY PROXY", callback_data='inline_1')]]
        await update.message.reply_text("PREMIUM PROXY কিনতে নিতে দেওয়া বাটনে ক্লিক করুন", reply_markup=InlineKeyboardMarkup(inline_keyboard))
    elif user_message == "☎ NUMBER BOT":
        inline_keyboard = [[InlineKeyboardButton("☎ NUMBER BOT", url="https://t.me/otp_palestine_v1_bot")]]
        await update.message.reply_text("NEW OTP RECIVER BOT", reply_markup=InlineKeyboardMarkup(inline_keyboard))
    elif user_message == "NEED HELP ❓":
        inline_keyboard = [[InlineKeyboardButton("♻ JOIN SUPPORT BOT", url="https://t.me/sell4upay_bot")]]
        await update.message.reply_text("JOIN OUR SUPPORT BOT AND TEXT", reply_markup=InlineKeyboardMarkup(inline_keyboard))
    else:
        await update.message.reply_text(f"❌ UNKNOWN COMMAND: {user_message}")

# অ্যাডমিন কমান্ড (অপরিবর্তিত)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) != ADMIN_ID:
        await update.message.reply_text("এই কমান্ডটি শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে।")
        return
    if not context.args:
        await update.message.reply_text("ব্যবহারের নিয়ম: /broadcast <আপনার মেসেজ>")
        return
    message_to_broadcast = ' '.join(context.args)
    users = ref.child('users').get()
    if not users:
        await update.message.reply_text("ডাটাবেসে কোনো ব্যবহারকারী নেই।")
        return
    success_count, fail_count = 0, 0
    failed_users = []
    for user_id, chat_id in users.items():
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_to_broadcast)
            success_count += 1
        except Forbidden:
            logger.warning(f"User {user_id} has blocked the bot. Removing.")
            fail_count += 1
            failed_users.append(user_id)
        except Exception as e:
            logger.error(f"Failed to send to {chat_id}: {e}")
            fail_count += 1
    for user_id in failed_users:
        ref.child('users').child(user_id).delete()
    report = f"📢 ব্রডকাস্ট সম্পন্ন!\n\n✅ সফল: {success_count}\n❌ ব্যর্থ: {fail_count} (যারা বট ব্লক করেছে তাদের মুছে ফেলা হয়েছে)"
    await update.message.reply_text(report)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) != ADMIN_ID:
        await update.message.reply_text("এই কমান্ডটি শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে।")
        return
    users = ref.child('users').get()
    total_users = len(users) if users else 0
    await update.message.reply_text(f"📊 মোট ব্যবহারকারী: {total_users}")

# --- মূল ফাংশন (এখানে পরিবর্তন করা হয়েছে) ---
def main() -> None:
    """বট এবং ওয়েব সার্ভার চালু করার জন্য প্রধান ফাংশন"""
    # --- নতুন যুক্ত করা অংশ ---
    # Flask সার্ভারটিকে একটি আলাদা থ্রেডে চালানো হচ্ছে
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # -------------------------

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))

    print("🚀 Bot is running with Firebase and Flask integration...")
    application.run_polling()

if __name__ == "__main__":
    main()
