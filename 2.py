import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.error import Forbidden
import firebase_admin
from firebase_admin import credentials, db
import json

# --- আপনার তথ্য এখানে দিন ---
# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"
# আপনার নিজের টেলিগ্রাম Chat ID (স্ট্রিং হিসাবে)
ADMIN_ID = "6893452352"

# Firebase সেটআপ
# serviceAccountKey.json ফাইলটির সঠিক পাথ দিন
cred_json = {
  "type": "service_account",
  "project_id": "jahanara-ef632",
  "private_key_id": "348c16145c9c97e4f34e11644a6869b4c826720a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBSyrV5gQM3FF0\n1tAgf4Mwvx0I7h197jej/pX1s/DxDt3JzlY7Jrr5d0VQfXOQhlcqNddYJx35l3JH\nNyMS8OkL/qQqIfFOwOSz12gcVYReLOK+aVYwG0uezk26UcdublihT/PlnM9e0u4w\nn0ZojXMUq9MGADyVexUgw9uT4rLJbu0CRAStUxyDATkNnkxIlirrqsV2pxjCCHeb\np3sA6IodCkjDUoevQZcop/z+A86iGuGO/tjHA8f4nwrukt5VQj8ESBE0hYgSoaRQ\nUYO4Pj+GOdE7jUnlWb8/fdzj8LoMTHwgCqFdjBIqq7GcxvS/fNMAMXona1P2ZNdt\nppsoylh5AgMBAAECggEALzg3rK1WS/X+iDZ5/ZZo7B2j8CyLU9pACXYGGFHvCFSD\nZetcMXMStiKm8jTTaHkJDiy9ALH9pp2Ss0cK8HOd2upIHGrSUlTZCf4TVuilP4Rj\nl/SPs4zXemIXpu6Xc6jNSgsIIA2gsx+ARKyEPMJhXKllEdA4/KNm0+xE1enJl19u\nNnYzJWXbpQdq1irGp2c3B1GVe2pJx0RUheoYnaUYXRd1RP4uWscX3irs004Xi/dm\nRxU4xTDgTgLdMYt8F5lP5NSqsR1eCgp3Gx1eNc5f+YsLLTQFT0F/Y46x7JFvhn2K\nm8EjvTzw4ixIDW2/doiHfvMNhGqg554GkH2GfIlV6QKBgQD9cNrsz3+43x+avROL\n5F5ih23vWBXU6VPrrffBipAZt3nhcDYkGMlWZ4E1ejb2gdRtJuAd+Ni0jxMsnq6g\nzyL8ZhqrDSp/nVofroljJikAuq2/kckgO4tnurAteq9/A+nVCgZ4amKGdc2xmZdU\nJnRHlSclTWzign5/CZo2t5k9qwKBgQDDPtTfRLB7e6pb7kYLmwijKIVrEPrHrNvi\np4Mq9qdlxsESSFeojabu9iEy7plHYjPvM8bZ2fFLx2OWGDxJf8SCUd0zZ6qc4wbW\nD05DH0wgYigetQELY8nzRsr5pgbt9kyyYt5FkOB4Lk8DiO39dpdNi44lRhWC+U42\npMZGy7K2awKBgGagTmZaV9PatgeIzON25CltwbyLpLuEiDEFTzAWFefz/eyl7aaM\nSussGow3Iw6K4CQa++HnJIlo7lDBKOGBPx+JkP724+CtLRNrL8LwbuYWscjDFfhx\nZC/qzvB7n5kFUqir2JbmLWNZTKPAGCFBORDLewCF67OFOAflMYc6rVjlAoGBAKwk\nW582eruEvyEqpctZt3XTJj7Ny639NClUNAvPSKwtXtD1w4Oy0LnjfEXhpHcRmGSQ\nLASraVm8xIrzd0P+SI32C6dlAUIt0DsvZ3s6vu3WXTUltXQLWWUKx67wuS9ZdynY\njcyb/a04dyXQtrRAuQn/vyYR8ql1kYYQJVkKA9ldAoGBAI68ERuhLwCbDPP3Vwni\nGR1wwslj0jytCyiMWnAASp9cTJ2hf1m13tkqdd3m3r1yS1lswYafUUpcgwPhVmEU\nYLeREhznncc4himUKUA6L88xJ9H+7R0e5EnJWq2z3pjN2HlR6/LyLqhO2Wboa6QC\nAPphW9geMdysJOn6RiS/ZUUt\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@jahanara-ef632.iam.gserviceaccount.com",
  "client_id": "109393520407792440821",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40jahanara-ef632.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred, {
    # আপনার Firebase Realtime Database-এর URL
    'databaseURL': 'https://jahanara-ef632-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
# ডাটাবেসের একটি রেফারেন্স তৈরি করা
ref = db.reference('/')
# --- তথ্য দেওয়া শেষ ---


# লগিং কনফিগার করা হচ্ছে
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start কমান্ডের জন্য ফাংশন (Firebase যুক্ত করা হয়েছে)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start কমান্ড দিলে এই ফাংশনটি কাজ করবে এবং ব্যবহারকারীকে ডাটাবেসে সেভ করবে"""
    user = update.effective_user
    user_id = user.id
    chat_id = update.effective_chat.id

    # --- Firebase এ ব্যবহারকারীর তথ্য সেভ করার অংশ ---
    try:
        users_ref = ref.child('users')
        users_ref.child(str(user_id)).set(chat_id)
        logger.info(f"User {user.first_name} (ID: {user_id}) added/updated in the database.")
    except Exception as e:
        logger.error(f"Failed to add user to database: {e}")
    # --- Firebase অংশ শেষ ---

    # --- আপনার আগের কোড অপরিবর্তিত রাখা হয়েছে ---
    reply_keyboard = [
        ["🛒 BUY PROXY", "☎ NUMBER BOT"],
        ["NEED HELP ❓"]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 আসসালামু আলাইকুম \n✅ Sell4U তে আপনাকে স্বাগতম \n🟢 Join Official Channel For Updates \n👉 @sell4u_market 👈",
        reply_markup=reply_markup
    )

# ইনলাইন বাটন ক্লিকের জন্য ফাংশন (অপরিবর্তিত)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ইনলাইন বাটনের কলব্যাক ডেটা হ্যান্ডেল করে"""
    query = update.callback_query
    await query.answer()

    if query.data == 'inline_1':
        await query.edit_message_text(text="👉 PROXY DETAILS \n NAME: USA(BUFALIO)[PRO] \n SPEED: 3MB ↓↑ \n ISSUE: ❌ NO ISSUE \n ID SUSPEND: ⛔ NO \n LIMIT: 1GB \n USES: 24/7 \n PRICE: 40 BDT/0.38 USD \n\n\n 🛒 FOR BUY 🛒\n PAY 40 BTD ON BKASH/NAGAD\n 01796095176\n GIVE SCREENSHOT OF PAYMENT\n BOT: @sell4ubd_bot\n CHANNEL: @sell4u_market")

# সাধারণ মেসেজ হ্যান্ডেল করার ফাংশন (অপরিবর্তিত)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """বটম বাটন থেকে আসা টেক্সট মেসেজ হ্যান্ডেল করে"""
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

# --- নতুন অ্যাডমিন কমান্ড ---

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """অ্যাডমিনের কাছ থেকে ব্রডকাস্ট মেসেজ পাঠায়"""
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
    """মোট ব্যবহারকারীর সংখ্যা দেখায়"""
    if str(update.message.from_user.id) != ADMIN_ID:
        await update.message.reply_text("এই কমান্ডটি শুধুমাত্র অ্যাডমিন ব্যবহার করতে পারবে।")
        return

    users = ref.child('users').get()
    total_users = len(users) if users else 0
    await update.message.reply_text(f"📊 মোট ব্যবহারকারী: {total_users}")

# --- মূল ফাংশন ---

def main() -> None:
    """বটটি চালু করার জন্য প্রধান ফাংশন"""
    application = Application.builder().token(TOKEN).build()

    # আগের হ্যান্ডেলারগুলো
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # নতুন অ্যাডমিন হ্যান্ডেলারগুলো
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))

    print("🚀 Bot is running with Firebase integration...")
    application.run_polling()

if __name__ == "__main__":
    main()

