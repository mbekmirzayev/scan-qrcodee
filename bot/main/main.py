import asyncio
from bot.loader import bot, dp
from bot import query


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
