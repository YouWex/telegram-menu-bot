import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from db import init_db, add_user, is_admin

import os

TOKEN = os.getenv("BOT_TOKEN")
    raise Exception("BOT_TOKEN tanımlı değil")

def main_menu(is_admin_user=False):
    keyboard = [
        [InlineKeyboardButton("🎮 Menü", callback_data="menu")],
        [InlineKeyboardButton("⚙️ Ayarlar", callback_data="settings")]
    ]
    if is_admin_user:
        keyboard.append([InlineKeyboardButton("👑 Admin", callback_data="admin")])
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    add_user(user.id, user.username)

    update.message.reply_text(
        "Hoş geldin kanka 😎",
        reply_markup=main_menu(is_admin(user.id))
    )

def callback(update: Update, context: CallbackContext):
    q = update.callback_query
    q.answer()

    if q.data == "menu":
        q.edit_message_text(
            "🎮 Menü:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Ücretsiz", callback_data="free")],
                [InlineKeyboardButton("💎 Ücretli", callback_data="paid")],
                [InlineKeyboardButton("⬅️ Geri", callback_data="back")]
            ])
        )

    elif q.data == "free":
        q.edit_message_text("🔥 Ücretsiz içerikler")

    elif q.data == "paid":
        q.edit_message_text("💎 Yetkili içerik")

    elif q.data == "settings":
        q.edit_message_text("⚙️ Ayarlar")

    elif q.data == "admin":
        q.edit_message_text("👑 Admin panel")

    elif q.data == "back":
        q.edit_message_text(
            "Ana Menü:",
            reply_markup=main_menu(is_admin(q.from_user.id))
        )

def run():
    init_db()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run()
