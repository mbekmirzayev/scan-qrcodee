from mailbox import Message

from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.main.main import dp, UserFormState


@dp.startup()
async def on_startup(bot: Bot):
    commands = [
        BotCommand(command="start", description="Qayta boshlash!"),
    ]
    await bot.set_my_commands(commands)



@dp.message(UserFormState.age, F.func(lambda message: message.text.isdigit()))
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UserFormState.phone_number)
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Telefon raqamni yuborish", request_contact=True))
    await message.answer(
        "Telefon raqamingizni yuborish uchun quyidagi tugmani bosing:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
