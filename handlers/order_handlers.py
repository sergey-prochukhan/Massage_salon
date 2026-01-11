from aiogram import Router, types, F
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
import asyncio
import sqlite3

order_han_router = Router()

user_name = "name"
user_t_id = "user_id"
user_nicname = "nicname"
user_m_type = "massage_type"
user_date = "date"
user_cont_inf = "contact"

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

#Собираем данные о клиенте по его ответам
@order_han_router.message(OrderStates.wait_user_name)
async def get_massage_type(message: types.Message, state: FSMContext):
    user_t_id = message.from_user.id
    user_nicname = message.from_user.username
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
    nikname = data.get("user_nikname")
    user_t_id = data.get("user_id")
    user_m_type = data.get("massage_type")
    user_date = data.get("date")
    user_cont_inf = data.get("contact")

    await message.answer(
        f"{user_name} Спасибо за заявку!\n"
        f"Вид массажа: {user_m_type}\n"
        f"Дата: {user_date}\n"
        f"Контакт: {user_cont_inf}\n"
        f"Подтвердите ваш заказ и мы скоро с вами свяжемся.\n"
        f"Чтобы вернуться в меню, нажмите \n Меню", 
        reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Принять✅", callback_data="confirm"),  # Подтвердить
                    InlineKeyboardButton(text="Изменить✎", callback_data="approve"),  # Внести изменения
                ],
                [
                    InlineKeyboardButton(text="←Меню", callback_data="back")
                ]
            ])
        )


@order_han_router.callback_query(F.data == "confirm")
async def add_order(callback: CallbackQuery, state: FSMContext):
    try:
        # Получаем данные из FSM
        data = await state.get_data()
        user_t_id = data.get("user_id")
        nikname = data.get("user_nikname")
        user_name = data.get("name")
        user_m_type = data.get("massage_type")
        user_date = data.get("date")
        user_cont_inf = data.get("contact")

        # Подключение к БД и создание таблицы
        db_con = sqlite3.connect('data/clients.db')
        db_cur = db_con.cursor()
        db_cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER,
                username TEXT NOT NULL,
                nicname TEXT NOT NULL,
                type TEXT NOT NULL,
                date TEXT NOT NULL,
                cont TEXT NOT NULL
            )
        ''')

        # Вставка данных
        db_cur.execute(
            "INSERT INTO clients (id, nicname, name, type, date, cont) VALUES (?, ?, ?, ?, ?)",
            (user_t_id, user_nikname, user_m_type, user_date, user_cont_inf)
        )
        db_con.commit()
        db_con.close()
        group_message = (
            f"📋 Новая заявка!\n\n"
            f"Имя: {user_name}\n"
            f"Контакт: {nikname}\n"
            f"ID пользователя: {user_t_id}\n"
            f"Вид массажа: {user_m_type}\n"
            f"Дата: {user_date}\n"
            f"Контакт: {user_cont_inf}"
        )
        await callback.bot.send_message(
            chat_id='-1003544458506',
            text=group_message)
        
        await callback.answer("Заявка успешно сохранена!")
        await state.clear()

    except Exception as e:
        await callback.answer(f"Не удалось сохранить: {e}")
                
    await state.clear()  # Очищаем FSM
