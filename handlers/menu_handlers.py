from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
import os
from bot_config import all_media_dir, privacy_file

# Инициализация роутера
menu_han_router = Router()



# Загрузка файлов
hello = FSInputFile(os.path.join(all_media_dir, 'hello.jpg'))
int_pic = FSInputFile(os.path.join(all_media_dir, 'int_pic.jpg'))
out_pic = FSInputFile(os.path.join(all_media_dir, 'out_pic.jpg'))
proc_pic = FSInputFile(os.path.join(all_media_dir, 'proc_pic.jpg'))
spec_pic = FSInputFile(os.path.join(all_media_dir, 'spec_pic.jpg'))
help_pic= FSInputFile(os.path.join(all_media_dir, 'help_pic.jpeg'))

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
hello_text = (
    "Здравствуйте!\n\n"
    "Это приветственное сообщение с картинкой и меню.\n"
    "Выберите действие ниже:"
)

# Клавиатура «Назад»
back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="← Назад", callback_data="back")]
])


# Хендлер для /start
@menu_han_router.message(Command("start"))
async def main_board(message: types.Message):
    await message.answer_photo(
        photo=hello,
        caption=hello_text,
        reply_markup=main_menu_kb
    )

# Хендлер для callback-запросов
@menu_han_router.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    # Обрабатываем кнопку «Услуги»
    if callback.data == "serv":
        media = InputMediaPhoto(
            media=proc_pic, 
            caption=(
                "Услуга 1)\n"
                "Услуга 2)\n"
                "Услуга 3)\n"
                "Услуга 4)\n"
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
                "Галина Костоправова\n"
                "Мастер копчикового массажа\n"
                "Диплом копчиколома 4 разряда\n"
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

    elif callback.data == "help":
        media = InputMediaPhoto(
            media=help_pic,  
            caption=(
                "ТАК ТАК ТАК!!!\n"
                "ЩА РАЗБЕРЁМСЯ\n"
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
            caption="Вот ваш файл!"
        )
        #Удаляем сообщение
            await callback.message.delete()
        # Уведомляем пользователя всплывающим окном
            await callback.answer("Файл отправлен!", show_alert=True)
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