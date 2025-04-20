from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    phone_number = State()
    main = State()