import os
import sys
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# -------------------- Настройка Django --------------------
PROJECT_ROOT = r"D:\Cosmetics\crystalcare"
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrystalCare.settings")

import django
django.setup()

from shop.models import Order
from accounts.models import Profile  # твій акаунтс-профіль
from accounts.bot_config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

# -------------------- Клавіатури --------------------
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📦 Відслідкувати замовлення", callback_data="status")],
        [InlineKeyboardButton("📝 Написати відгук", callback_data="review")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_menu_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 Повернутися у меню", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)

# -------------------- /start --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Обери дію нижче:", reply_markup=main_menu_keyboard())

# -------------------- Обробка кнопок --------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "status":
        await query.edit_message_text(
            "Введи ім’я користувача або номер телефону для пошуку замовлення:",
            reply_markup=back_to_menu_keyboard()
        )
        context.user_data["awaiting_status"] = True
        context.user_data["awaiting_review"] = False

    elif query.data == "review":
        await query.edit_message_text(
            "Відправ свій відгук прямо у чат. Після цього він збережеться.",
            reply_markup=back_to_menu_keyboard()
        )
        context.user_data["awaiting_review"] = True
        context.user_data["awaiting_status"] = False

    elif query.data == "menu":
        await query.edit_message_text(
            "Головне меню:",
            reply_markup=main_menu_keyboard()
        )
        context.user_data["awaiting_review"] = False
        context.user_data["awaiting_status"] = False

# -------------------- Обробка повідомлень --------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get("awaiting_status"):
        # Знаходимо профілі, де full_name або phone містить текст
        profiles = Profile.objects.filter(full_name__icontains=text) | Profile.objects.filter(phone__icontains=text)
        orders_text = ""

        for profile in profiles:
            user_orders = Order.objects.filter(user=profile.user).order_by("-created_at")
            for order in user_orders:
                orders_text += (
                    f"📌 Замовлення #{order.id}\n"
                    f"🕒 Статус: {order.get_status_display()}\n"
                    f"💰 Сума: {order.total_price} грн\n\n"
                )

        if not orders_text:
            orders_text = "❌ За вашим запитом замовлень не знайдено."

        await update.message.reply_text(orders_text, reply_markup=back_to_menu_keyboard())
        context.user_data["awaiting_status"] = False

    elif context.user_data.get("awaiting_review"):
        await update.message.reply_text("✅ Дякуємо за відгук! ❤️", reply_markup=main_menu_keyboard())
        context.user_data["awaiting_review"] = False

    else:
        await update.message.reply_text("Будь ласка, обери дію через меню:", reply_markup=main_menu_keyboard())

# -------------------- Запуск бота --------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущено! ✅")
    app.run_polling()
