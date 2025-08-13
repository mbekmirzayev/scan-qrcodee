import asyncio

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton, Message, CallbackQuery, KeyboardButton, BotCommand
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
TOKEN = "8031838912:AAFnANJJDDsc0aojbXopnsdI5QVm5trpWik"
GROUP_CHAT_ID =  -1002767989520

dp = Dispatcher()

from aiogram.types import BotCommand

@dp.startup()
async def on_startup(bot: Bot):
    commands = [
        BotCommand(command="start", description="Qayta boshlash!"),
    ]
    await bot.set_my_commands(commands)


class UserFormState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone_number = State()


@dp.message(Command("getid"))
async def get_chat_id(message: Message):
    await message.answer(f"yout user id: <code>{message.chat.id}</code>")
    await message.answer(f"current chat id : <code>{message.chat.id}</code>")


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

@dp.message(UserFormState.phone_number, F.contact)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)

    data = await state.get_data()
    first_name = data["first_name"]
    last_name = data["last_name"]
    age = data["age"]
    phone = data["phone_number"]

    text = (
        f"Hurmatli mijoz!\n"
        f"Ismingiz: {first_name}\n"
        f"Familiyangiz: {last_name}\n"
        f"Yoshingiz: {age}\n"
        f"Telefon raqam: {phone}"
    )

    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text="Tasdiqlansin", callback_data="tasdiq"),
        InlineKeyboardButton(text="Rad qilinsin", callback_data="rad")
    )

    await message.answer(text, reply_markup=ikb.as_markup())
@dp.message()
async def get_chat_id(message: Message):
    await message.answer(f"Guruh ID: {message.chat.id}")
@dp.callback_query(F.data.in_(["tasdiq", "rad"]))
async def process_decision(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    action = callback.data

    if action == "tasdiq":
        text = (
            f"📥 Yangi foydalanuvchi:\n"
            f"Ismi: {data['first_name']}\n"
            f"Familiyasi: {data['last_name']}\n"
            f"Yoshi: {data['age']}\n"
            f"Telefon raqami: {data['phone_number']}"
            f"user id : {data[]}"
        )
        await callback.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)


    else:
        await callback.message.answer("Ma'lumotlaringiz rad etildi.")

    await state.clear()
    await callback.answer()

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())