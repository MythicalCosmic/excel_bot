from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BALANCE = "💰 Balans"
PHONE_NUMBER = "📱 Telefon raqamingizni kiriting:"

def main_key() -> ReplyKeyboardMarkup:
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BALANCE)],
        ],
        resize_keyboard=True
    )

def phone_number_key() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PHONE_NUMBER, request_contact=True)]
        ],
        resize_keyboard=True
    )