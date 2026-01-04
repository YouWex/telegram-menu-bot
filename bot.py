import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from db import init_db, add_user

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)

    keyboard = [
        [InlineKeyboardButton("📦 Menü 1", callback_data="menu1")],
        [InlineKeyboardButton("⚙️ Ayarlar", callback_data="settings")]
    ]
    await update.message.reply_text(
        "Hoş geldin kanka 👋",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu1":
        await query.edit_message_text("Menü 1 seçildi")
    elif query.data == "settings":
        await query.edit_message_text("Ayarlar burası")

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()
