from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from .states import UserStates
from config.settings import get_translation, ADMIN_ID
from keyboards.keyboards import main_key, phone_number_key, BALANCE
from utils.utils import *

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        if check_user_phone_number_exists(user_id=user_id):
            set_user_state(user_id, UserStates.main.state)
            await message.reply(get_translation("main_message", 'uz'), parse_mode="HTML", reply_markup=main_key())
            await state.set_state(UserStates.main)
        else:
            set_user_state(user_id, UserStates.phone_number.state)
            await message.reply(get_translation("start_message", 'uz'), parse_mode="HTML", reply_markup=phone_number_key())
            await state.set_state(UserStates.phone_number)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"❌ Error: {e}")

@router.message(lambda message: message.contact, UserStates.phone_number)
async def handle_phone_number(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        phone_number = message.contact.phone_number
        set_user_phone_number(user_id=user_id, phone_number=phone_number)
        try:
            user_info = await get_user_info(phone_number=phone_number)
            if user_info and "user_data" in user_info and user_info["user_data"]:
                await message.answer(get_translation('thanks', 'uz'), parse_mode="HTML")
                await message.reply(get_translation('main_message', 'uz'), parse_mode="HTML", reply_markup=main_key())
                await state.set_state(UserStates.main)
                set_user_state(user_id, UserStates.main.state)
            else:
                await message.reply(get_translation('user_not_found', 'uz'), parse_mode="HTML")
                await state.set_state(UserStates.phone_number)
                set_user_state(user_id, UserStates.phone_number.state)
        except Exception as e:
            await message.reply(get_translation('user_not_found', 'uz'), parse_mode="HTML")
            await bot.send_message(ADMIN_ID, f"❌ Error fetching user info: {e}")
            await state.set_state(UserStates.main)
        set_user_state(user_id, UserStates.main.state)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"❌ Error: {e}")

@router.message(lambda message: message.text == BALANCE, UserStates.main)
async def handle_balance(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        set_user_state(user_id, UserStates.main.state)

        phone_number = get_user_phone_number(user_id=user_id)
        user_info = await get_user_info(phone_number=phone_number)

        if user_info and user_info.get("ok") == "true" and "data" in user_info:
            data = user_info["data"]
            balance = data.get("balance", 0)
            await message.answer(get_translation('balance_message', 'uz').format(balance), parse_mode="HTML")
        else:
            await message.answer(get_translation('user_not_found', 'uz'), parse_mode="HTML")

        await message.reply(get_translation("main_message", 'uz'), parse_mode="HTML", reply_markup=main_key())
        await state.set_state(UserStates.main)

    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"❌ Error: {e}")


@router.message(UserStates.main)
async def handle_main(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        set_user_state(user_id, UserStates.main.state)
        await message.reply(get_translation("main_message", 'uz'), parse_mode="HTML", reply_markup=main_key())
        await state.set_state(UserStates.main)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"❌ Error: {e}")



@router.message(UserStates.start, UserStates.phone_number, UserStates.main)
async def handle_unrecognized_input(message: Message, state: FSMContext):
    
    current_state = await state.get_state()
    user_id = message.from_user.id
    state_responses = {
        UserStates.start: {
            "text": get_translation('start_message', 'uz'),
            "keyboard": phone_number_key()
        },
        UserStates.phone_number: {
            "text": get_translation('start_message', 'uz'), 
            "keyboard": phone_number_key()
        },
        UserStates.main: {
            "text": get_translation("main_message", 'uz'),
            "keyboard": main_key()
        }
    }
    response = state_responses.get(current_state, {
        "text": get_translation('main_message', 'uz'),
        "keyboard": main_key()
    })
    await message.reply(
        response["text"],
        reply_markup=response["keyboard"],
        parse_mode='HTML'
    )

@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_exists(user_id=user_id) and check_user_phone_number_exists(user_id):
        await message.reply(get_translation('main_message', 'uz'), reply_markup=main_key(), parse_mode="HTML")
        await state.set_state(UserStates.main.state)
        set_user_state(user_id=user_id, state=UserStates.main.state)
    else:
        await message.reply(get_translation('start_message', 'uz'), parse_mode='HTML', reply_markup=phone_number_key())
        await state.set_state(UserStates.phone_number) 