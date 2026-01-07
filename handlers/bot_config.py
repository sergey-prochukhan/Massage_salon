import os
from aiogram.types import FSInputFile

# Путь к папке с изображениями
all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
all_misc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc')

sale_pic = FSInputFile(os.path.join(all_media_dir, 'sale_pic.jpg'))

sale_text = "Текст Акции\n"

sale_date = "дата и время акции"

privacy_file = FSInputFile(os.path.join(all_misc_dir, 'privacy.docx'))