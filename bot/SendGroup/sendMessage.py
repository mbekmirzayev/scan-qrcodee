from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.BotToken.bot_token import GROUP_CHAT_ID
from bot.main.main import dp, UserFormState


@dp.callback_query(F.data.in_(["tasdiq", "rad"]))
async def process_decision(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    action = callback.data

    if action == "tasdiq":
        # Foydalanuvchi ma'lumotlarini groupga yuborish
        text = (
            f"📥 Yangi foydalanuvchi:\n"
            f"Ismi: {data['first_name']}\n"
            f"Familiyasi: {data['last_name']}\n"
            f"Yoshi: {data['age']}\n"
            f"Telefon raqami: {data['phone_number']}"
        )
        await callback.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # Foydalanuvchiga markaz lokatsiyasini yuborish
        await callback.message.answer(" SUCCES✅")

    else:
        await callback.message.answer("Ma'lumotlaringiz rad etildi.")

@dp.message(UserFormState.phone_number, F.contact)
async def phone_handler(message: Message, state: FSMContext, callback=None):
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

# Callback handler
    await state.clear()
    await callback.answer()
