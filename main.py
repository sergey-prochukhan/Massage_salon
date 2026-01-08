import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
#from dotenv import load_dotenv
from handlers.main_handlers import main_han_router
from handlers.menu_handlers import menu_han_router

#load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(main_han_router, menu_han_router)

async def main():
    logger.info("Запуск бота...")

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())