from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
import asyncio
import sqlite3
import re
from handlers.menu_handlers import menu_han_router, main_board

GROUP_CHAT_ID = "-1003544458506"

order_han_router = Router()

def escape_markdown(text: str) -> str:
    """Экранирует спецсимволы Markdown: * _ [ ] ( ) ~ ` > # + - | { } . !"""
    if not text:
        return ""
    escaped = re.sub(r'([\*_\[\]\(\)\~\`\>\#\+\-\|\{\}\.\!])', r'\\\1', text)
    return escaped

def is_valid_markdown(text: str) -> bool:
    """Проверяет сбалансированность Markdown-сущностей: [ ], * *, _ _"""
    stack = []
    for char in text:
        if char in ['[', '*', '_']:
            stack.append(char)
        elif char == ']':
            if not stack or stack.pop() != '[':
                return False
        elif char == '*':
            if stack and stack[-1] == '*':
                stack.pop()  # Закрываем пару **
            else:
                stack.append('*')
        elif char == '_':
            if stack and stack[-1] == '_':
                stack.pop()
            else:
                stack.append('_')
    return len(stack) == 0

class OrderStates(StatesGroup):
    wait_user_name = State()
    wait_massage_type = State()
    wait_date = State()
    wait_contact = State()

def get_user_link(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"
    else:
        name = escape_markdown(user.first_name or "Пользователь")
        return f"[{name}](tg://user?id={user.id})"

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
        await state.set_state(OrderStates.wait_user_name)
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")
        await callback.answer()

def validate_name(text: str) -> tuple[bool, str]:
    if not text:
        return False, "Имя не может быть пустым."
    if len(text.strip()) < 2:
        return False, "Имя должно содержать хотя бы 2 символа."
    if len(text) > 50:
        return False, "Имя слишком длинное (максимум 50 символов)."
    if not all(c.isalpha() or c.isspace() or c in "-'" for c in text):
        return False, "Имя может содержать только буквы, пробелы, дефисы и апострофы."
    return True, None

@order_han_router.message(OrderStates.wait_user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    try:
        is_valid, error = validate_name(message.text)
        if not is_valid:
            await message.answer(error)
            return

        user_t_id = message.from_user.id
        user_link = get_user_link(message.from_user)
        user_name = message.text.strip()

        await state.update_data(name=user_name, user_id=user_t_id, user_link=user_link)
        await message.answer("Какой вид массажа вас интересует?")
        await state.set_state(OrderStates.wait_massage_type)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}. Попробуйте ещё раз.")


def validate_massage_type(text: str) -> tuple[bool, str]:
    if not text:
        return False, "Пожалуйста, укажите вид массажа."
    if len(text.strip()) < 3:
        return False, "Описание вида массажа должно быть не короче 3 символов."
    if len(text) > 100:
        return False, "Слишком длинное описание (максимум 100 символов)."
    return True, None

@order_han_router.message(OrderStates.wait_massage_type)
async def get_massage_type(message: types.Message, state: FSMContext):
    is_valid, error = validate_massage_type(message.text)
    if not is_valid:
        await message.answer(error)
        return

    user_m_type = message.text.strip()
    await state.update_data(massage_type=user_m_type)
    await message.answer("Когда вам было бы удобно прийти на массаж?")
    await state.set_state(OrderStates.wait_date)

from datetime import datetime

def validate_date(text: str) -> tuple[bool, str]:
    text = text.strip()
    if not text:
        return False, "Дата не может быть пустой."

    if not re.match(r"^\d{1,2}[./-]\d{1,2}[./-]\d{4}$", text):
        return False, "Введите дату в формате ДД.ММ.ГГГГ (например, 15.03.2025)."

    text = re.sub(r"[./-]", ".", text)
    try:
        day, month, year = map(int, text.split("."))
        date = datetime(year, month, day)
        if date.date() < datetime.now().date():
            return False, "Дата не может быть в прошлом."
        return True, None
    except ValueError:
        return False, "Некорректная дата. Проверьте день, месяц и год."

@order_han_router.message(OrderStates.wait_date)
async def get_date(message: types.Message, state: FSMContext):
    is_valid, error = validate_date(message.text)
    if not is_valid:
        await message.answer(error)
        return

    user_date = message.text.strip()
    await state.update_data(date=user_date)
    await message.answer("Как с вами связаться? Укажите телефон или Telegram.")
    await state.set_state(OrderStates.wait_contact)


def validate_contact(text: str) -> tuple[bool, str]:
    text = text.strip()
    if not text:
        return False, "Контакт не может быть пустым."

    phone_pattern = r"^(\+7|8)[\d]{10}$"
    if re.match(phone_pattern, re.sub(r"[\s\-\(\)]", "", text)):
        return True, None

    if text.startswith("@") and 5 <= len(text) <= 32:
        return True, None

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_pattern, text):
        return True, None

    tg_link_pattern = r"^(https?://)?t\.me/[a-zA-Z0-9_]{5,}$"
    if re.match(tg_link_pattern, text):
        return True, None

    return False, (
        "Введите корректный контакт:\n"
        "- Телефон (+7ХХХХХХХХХХ или 8ХХХХХХХХХХ)\n"
        "- @username в Telegram\n"
        "- Email\n"
        "- Ссылка на Telegram (t.me/...)"
    )


@order_han_router.message(OrderStates.wait_contact)
async def get_contact(message: types.Message, state: FSMContext):
    is_valid, error = validate_contact(message.text)
    if not is_valid:
        await message.answer(error)
        return

    user_cont_inf = message.text.strip()
    await state.update_data(contact=user_cont_inf)


    data = await state.get_data()
    user_name = escape_markdown(data.get("name", ""))
    user_m_type = escape_markdown(data.get("massage_type", ""))
    user_date = escape_markdown(data.get("date", ""))
    user_link = data.get("user_link", "")

    final_text = (
        f"{user_name}, спасибо за заявку!\n"
        f"Вид массажа: {user_m_type}\n"
        f"Дата: {user_date}\n"
        f"Контакт: {escape_markdown(user_cont_inf)}\n"
        f"Профиль: {user_link}\n"
        "Подтвердите ваш заказ, и мы скоро с вами свяжемся."
    )

    # Создаём клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять✅", callback_data="confirm"),
            InlineKeyboardButton(text="Изменить✎", callback_data="approve"),
        ],
        [
            InlineKeyboardButton(text="←Меню", callback_data="back")
        ]
    ])

    # Логирование для отладки
    print("=== ОТЛАДКА: ТЕКСТ ДЛЯ ОТПРАВКИ ===")
    print(final_text)
    print("Корректный Markdown:", is_valid_markdown(final_text))
    print("===========================\n")

    if is_valid_markdown(final_text):
        await message.answer(
            final_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # Если разметка сломана — отправляем как простой текст (без экранирования)
        await message.answer(final_text.replace('\\', ''), reply_markup=keyboard)



@order_han_router.callback_query(F.data == "confirm")
async def add_order(callback: CallbackQuery, state: FSMContext):
    db_con = None
    try:
        data = await state.get_data()
        user_t_id = data.get("user_id")
        user_link = data.get("user_link", "")
        user_name = escape_markdown(data.get("name", ""))
        user_m_type = escape_markdown(data.get("massage_type", ""))
        user_date = escape_markdown(data.get("date", ""))
        user_cont_inf = escape_markdown(data.get("contact", ""))

        # Подключение к БД
        db_con = sqlite3.connect('data/clients.db')
        db_cur = db_con.cursor()


        db_cur.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER,
                profile_link TEXT NOT NULL,
                client_name TEXT NOT NULL,
                type TEXT NOT NULL,
                date TEXT NOT NULL,
                cont TEXT NOT NULL
            )
        ''')

        db_cur.execute(
            "INSERT INTO clients (id, profile_link, client_name, type, date, cont) VALUES (?, ?, ?, ?, ?, ?)",
            (user_t_id, user_link, user_name, user_m_type, user_date, user_cont_inf)
        )
        db_con.commit()

        # Сообщение для группы
        group_message = (
            f"📋 Новая заявка!\n\n"
            f"Имя: {user_name}\n"
            f"Профиль: {user_link}\n"
            f"ID пользователя: {user_t_id}\n"
            f"Вид массажа: {user_m_type}\n"
            f"Дата: {user_date}\n"
            f"Контакт: {user_cont_inf}"
        )

        if is_valid_markdown(group_message):
            await callback.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=group_message,
                parse_mode="Markdown"
            )
        else:
            await callback.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=group_message.replace('\\', '')
            )

        # 1. Показываем alert-уведомление (всплывающее окно)
        await callback.answer("Заявка принята! Спасибо за обращение.", show_alert=True)


        # 2. Очищаем состояние FSM
        await state.clear()

        # 3. Вызываем главное меню (как если бы пользователь ввёл /menu)
        await main_board(callback.message)

    except Exception as e:
        # В случае ошибки — alert с ошибкой
        await callback.answer(f"Не удалось сохранить: {e}", show_alert=True)
    finally:
        if db_con:
            db_con.close()