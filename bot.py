from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler, CallbackContext

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    # Создаем кнопки для взаимодействия
    keyboard = [
        [InlineKeyboardButton("Запустить мини-приложение", callback_data='launch_miniapp')],
        [InlineKeyboardButton("Помощь", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Выберите опцию:', reply_markup=reply_markup)

# Функция для обработки команды /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Я могу помочь вам запустить мини-приложение или ответить на ваши вопросы.")

# Функция для обработки текстовых сообщений
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Вы написали: {update.message.text}")

# Функция для обработки нажатий на кнопки
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    # Проверяем, какую кнопку нажал пользователь
    if query.data == 'launch_miniapp':
        # Если выбрали запуск мини-приложения
        await query.edit_message_text(text="Мини-приложение запущено!")
        # Здесь можно добавить дополнительную логику для запуска мини-приложения
    elif query.data == 'help':
        await query.edit_message_text(text="Для запуска приложения нажмите 'Запустить мини-приложение'.")

def main():
    # Вставь сюда токен своего бота
    TELEGRAM_TOKEN = '8116965156:AAGb9sdlIRqV2WbTJEETIyOSRPgYFAwM8HY'
    
    # Создаем приложение бота
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Устанавливаем обработчики команд и кнопок
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()