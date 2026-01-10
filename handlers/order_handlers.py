from aiogram import Router
from aiogram.types import CallbackQuery
import asyncio

order_han_router = Router()

@order_han_router.callback_query(lambda c: c.data == "approve")
async def start_ordering(callback: CallbackQuery):
        try:
            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Начнём...")
            
            await asyncio.sleep(2)

            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Какой вид массажа вас интересует?")
            
            await asyncio.sleep(2)

            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Когда вам было бы удобно прийти на массаж?")
            
            await asyncio.sleep(2)

            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Как с вами связаться?")
            
            await asyncio.sleep(2)

            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Спасибо за заявку, мы скоро с вами свяжемся. Что бы вернуться в меню нажмите /menu")
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

        await callback.answer()
