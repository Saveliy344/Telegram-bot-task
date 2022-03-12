from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, Defaults
from telegram.ext import CommandHandler, ConversationHandler
from telegram import Update, ParseMode, MessageEntity

import logging

from config import TOKEN

defaults = Defaults(parse_mode=ParseMode.HTML)

updater = Updater(token=TOKEN, defaults=defaults)
dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Приветствую великих людей!")


def get_photo_or_video(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Получено фото или видео!")


def get_audio(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Получено аудио!")


def forward_photo_or_video(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="<b>Переслано фото или видео!</b>")


def get_link(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Получена ссылка!")


def number(update, context):
    try:
        value = float(context.args[1])
        context.user_data[context.args[0]] = float(context.args[1])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"<b>{context.args[0]}: {context.args[1]}</b>")
    except BaseException:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"<b>Не удалось сохранить аргумент!</b>")


def find_sum(update, context):
    try:
        result = int(context.user_data.get(context.args[0])) + int(context.user_data.get(context.args[1]))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{result}")
    except BaseException:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"<b>Не удалось найти нужную сумму!</b>")


start_handler = CommandHandler('start', start)
number_handler = CommandHandler('number', number)
sum_handler = CommandHandler('sum', find_sum)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(MessageHandler((Filters.photo | Filters.video) & Filters.forwarded, forward_photo_or_video))
dispatcher.add_handler(MessageHandler(Filters.photo | Filters.video, get_photo_or_video))
dispatcher.add_handler(MessageHandler(Filters.audio, get_audio))
dispatcher.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), get_link))
dispatcher.add_handler(number_handler)
dispatcher.add_handler(sum_handler)
updater.start_polling()
