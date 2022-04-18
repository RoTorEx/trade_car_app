# Файл для сборки образа приложения

# Получаем образ Python
FROM python:3.10-alpine

# Устанавливаем рабочую директорию образа
WORKDIR /usr/src/app

# Настройка окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# установка psycopg2 и зависимостей
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Копирование файлов pipenv 
COPY Pipfile ./
COPY Pipfile.lock ./

# Уставнока pipenv и зависимостей приложения
RUN pip install pipenv
RUN set -ex && pipenv install --deploy --system

# Копирование и настрйока скрипта entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Копирование проекта
COPY . .

# Команда запуска проекта при развёртывании через Docker
# CMD ["python", "manage.py", "runserver"]

# Запуск скрипта entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
