from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from data.bot_config import services_text

# Инициализация роутера
menu_han_router = Router()
#images links
hello = "https://disk.yandex.ru/get/mky90I09j4a4mw"
int_pic = "https://disk.yandex.ru/get/-hkTCwDDmS0S-Q"
out_pic = "https://disk.yandex.ru/get/7ddIVQMkvprBmg"
sale_pic = "https://disk.yandex.ru/get/r_tDrWKvq3u37w"
help_pic = "https://disk.yandex.ru/get/kZQ1DV7hPaOTdQ"
spec_pic = "https://disk.yandex.ru/get/b23AAYwefRk1lQ"
proc_pic = "https://disk.yandex.ru/get/ABiY54bGDF_vAg"



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


# Хендлер для /start
@menu_han_router.message(Command("start"))
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

    elif callback.data == "contacts":
        media = InputMediaPhoto(
            media=out_pic,  
            caption=(
                "Адрес\n"
                "Телефон\n"
                "e-mail\n"
                "Телеграм\n"
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
    
    elif callback.data == "spec":
        media = InputMediaPhoto(
            media=spec_pic,  
            caption=(
                "Галина\n"
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
                reply_markup=back_kb  # Меняем клавиатуру на «Назад»
            )
        except Exception as e:
            await callback.answer(f"Ошибка: {e}")

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

    #Обрабатываем кнопку "Согласен(а)"
    
    elif callback.data == "approve":
        await callback.answer(f"Функционал в разработке\n Будет доступен со следующим обновлением.", show_alert=True)

    #Обрабатываем кнопку "Скачать"
#elif callback.data == "sendmedoc":
       # try:
       #     await callback.message.answer_document(
      #      document=privacy_file,
     #       caption="Вот ваш файл!",
      #      reply_markup=order_kb
       # )
        
       #     await callback.message.delete()
        # Уведомляем пользователя всплывающим окном
        #    await callback.answer("Соглашение отправлено. После ознакомления нажмите кнопку Согласен(а) что бы продолжить.", show_alert=True)
        #Удаляем сообщение
        #    await callback.message.delete()
       # except FileNotFoundError:
       #     await callback.answer("Ошибка: файл не найден!", show_alert=True)
       # except Exception as e:
          #  await callback.answer(f"Ошибка: {e}", show_alert=True)

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