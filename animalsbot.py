from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()
token = os.getenv('ANIMALS_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='main.log',
    filemode='w',
    level=logging.INFO)


def get_new_dog():
    URL = 'https://dog.ceo/api/breeds/image/random'
    try:
        response = requests.get(URL).json()
        random_dog = response.get('message')
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url).json()
        random_dog = response[0].get('url')

    return random_dog


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_dog())


def get_new_cat():
    URL = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(URL).json()
        random_cat = response[0].get('url')
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        random_cat = 'https://cataas.com/cat'
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_cat())


def get_new_duck():
    URL = 'https://random-d.uk/api/random'
    try:
        response = requests.get(URL).json()
        random_duck = response.get('url')
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')

    return random_duck


def new_duck(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_duck())


def buttons(update, context):
    if (update.message.text == "Песик🐕"):
        new_dog(update, context)
    if (update.message.text == "Котик🐈"):
        new_cat(update, context)
    if (update.message.text == "Уточка🦆"):
        new_duck(update, context)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([["Песик🐕"], ["Котик🐈"], ['Уточка🦆']],
                                  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого песика я тебе нашёл'.format(name),
        reply_markup=buttons,
        )
    context.bot.send_photo(chat.id, get_new_dog())


def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newduck', new_duck))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, buttons))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
