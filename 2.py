from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# =======================
# Bot Token
TOKEN = "7884768889:AAHyXrH1YDwwPhHP-pZn9R5ukWhFPB4xG2U"

# 
# =======================
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🛒 BUY SERVICES")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 আসসালামু আলাইকুম \n✅ Sell4U তে আপনাকে স্বাগতম \n🟢 Join Official Channel For Updates \n👉 @sell4u_market 👈",
        reply_markup=reply_markup
    )

# =======================
# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "🛒 BUY SERVICES":
        keyboard = [
            [InlineKeyboardButton("🔗 BUY PROXY PRO", callback_data="normal_btn")],
            [InlineKeyboardButton("🎬 HOW TO BUY", url="https://t.me/sell4upay_bot")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ Premium Proxy কিনতে নিতে দেওয়া বাটনে ক্লিক করুন \n যদি না জেনে থাকেন তাহলে ভিডিও দেখে আসেন",
            reply_markup=reply_markup
        )

# =======================
# Handle callback buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        await query.answer()
        if query.data == "normal_btn":
            await query.edit_message_text(text="👉 PROXY DETAILS \n NAME: USA(BUFALIO)[PRO] \n SPEED: 3MB ↓↑ \n ISSUE: ❌ NO ISSUE \n ID SUSPEND: ⛔ NO \n LIMIT: 1GB \n USES: 24/7 \n PRICE: 40 BDT/0.38 USD \n\n\n 🛒 FOR BUY 🛒\n PAY 40 BTD ON BKASH/NAGAD\n 01796095176\n GIVE SCREENSHOT OF PAYMENT\n BOT: @sell4ubd_bot\n CHANNEL: @sell4u_market")




# Broadcast function
# def broadcast_message(app, text: str):
#     ref = db.reference('users')
#     users = ref.get()
#     if not users:
#         print("No users to broadcast.")
#         return
#     for uid, info in users.items():
#         try:
#             app.bot.send_message(chat_id=int(uid), text=text)
#             print(f"Sent to {uid}")
#         except Exception as e:
#             print(f"Failed to send to {uid}: {e}")

# # =======================
# # /broadcast command (admin only)
# async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     admin_id = 6893452352  # <-- Replace with your Telegram ID
#     if update.effective_user.id != admin_id:
#         await update.message.reply_text("❌ You are not authorized to use this command.")
#         return
#     message = " ".join(context.args)
#     broadcast_message(context.application, message)
#     await update.message.reply_text("✅ Broadcast sent!")

# =======================
# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    # app.add_handler(CommandHandler("broadcast", broadcast_command))

    print("✅ Bot is running...")
    app.run_polling()

# =======================
if __name__ == "__main__":
    main()
