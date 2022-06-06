from telethon import TelegramClient, events
from telethon.tl.custom import Button
from dotenv import load_dotenv
from constants import SUBMIT_BUTTON, RESET_BUTTON, HELLO_TIP, SUBMIT_TIP

import os
import redis
import pprint
import subprocess
import logging
import storage
import markdown
import sys
import shutil

load_dotenv()
bot = \
    TelegramClient(os.environ['BOT_NAME'], os.environ['BOT_ID'], os.environ['BOT_API_KEY']) \
    .start(bot_token=os.environ['BOT_TOKEN'])

logging.basicConfig( \
    filename=os.environ['LOG_FILE'], \
    level=logging.__getattribute__(os.environ['LOG_LEVEL']))

def inline_buttons():
    return [[Button.text(SUBMIT_BUTTON), Button.text(RESET_BUTTON)]]

def del_artifacts(sender):
    storage.del_values(sender)
    shutil.rmtree(sender)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    logging.info(f"Received /start")
    logging.debug(f"event {event}")
    await event.respond('Привет!\n' + HELLO_TIP)
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern=RESET_BUTTON))
async def callback(event):
    logging.info(f"Received {RESET_BUTTON}")
    logging.debug(f"event {event}")
    sender = str(event.chat_id)
    del_artifacts(sender)
    await event.respond('Начинаем заново!\n' + HELLO_TIP, buttons=Button.clear())
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern=SUBMIT_BUTTON))
async def callback(event):
    logging.info(f"Received {SUBMIT_BUTTON}")
    logging.debug(f"event {event}")
    sender = str(event.chat_id)
    values = storage.list_values(sender)
    markdown_file = markdown.create(values, sender)
    pdf_file = os.path.join(sender, 'home_assignment.pdf')

    await event.respond('Готовлю pdf🥁\n')

    subprocess.run(['pandoc', '-f', 'markdown', markdown_file, '-o', pdf_file])
    
    await event.respond('Готово⚡️💪\n', 
        buttons=Button.clear(),
        file=pdf_file
    )
    del_artifacts(sender)
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def callback(event):
    logging.info(f"Received events.NewMessage")
    logging.debug(f"event {event}")
    sender = event.chat_id
    user_id = str(sender)
    if os.path.exists(user_id) == False:
        os.mkdir(user_id)
    if event.media != None:
        file_name = str(event.file.media.id)
        result = await bot.download_media(event.media, os.path.join(user_id, file_name))
        if result != None:
            storage.push_value(user_id, result)
        else:
            raise RuntimeError(f"Error on downloading media\n{media}")

        await event.respond('Файл загружен⚡️💪\n' + SUBMIT_TIP, buttons=inline_buttons())

def main():
    storage.init()
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
