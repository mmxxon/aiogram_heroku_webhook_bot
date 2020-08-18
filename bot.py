import os
import logging

from aiogram import Bot, Dispatcher, types, executor

PROJECT_NAME = os.environ.get("PROJ")
TOKEN = os.environ.get("TOKEN")

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = "/webhook/" + TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))

bot = Bot(TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


# Example handler
@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id, text="hi")


# Run after startup
async def on_startup():
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


# Run before shutdown
async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == "__main__":
    if "HEROKU" in list(os.environ.keys()):
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp)
