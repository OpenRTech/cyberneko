from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random
from random import randrange
import urllib
import json
import rstr
import requests
import time
import config


###

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.error('"%s" caused error "%s"', update, error)

###

def getRandomWallhavenArts(wallhavenTag, wallhavenlastPage):

    warpedTime = int( time.time() * 1000.0 )
    random.seed(((warpedTime & 0xff000000) >> 24) +
             ((warpedTime & 0x00ff0000) >>  8) +
             ((warpedTime & 0x0000ff00) <<  8) +
             ((warpedTime & 0x000000ff) << 24)) # fuck yeah

    randomPageSeed = rstr.xeger(r'[a-zA-Z0-9]{6}')
    randomPage = randrange(wallhavenlastPage)
    randomImage = randrange(23) # wallhaven does have 24 pictures on page

    wallhavenUrl = 'https://wallhaven.cc/api/v1/search?q=id:' + wallhavenTag + '&purity=100&seed=' + randomPageSeed + '&category=anime&sorting=favorites&page=' + str(randomPage)

    wallhavenPage = requests.get(wallhavenUrl)
    wallhavenJson = wallhavenPage.json()

    imageUrl = wallhavenJson["data"][randomImage]["path"]
    return imageUrl


def start(update, context):
    randomImage = getRandomWallhavenArts("animal ears", 47)
    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=randomImage, caption=randomImage, disable_notification=True)

start_handler = CommandHandler('start', start)


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text, disable_notification=True)

echo_handler = MessageHandler(Filters.text, echo)




def main():
    
    updater = Updater(token=config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
