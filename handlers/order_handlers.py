from aiogram import Router, types, F
from aiogram.filters.command import Command


order_han_router = Router()

@order_han_router.message(Command("ordering"))
async def message(message: types.Message):
    await message.answer("Всё получилось", alert=True)

#await callback.answer()