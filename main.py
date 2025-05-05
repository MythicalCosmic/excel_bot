import asyncio
import logging
from uvicorn import Config, Server
from fastapi import FastAPI, HTTPException, Query
from aiogram.types import Update
from config.config import bot, dp
from utils.utils import get_user_info, get_user_id
from config.settings import WEBHOOK
import traceback


app = FastAPI()

@app.post("/webhook")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


async def start_webhook():
    logging.info("Starting bot in webhook mode...")
    config = Config(app=app, host="0.0.0.0", port=8002)
    server = Server(config)
    await server.serve()

from pydantic import BaseModel

class NotifyUserRequest(BaseModel):
    phone_number: str
    amount: float

@app.post("/notify-user/")
async def notify_user(data: NotifyUserRequest):
    phone_number = data.phone_number
    amount = data.amount

    telegram_id = get_user_id(phone_number=phone_number)
    if not telegram_id:
        raise HTTPException(status_code=404, detail="Telegram ID not found for this user")

    message = f"💰 Your account has been credited with {amount} units. Thank you!"
    await bot.send_message(chat_id=telegram_id, text=message)
    return {"status": "success", "message": "Notification sent successfully"}
    
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
