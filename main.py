import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN



async def startup(dispatcher: Dispatcher):
    print('Bot is starting...')

async def shutdown(dispatcher: Dispatcher):
    print('Bot is shutting down...')

async def main():
    bot = Bot(token = BOT_TOKEN)
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass