from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import Update

import logging

TOKEN = 'SECRET INFORMATION'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Приветствую великих людей!")


def sum(update, context):
    args = context.args
    if len(args) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Нужно передать 2 аргумента: /sum (число) (число)!")
    try:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{int(args[0]) + int(args[1])}")
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Не удалось преобразовать аргументы к целому типу!")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
start_handler = CommandHandler('start', start)
sum_handler = CommandHandler('sum', sum)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(sum_handler)
dispatcher.add_handler(start_handler)
updater.start_polling()
