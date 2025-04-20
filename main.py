import asyncio
import logging
from uvicorn import Config, Server
from fastapi import FastAPI
from aiogram.types import Update
from config.config import bot, dp
from config.settings import WEBHOOK


app = FastAPI()

@app.post("/webhook")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


async def start_webhook():
    logging.info("Starting bot in webhook mode...")
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config)
    await server.serve()

async def start_polling():
    logging.info("Starting bot in polling mode...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    logging.info(f"Bot is running in {'WEBHOOK' if WEBHOOK else 'POLLING'} mode.")
    if WEBHOOK:
        await start_webhook()
    else:
        await start_polling()

if __name__ == "__main__":
    logging.info("Bot is starting...")
    asyncio.run(main())
