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
  "private_key_id": "31aac16002452541f7310a589cb726b858310709",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxKMP4m9AWXd0p\ncCXbNX90E9cjMfNznmTAcTQ+3uU6YDKIWx8kAOn6iMXsLxyxjY/6SiVNwoptRvsj\nb9R6AbxBTtrCgEYLeDs5bEatJFL6JmqTiaWY2ZXyRUiWmfVFDxW78BaeWkHF8fFb\nuzWnv5i8mfyMbKSrOHSB3YpVmD4iJJwCLRlFGtf3hKLqm08vq+UbMrw16EbTJIcd\ngYw4OR/sYnFfOSQshIdhqphiEDmJELlNR0S3blOmNh9vN7dbbhMoptLTjS06ZptT\nXtIHfLP/QCOAUHdZrt//olL5QSKVfrAm8Z3pqFMtPTzDG7DJlJPjQ4CvKqXTRcee\neRnoybLTAgMBAAECggEATfMF50mHkY/TU/xIa99qKQTh0FaWK/Uxl4s31cH1Um4p\nTd3qIclVKissCvPfyC/lfddJ+qDyj4p/zePStaw1zPaJQrN2Hm3UgTunDV/CMtbc\nZfZWqp5yX5skiT9MsAonIf5NtXc5IYOHEzmYLisbZUDL4m2bNsssWEfGKktGa3a6\nxbKeHrdBtLlc4Egb9c3UPuphUIs0N9HHMK3nf9Q0HXnrJTrifqJ/0YC76jVvOdLp\ns/N4ZrKXel/ArVTVe0XHLq3Dqkhu7P1OrtlQVYnjfHP1arX4wnLqGF0T9hbbxuS/\nHUKKlj/+VCLOdxh4mfcFc8s1Hzo7CRd3Jm+GyOXI4QKBgQD2/iCmuY+ujdrqITdG\nbPk/yl2MaIkQ6vIz21xqGJsyVa9vuRaxnh4rweyOzEbvQlaLvuO9z/THhsrBpfUG\neXa/2CfVInFojLB+HzzdvanrwVhaFOqk5BJHYxa91yP/qeeDAFoZDGNBVdhJpnCl\n+mnRRuJTrQ6WRNgi51kgSy+QRwKBgQC3nq/6XQwZXKN+P+sUvw9PzFpQ6H9yrOAN\n/WK+W3SzOpnJufefmz79YJk8O8DlkrzYci63/zSHo8a+uNdHu7EQBEfbWiQIGgS0\nBKd7xg6lGbl2sLiRXRylAuVQ/qYNB6PD16LHA72yLFO0IkC5d5B4J4rAUoxTtVOK\nYnpgKwm7FQKBgQCSr/agThBBMMpUxolXcBzPf9XzL5pHy+EwXxURha+WQ0E/7wLF\nVgzBHBjr7fIq4pEXybTj4/+SCEGepHtS7wxRf4SYli4YU4X2QYMahivGcjuQtF9u\nsm0QrI6zDHS6wCNYr/rSaYMBKISdqRW53XC+84QzAdJp+FUM1a0e+sgyvQKBgBN4\n6qScVXojDtuGn8F1eYQ24aUO4uUgXCpfoqcZP8j5//EanZ35cragFeADXjN6WjiB\n815j3Ag+YAc9xua+ispuCcjDSGrrh3AnxjMkD82GatqhZxFTVIRTSEpMlwNuufk8\n1vBP/z/z33SM5VxFx7ZWSyqWFneSFSfpxZyJM+D5AoGAYO3pg3QZYoqjgsRqWeqF\nGBHH7H6FOXhANNA2jG4MI1o8q9Ybvg6Fm6wIbyZ5NubkXuwgQJcBBo1TwU1ROpLK\nDWt/g3gmTri6agt6UWMdR/zs/qFAo+QmxNa/QVaeyeIyT+Fb8kM7Vpi9V5PwaogN\n+4a/xCPH9PWZQ/8Y7Xmbyf8=\n-----END PRIVATE KEY-----\n",
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


