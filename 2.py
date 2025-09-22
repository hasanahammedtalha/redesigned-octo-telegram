import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# আপনার টেলিগ্রাম বটের টোকেন এখানে দিন
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"

# লগিং কনফিগার করা হচ্ছে
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start কমান্ডের জন্য ফাংশন
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start কমান্ড দিলে এই ফাংশনটি কাজ করবে"""

    # --- বটম বাটন (Reply Keyboard) ---
    reply_keyboard = [
        ["মেনু ১", "মেনু ২"],
        ["সাহায্য"]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    # --- ইনলাইন বাটন (Inline Keyboard) ---
    inline_keyboard = [
        [InlineKeyboardButton("ইনলাইন বাটন ১", callback_data='inline_1')],
        [InlineKeyboardButton("ইনলাইন বাটন ২", callback_data='inline_2')],
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        "হ্যালো! আমি একটি ডেমো বট।",
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "অনুগ্রহ করে একটি ইনলাইন বাটন নির্বাচন করুন:",
        reply_markup=inline_markup
    )


# ইনলাইন বাটন ক্লিকের জন্য ফাংশন
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ইনলাইন বাটনের কলব্যাক ডেটা হ্যান্ডেল করে"""
    query = update.callback_query
    await query.answer() # কলব্যাক ক্যোয়ারীটি গ্রহণ করা হয়েছে তা নিশ্চিত করে

    if query.data == 'inline_1':
        await query.edit_message_text(text="আপনি 'ইনলাইন বাটন ১' ক্লিক করেছেন।")
    elif query.data == 'inline_2':
        await query.edit_message_text(text="আপনি 'ইনলাইন বাটন ২' ক্লিক করেছেন।")


# সাধারণ মেসেজ হ্যান্ডেল করার জন্য ফাংশন (বটম বাটনের জন্য)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """বটম বাটন থেকে আসা টেক্সট মেসেজ হ্যান্ডেল করে"""
    user_message = update.message.text

    if user_message == "মেনু ১":
        await update.message.reply_text("আপনি 'মেনু ১' নির্বাচন করেছেন।")
    elif user_message == "মেনু ২":
        await update.message.reply_text("আপনি 'মেনু ২' নির্বাচন করেছেন।")
    elif user_message == "সাহায্য":
        await update.message.reply_text("সাহায্যের জন্য /start কমান্ড দিন।")
    else:
        await update.message.reply_text(f"আপনি বলেছেন: {user_message}")


def main() -> None:
    """বটটি চালু করার জন্য প্রধান ফাংশন"""
    # অ্যাপ্লিকেশন তৈরি করুন এবং আপনার বটের টোকেন দিন
    application = Application.builder().token(TOKEN).build()

    # বিভিন্ন কমান্ডের জন্য হ্যান্ডেলার যোগ করুন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # বটটি চালু করুন
    application.run_polling()


if __name__ == "__main__":
    main()
