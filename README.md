# Instruction to Trade cars application

## Настройка окружения

### pipenv

Подробнее о __pipenv__: <https://semakin.dev/2020/04/pipenv/>.

Настариваем виртуальное окружение проекта.

В проект устанавливаем пакеты через __pipenv__

Установка Django: *pipenv install django* – после первого пакета создаются файлы __Pipfile__ и __Pipfile.lock__. Так же устанавливаем другие пакеты и модули.

Активация виртуалки в проекте: *pipenv shell*. *exit* – для деакцивации.

### Docker Compose & PostgreSQL

Инструкция по разворачиванию Docker с Docker-compose с Postgres: <https://django.fun/tutorials/dokerizaciya-django-s-pomoshyu-postgres-gunicorn-i-nginx/>.

Убить процесс занимающий порт: <https://ask-dev.ru/info/10471/find-and-kill-process-locking-port-3000-on-mac>.

__? Как сохранять изменения в проекте между запусками докера ?__

Собрать образ и поднять докер компоуз: *docker-compose up -d --build*.

Посмотреть логи активного контейнера: *docker-compsoe logs -f*.

Обращаться к сервисам (web – приложение, db – база данных) через запущенный контейнер: *docker-compose exec web(db) ...*.

Остановить контейнер и удалить его: *docker-compose down -v*.

## Настройка Django проекта

Создадим новый проект: *django-admin startproject main_project .* - точка установит проект в данную папку, уберёт лишнюю вложенность из проекта.

Запустим три приложения (Buyer, Dealership and Supplier) через *python manage.py startapp*

### Настройка __settings.py__ в __main_project__

Регистрируем все приложения и все сторонние пакеты в __settings.py__. Привязываем пути к приложениям с адресами в __urls.py__.

Для каждого приложения в проекте создаём модели таблиц.
