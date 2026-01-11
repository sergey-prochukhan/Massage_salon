from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
import asyncio

order_han_router = Router()
#
# Определяем состояния
class OrderStates(StatesGroup):
    wait_user_name = State()
    wait_massage_type = State()
    wait_date = State()
    wait_contact = State()


#Обрабатываем кнопку "Согласен(а)"
@order_han_router.callback_query(F.data == "approve")
async def start_ordering(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text="Начнём..."
        )
        await asyncio.sleep(2)

        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text="Как к вам обращаться?"
        )
        await state.set_state(OrderStates.wait_user_name)  # Переходим в состояние
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")
    await callback.answer()

@order_han_router.message(OrderStates.wait_user_name)
async def get_massage_type(message: types.Message, state: FSMContext):
    user_t_id = message.from_user.id
    user_name = message.text  # Сохраняем ответ
    await state.update_data(name=user_name, user_id=user_t_id)  # Записываем в FSM

    await message.answer("Какой вид массажа вас интересует?")
    await state.set_state(OrderStates.wait_massage_type)

@order_han_router.message(OrderStates.wait_massage_type)
async def get_massage_type(message: types.Message, state: FSMContext):
    user_m_type = message.text  # Сохраняем ответ
    await state.update_data(massage_type=user_m_type)  # Записываем в FSM

    await message.answer("Когда вам было бы удобно прийти на массаж?")
    await state.set_state(OrderStates.wait_date)

@order_han_router.message(OrderStates.wait_date)
async def get_date(message: types.Message, state: FSMContext):
    user_date = message.text
    await state.update_data(date=user_date)

    await message.answer("Как с вами связаться?")
    await state.set_state(OrderStates.wait_contact)

@order_han_router.message(OrderStates.wait_contact)
async def get_contact(message: types.Message, state: FSMContext):
    user_cont_inf = message.text
    await state.update_data(contact=user_cont_inf)

    # Получаем все сохранённые данные
    data = await state.get_data()
    user_name = data.get("name")
    user_t_id = data.get("user_id")
    user_m_type = data.get("massage_type")
    user_date = data.get("date")
    user_cont_inf = data.get("contact")

    await message.answer(
        f"{user_name} Спасибо за заявку!\n"
        f"Вид массажа: {user_m_type}\n"
        f"Дата: {user_date}\n"
        f"Контакт: {user_cont_inf}\n"
        f"Ваш ID{user_t_id}\n"
        f"Подтвердите ваш заказ и мы скоро с вами свяжемся.\n"
        f"Чтобы вернуться в меню, нажмите /menu"
    )

    await state.clear()  # Очищаем FSM
