
# Базовый образ с Python
FROM python:3.11.14


#Устанавливаем UV через официальный бинарник (быстрее, чем pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

#Настройки для UV (ускоряют сборку и запуск)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy


#Рабочий каталог
WORKDIR /app

#Копируем файлы проекта
COPY . .


#Устанавливаем зависимости через UV
RUN uv pip install -r requirements.txt


#Команда запуска бота
CMD ["uv", "run", "python", "main.py"]
#test
