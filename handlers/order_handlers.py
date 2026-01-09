from aiogram import Router, types, F
from aiogram.filters.command import Command
from main import bot


order_han_router = Router()

@order_han_router.message(Command("ordering"))
async def show_alert_ordering(callback_query: types.CallbackQuery):
    await bot.answer.callback_query(callback_query.id,
    text="Всё получилось", 
    show_alert=True
    )

#await callback.answer()
