import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.error import Forbidden
import firebase_admin
from firebase_admin import credentials, db
import json
import os

# --- আপনার তথ্য এখানে দিন ---
# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"
# আপনার নিজের টেলিগ্রাম Chat ID (স্ট্রিং হিসাবে)
ADMIN_ID = "6893452352"

# Firebase সেটআপ
# serviceAccountKey.json ফাইলটির সঠিক পাথ দিন
cred_json = json.loads(os.environ["{
  "type": "service_account",
  "project_id": "jahanara-ef632",
  "private_key_id": "3fa75ae361cf3b1f93a7911377303df7d51f7e82",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDze9u7ESNAsgJY\nlsGkkiO+fiXlqS/e/iKRhLA7VSKlYcFlB33Ps0dE1MznntF9w9tj61NPSErhUOO0\nRA+EgTVHio2LzusXN4xYX2EIJIMsY3XWdZcdiEl0dGZUDl1K7y/1fACDDy6p5GXT\n5iyMrH3dHxWX3BEQ8Qtb/Nx7lVD3I2ttIS9qwwE/0yiCOVVnS3gxkZz0yNOfFZxk\nqNj6QdffZbjsmhyo1aFroAl32p0IObuO0qNdFE1tNw6QI8TncDxXlFX47poANauZ\n/xZ00dJmoipxWo8Vf17lEFP/WJarWZjWlQUg0Kuz/aNzIUjzjrMT5hciRK7IbLQX\nhACdU+bhAgMBAAECggEADFDCHhnJb5DpbTdv4z34lJ6vFkka2KPAVh2w58lgO58A\nkBaDSrWJ1+2PETKfbEXzM4BASiDxF6k2oUQ1iDlcW2piyzTrv3SB8ujdILMvFthP\niinPu1DMzVkDYYJJ/fuv8HHlmTtz++gnbeLFM1bYtW3octJQ4ytcDJqzQMV+T0e4\nONBd/OoMzqE7HrKtAa3/w75irr8ElqE0fh3hO5uNM5UpV4Nk1Xw3A2WZEsbjWIim\nXZtcL9hhAhvQbjDOfw1SyV14+dL28tsYZ42TYkbRws5H5HHgyPc9P2qtri8cTi+k\nKYi/28BtgWSa3RamIUsRaUiudIEoN2H6ZYUHpgcu6QKBgQD/Dbot7STlomqzmMlW\ng4dUAtIfbQsmzBj/G6JexgJU2x86O9STEZreTO/0WBgiLtts7XD1JFb2EltDNUzi\n/ovBK8zrpd1WTVjgpHrhkh7brl3jtvLg90HlPwQbooN/L/UFJhZcUr/6pjY30UEL\nvlmeIIs1C9uLaA1VlX83ShQDOQKBgQD0YyQadjXhuAeBzgIr+4XcjfVGg8IDOwJR\n3e4YPeYdwFDjSQvdczL2Wg7BmjUEr+qyCondUIyy+hFDB0LBSr6EU8XEaCyrOf9w\nMgkU5U8ia8T9ZIky0SLYGHxKDvH01QeCj3BBTO2Zyw4wfW7kATVMN+qV2XgrvjBp\nmZG0SSy46QKBgQDFabSfc5xJeWspU6sTIX8PkZdd56LoBrWaT6Nfw9duIqSLCGBC\n7S93vQlFkSIs4yPHrgjuVZBRqmelH45BbFBz1hkolBs7f2a5idXq3pSv6MiXRrW7\nVuZUMHBXi3RIb7AwqghIsWwS76+riHXWRyFKeVoGVwU5Y/JeOfZbryTKUQJ/SI0m\nKrTtShVYJTEDdAs3skJyjnyPHGZoSeWYyZmWtz5gxRjqbNPGTVxvBQrCsqGHC1QV\nmZ5QJtIWTc/aAYgvBxnXnHdQy4RsUOKJz6pD0/Qqhw9Rq8Rqk7yxKUtGiWi00g3D\nRZ+Q6hdeHwcd5JJ3QClZeyMUiefsd20f1GXk4QKBgQCW5mhDyYTUxMHuL9avUlQq\nbLPC2/I5HS3fna62fIdUCrj3IMxWd0fpWPZoy3wyjkumBVHHT7rD9odCDYU6o8RA\nXBK9UeVVhtaqJioeFo/QrgZfCmEoyhOIesAJNXoFwyyTiCSfmmmHiEID7YzS246E\nAeJpYt5nIKWW/aV/UOqbrQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@jahanara-ef632.iam.gserviceaccount.com",
  "client_id": "109393520407792440821",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40jahanara-ef632.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}"])
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


