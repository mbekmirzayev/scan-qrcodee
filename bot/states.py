from aiogram.fsm.state import State, StatesGroup

class UserFormState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()
