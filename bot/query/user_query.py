# bot/query/user_query.py
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.loader import dp
from bot.states import UserFormState


@dp.message(CommandStart())
async def inline_handler(message: Message, state: FSMContext):
    await state.set_state(UserFormState.first_name)
    await message.answer("Ismingizni kiriting: ")


@dp.message(UserFormState.first_name)
async def first_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(UserFormState.last_name)
    await message.answer("Familyangizni kiriting:")


@dp.message(UserFormState.last_name)
async def last_handler(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(UserFormState.age)
    await message.answer("Yoshingizni kiriting:")
