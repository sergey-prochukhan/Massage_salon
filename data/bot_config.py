import os
from aiogram.types import FSInputFile

all_img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
all_misc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc')

#images links
hello = FSInputFile(os.path.join(all_img_dir, 'hello.jpg'))
int_pic = FSInputFile(os.path.join(all_img_dir, 'int_pic.jpg'))
out_pic = FSInputFile(os.path.join(all_img_dir, 'out_pic.jpg'))
sale_pic = FSInputFile(os.path.join(all_img_dir, 'sale_pic.jpg'))
help_pic = FSInputFile(os.path.join(all_img_dir, 'help_pic.jpeg'))
spec_pic = FSInputFile(os.path.join(all_img_dir, 'spec_pic.jpg'))
proc_pic = FSInputFile(os.path.join(all_img_dir, 'proc_pic.jpg'))

privacy_file = FSInputFile(os.path.join(all_misc_dir, 'privacy.docx'))

sale_text = "Текст Акции\n"

sale_date = "дата и время акции"




services_text = (
    "💆Классический массаж всего тела\n"    # — ваша перезагрузка! Снимем напряжение, улучшим кровообращение и вернём энергию. Длительность: 60–90 мин.\n"
    "🍑Антицеллюлитный массаж \n" # — путь к гладкой коже! Активируем обмен веществ, уменьшаем объёмы и возвращаем упругость. Рекомендуемый курс: 8–12 сеансов.\n"
    "😌Массаж ШВЗ\n" # — быстрое снятие напряжения! Уберём скованность в шее, улучшим кровоток и поможем при головных болях. Всего 20–30 мин.\n"
    "🌿Лимфодренажный массаж\n \n"  # — детокс для вашего тела! Стимулируем лимфоток, снимаем отёки и обновляем кожу. Идеально после интенсивных тренировок или перелётов.\n"
    "Нажми «Записаться на массаж», чтобы попасть к нам на приём✨."

)

#db = 'data/clients.db'