from aiogram import Router
from aiogram.types import CallbackQuery

order_han_router = Router()

@order_han_router.callback_query(lambda c: c.data == "approve")
async def start_ordering(callback: CallbackQuery):
        try:
            await callback.bot.send_message(
                 chat_id=callback.message.chat.id,
                 text="Работает!")
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

        await callback.answer()
