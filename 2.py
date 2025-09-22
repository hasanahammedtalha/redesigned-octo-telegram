import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

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
# Handle user text
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "BUY OTP PRO":
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
# Handle inline button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "normal_btn":
        await query.edit_message_text(
            text="👉 PROXY DETAILS \n NAME: USA(BUFALIO)[PRO] \n SPEED: 3MB ↓↑ \n ISSUE: ❌ NO ISSUE \n ID SUSPEND: ⛔ NO \n LIMIT: 1GB \n USES: 24/7 \n PRICE: 40 BDT/0.38 USD \n\n\n 🛒 FOR BUY 🛒\n PAY 40 BTD ON BKASH/NAGAD\n 01796095176\n GIVE SCREENSHOT OF PAYMENT\n BOT: @sell4ubd_bot\n CHANNEL: @sell4u_market"
        )

# ======================
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = "https://redesigned-octo-telegram-12x.onrender.com/"  # নিজের Render URL বসাও

    await app.bot.delete_webhook()
    await app.bot.set_webhook(RENDER_URL)

    print("🚀 Bot is running with webhook...")
    await app.run_webhook(listen="0.0.0.0", port=PORT, webhook_url=RENDER_URL)

if __name__ == "__main__":
    asyncio.run(main())
