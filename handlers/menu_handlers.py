from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from bot_config import services_text, hello, int_pic, out_pic, sale_pic, spec_pic, proc_pic, help_pic, privacy_file
from bot_config import spec_pic, spec2_pic, spec3_pic, spec4_pic


# Инициализация роутера
menu_han_router = Router()

# Основная клавиатура меню
main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💆                Услуги                💆", callback_data="serv")],
    [InlineKeyboardButton(text="📞              Контакты              📞", callback_data="contacts")],
    [InlineKeyboardButton(text="⭐         Наши специалисты         ⭐", callback_data="spec")],
    [InlineKeyboardButton(text="💬               Помощь               💬", callback_data="help")],
    [InlineKeyboardButton(text="📝       Записаться на массаж       📝", callback_data="order")]
])

order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👍              Согласен(а)               👍", callback_data="approve")],
    [InlineKeyboardButton(text="📝          Скачать документ           📝", callback_data="sendmedoc")],
    [InlineKeyboardButton(text="← Назад", callback_data="back")]
])

# Приветственный текст
hello_text = ("""Здравствуйте! 👋
Я — виртуальный помощник массажного салона [Название]. 
Готов помочь вам:
-подобрать подходящую процедуру;
-узнать расписание свободных окон;
-записаться на сеанс;
-получить консультацию по ценам и акциям.
Чтобы начать, выберите интересующую тему ниже"""
)
# Клавиатура «Назад»
back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝       Записаться на массаж       📝", callback_data="order")],
    [InlineKeyboardButton(text="← Назад", callback_data="back")]
    
])

@menu_han_router.message(Command("get_chat_id"))
async def getting_chat_id(message: types.Message):
    chat_id=message.chat.id
    await message.answer(f"{chat_id}")

# Хендлер для /start
@menu_han_router.message(Command("start"))
@menu_han_router.message(Command("menu"))
async def main_board(message: types.Message):
    await message.answer_photo(
        photo=hello,
        caption=hello_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨                Меню                ✨", callback_data="menubtn")]
        ])
    )

# Хендлер для callback-запросов
@menu_han_router.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    # Обрабатываем кнопку «Услуги»
    if callback.data == "serv":
        media = InputMediaPhoto(
            media=proc_pic, 
            caption=services_text
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=back_kb  # Меняем клавиатуру на «Назад»
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")
    
    # Открываем главное меню
    elif callback.data == "menubtn":
        media = InputMediaPhoto(
            media=hello,  
            caption=hello_text
            )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=main_menu_kb  
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")
    
    #Кнопка "Контакты"
    elif callback.data == "contacts":
        media = InputMediaPhoto(
            media=out_pic,  
            caption=(
                "Адрес Ленинград, 3-я улица Строителей,\n дом 25, квартира 12\n"
                "Телефон +7(999)888-77-66\n"
                "e-mail massag@horoshiy.ru\n"
                "Телеграм @aphonasiy_bot\n"
                "Нажми «Назад», чтобы вернуться."
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=back_kb  # Меняем клавиатуру на «Назад»
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    #Листаем специалистов
    elif callback.data == "spec":
        media = InputMediaPhoto(
            media=spec_pic,  
            caption=(
                "Алина\n"
                "Мастер универсал\n"
                "Стаж 10 лет\n"
                "Диплом массажиста, сертификат, грамота\n \n"     #это могут быть ссылки на документы
                "Нажми «Записаться на массаж», чтобы попасть к ней на приём."
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏪", callback_data="spec_4"),  # Предыдущая специалист
                    InlineKeyboardButton(text="⏩", callback_data="spec_2"),  # Следующий специалист   
                ],
                [
                    InlineKeyboardButton(text="Записаться📝", callback_data="order"),
                    InlineKeyboardButton(text="←Меню", callback_data="back")
                ]
                ])
                )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    elif callback.data == "spec_2":
        media = InputMediaPhoto(
            media=spec2_pic,  
            caption=(
                "Степан\n"
                "Дровосек\n"
                "Избавит вас от целлюлита за один сеанс\n"
                "7 классов школы №2 х. Обильный\n \n"     #это могут быть ссылки на документы
                "Нажми «Записаться на массаж», чтобы попасть к нему на... массаж."
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏪", callback_data="spec"),  # Предыдущая специалист
                    InlineKeyboardButton(text="⏩", callback_data="spec_3"),  # Следующий специалист   
                ],
                [
                    InlineKeyboardButton(text="Записаться📝", callback_data="order"),
                    InlineKeyboardButton(text="←Меню", callback_data="back")
                ]
                ])
                )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    elif callback.data == "spec_3":
        media = InputMediaPhoto(
            media=spec3_pic,  
            caption=(
                "Галина\n"
                "Мастер массажа ШВЗ\n"
                "Вложит душу в ваши позвонки\n"
                "Если честно коллектив её побаивается...\n \n"     #это могут быть ссылки на документы
                "Нажми «Записаться на массаж», чтобы записаться к ней  на приём."
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏪", callback_data="spec_2"),  # Предыдущая специалист
                    InlineKeyboardButton(text="⏩", callback_data="spec_4"),  # Следующий специалист   
                ],
                [
                    InlineKeyboardButton(text="Записаться📝", callback_data="order"),
                    InlineKeyboardButton(text="←Меню", callback_data="back")
                ]
                ])
                )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    elif callback.data == "spec_4":
        media = InputMediaPhoto(
            media=spec4_pic,  
            caption=(
                "Ольга\n"
                "Мастер лимфодренажного массажа\n"
                "Стаж 7 лет\n"
                "Любителям острых ощущений стоит записаться к ней на массаж. Новые незабываемые ощущения гарантируем...\n"
                "Нажми «Записаться на массаж», чтобы записаться к ней на приём."
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup= InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⏪", callback_data="spec_3"),  # Предыдущая специалист
                    InlineKeyboardButton(text="⏩", callback_data="spec"),  # Следующий специалист   
                ],
                [
                    InlineKeyboardButton(text="Записаться📝", callback_data="order"),
                    InlineKeyboardButton(text="←Меню", callback_data="back")
                ]
                ])
                )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")
  
    #Обработка кнопки "Помощь"
    elif callback.data == "help":
        media = InputMediaPhoto(
            media=help_pic,  
            caption=(
                "раздел ещё в стадии разработки\n"
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="← Назад", callback_data="back")]
                ])  # Меняем клавиатуру на «Назад»
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    #Обрабатываем кнопку "Заказать"
    elif callback.data == "order":
        media = InputMediaPhoto(
            media=int_pic,  
            caption=(
                "Перед тем как мы продолжим необходимо\n"
                "дать согласие на обработку пользовательских данных\n"
            )
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=order_kb  # Добавляем кнопку согласия на обработку пользовательских данных, скачивание пользовательского соглашения и кнопку назад
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")
  

    #Обрабатываем кнопку "Скачать"
    elif callback.data == "sendmedoc":
        try:
            await callback.message.answer_document(
            document=privacy_file,
            caption="Вот ваш файл!",
            reply_markup=order_kb
        )
        
            await callback.message.delete()
        #Уведомляем пользователя всплывающим окном
            await callback.answer("Соглашение отправлено. После ознакомления нажмите кнопку Согласен(а) что бы продолжить.", show_alert=True)
        #Удаляем сообщение
            await callback.message.delete()
        except FileNotFoundError:
            await callback.answer("Ошибка: файл не найден!", show_alert=True)
        except Exception as e:
            await callback.answer(f"Ошибка: {e}", show_alert=True)

    # Обрабатываем кнопку «Назад»
    
    elif callback.data == "back":
        media = InputMediaPhoto(
            media=hello,
            caption=hello_text
        )
        try:
            await callback.bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=media,
                reply_markup=main_menu_kb  # Возвращаем основное меню
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

    # Отвечаем на callback (убираем «часики» у кнопки)
    await callback.answer()