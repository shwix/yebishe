import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

users = {}
orders = {}
COMMISSION = 0.15
CRYPTO_ADDRESS = "ВАШ_КОШЕЛЕК_USDT"  # Замените здесь!

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🎵 Spotify", callback_data='service_spotify')],
        [InlineKeyboardButton("🎥 Netflix", callback_data='service_netflix')],
        [InlineKeyboardButton("💳 Виртуальная карта", callback_data='service_card')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')]
    ]
    update.message.reply_text('Выберите сервис:', reply_markup=InlineKeyboardMarkup(keyboard))

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data

    if data.startswith('service_'):
        service = data.split('_')[1]
        context.user_data['current_service'] = service
        query.edit_message_text(text=f"Введите логин/email для {service}:")
    elif data == 'help':
        query.edit_message_text(text="📞 Поддержка: @ваш_аккаунт")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    text = update.message.text

    if 'current_service' in context.user_data:
        service = context.user_data['current_service']
        order_id = len(orders) + 1
        orders[order_id] = {"user_id": user_id, "service": service, "login": text, "status": "pending"}
        
        amount_usd = 15  # Пример для Spotify
        total_crypto = amount_usd * (1 + COMMISSION)
        
        update.message.reply_text(
            f"📝 Заказ #{order_id}:\n"
            f"• Сервис: {service}\n"
            f"• Логин: {text}\n"
            f"• Сумма: {total_crypto:.2f} USDT\n\n"
            f"Адрес: {CRYPTO_ADDRESS}\n"
            f"Сеть: TRC-20\n"
            f"⏳ Таймер: 30 мин"
        )
        del context.user_data['current_service']

def main() -> None:
    updater = Updater("7624343284:AAEXxsYAHHYu0yPzOcdEXlGC3d4K9Es30Q0")  # Замените здесь!
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
