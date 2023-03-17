import logging
import asyncio

import aiogram.types
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from keyboards import *
from config import DefaultConfig

bot = Bot(token=DefaultConfig.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

user_data = dict()


@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    start_message = "Hello! This bot is based on API of Replicate-powered app scribblediffusion.com.\n" \
                    "Usage: Send a line drawing with a caption describing the desired result. Your input will be " \
                    "used to generate an output image.\n"
    await bot.send_message(chat_id=message.chat.id, text=start_message)


@dp.message_handler()
async def retry_message(message: types.Message):
    """
    Retry message if user don't want to change prompt and image
    :param message:
    :return:
    """
    logging.info(f"{message.text}, {user_data}")
    if message.text == cmd_regenerate or message.text == cmd_retry:
        if user_data.get(message.from_user.id):
            await asyncio.gather(generate_image(message.from_user.id))
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="The cache was cleared due to inactivity. Please resend your image with caption.",
                reply_markup=aiogram.types.ReplyKeyboardRemove()
            )


@dp.message_handler(content_types=['document', 'text'])
async def on_file_with_caption_upload(message: types.Message):
    """
    Handle messages with document content.
    """
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    await process_user_data(file_path, message)


@dp.message_handler(content_types=['photo', 'text'])
async def on_photo_with_caption_upload(message: types.Message):
    """
    Handle messages with image content.
    """
    file = await bot.get_file(message.photo[-1].file_id)
    file_path = file.file_path
    await process_user_data(file_path, message)


async def process_user_data(file_path, message):
    available_formats = {"jpeg", "jpg", "bmp", "gif", "webp"}

    logging.info(f"User: {message.from_user.id} - Prompt: '{message.caption}'")

    json_data = {
        "image": 'https://api.telegram.org/file/bot{0}/{1}'.format(DefaultConfig.TELEGRAM_TOKEN, file_path),
        "prompt": message.caption
    }
    user_data[message.from_user.id] = {
        "chat_id": message.chat.id,
        "json_data": json_data
    }
    if message.caption is None:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Send file with caption, please!",
            reply_markup=aiogram.types.ReplyKeyboardRemove()
        )
    elif file_path.split(".")[-1] not in available_formats:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Only documents with next extensions are supported: " + ", ".join(list(available_formats)),
            reply_markup=aiogram.types.ReplyKeyboardRemove()
        )
    else:
        await asyncio.gather(generate_image(message.from_user.id))


async def generate_image(user_id) -> None:
    """
    Send image and prompt via ScribbleDiffusion API and send new image to user
    """
    scribble_prediction_url = "https://scribblediffusion.com/api/predictions/"
    chat_id = user_data[user_id]["chat_id"]
    json_data = user_data[user_id]["json_data"]

    msg = await bot.send_message(
        chat_id=chat_id,
        text="Generating image..."
    )

    response = requests.post(
        scribble_prediction_url, json=json_data
    )
    for i in range(10):
        prompt = json_data["prompt"]
        logging.info(f"User: {user_id} - Try {i} - Prompt: '{prompt}'")
        await asyncio.sleep(2)
        image_response = requests.get(
            scribble_prediction_url + response.json()["id"]
        )
        if image_response.json()["output"] is not None and len(image_response.json()["output"]) == 2:
            await bot.send_document(
                chat_id=chat_id,
                document=image_response.json()["output"][1],
                caption=f'Done in {round(image_response.json()["metrics"]["predict_time"], 2)} seconds.'
                        f'\nPrompt: {json_data["prompt"]}',
                reply_markup=kb_regenerate
            )
            break
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Something is wrong. Please retry!",
            reply_markup=kb_retry
        )


@dp.errors_handler()
def error(update, context):
    """
    Log Telegram exceptions
    """
    logging.warning(f"Update '{update}'")
    logging.exception(context.error)


async def on_startup(dp):
    await bot.set_webhook(DefaultConfig.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    logging.warning('Bye!')


if __name__ == '__main__':
    # Enable logging
    DefaultConfig.init_logging()
    # Start the Bot
    if DefaultConfig.MODE == "webhook":
        start_webhook(
            dispatcher=dp,
            webhook_path=DefaultConfig.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=DefaultConfig.WEBAPP_HOST,
            port=DefaultConfig.WEBAPP_PORT,
        )
        logging.info(f"Start webhook mode on port {DefaultConfig.WEBAPP_PORT}")
    else:
        executor.start_polling(dp)
        logging.info(f"Start polling mode")
