from aiogram import BaseMiddleware
from aiogram.types import Message
from handlers.states import UserStates
from config.settings import get_translation
from utils.utils import * 
from keyboards.keyboards import phone_number_key

class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        
        user_id = event.from_user.id
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name
        username = event.from_user.username
        
        if not user_exists(user_id):
            add_user(user_id, first_name, last_name, username)
            set_user_state(user_id, UserStates.phone_number.state)
            
            await event.answer(
                get_translation('start_message', 'uz'),
                reply_markup=phone_number_key(),
                parse_mode='HTML'
            )
            state = data['state']
            await state.set_state(UserStates.phone_number)
            return 
        
        return await handler(event, data)