from flask import Flask, request, render_template 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler, CallbackContext
from bot import main as run_telegram_bot
import threading

app = Flask(__name__)

# Вставь сюда токен своего бота 
TELEGRAM_TOKEN = '8116965156:AAGb9sdlIRqV2WbTJEETIyOSRPgYFAwM8HY'

# Функция для обработки команды /start с кнопками
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Курс 1", callback_data='course1')],
        [InlineKeyboardButton("Курс 2", callback_data='course2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите курс:', reply_markup=reply_markup)

# Функция для обработки нажатий на кнопки
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    # Обработка выбора курса
    if query.data == 'course1':
        await query.edit_message_text(text="Вы выбрали Курс 1!")
    elif query.data == 'course2':
        await query.edit_message_text(text="Вы выбрали Курс 2!")

# Функция для обработки текстовых сообщений
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

# Создаем приложение Telegram
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Устанавливаем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Запуск бота через webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    application.process_update(Update.de_json(update, application.bot))
    return '', 200

# Маршрут для мини-приложения
@app.route('/miniapp')
def miniapp():
    courses = ["Курс 1", "Курс 2"]
    # Логика для отображения курсов
    return render_template('index.html')

# Функция для запуска Flask-приложения
def run_flask():
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    # Запуск Telegram-бота в отдельном потоке
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.start()

    # Запуск Flask-приложения в основном потоке
    run_flask()