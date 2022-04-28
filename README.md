# Instruction to Trade cars application

## Настройка окружения

### pipenv

Подробнее о __pipenv__ [тут](https://semakin.dev/2020/04/pipenv/).

Настариваем виртуальное окружение проекта. В проект устанавливаем пакеты через __pipenv__.

Установка Django: *pipenv install django* – после первого пакета создаются файлы __Pipfile__ и __Pipfile.lock__. 

Так же устанавливаем другие пакеты и модули.
Активация виртуалки в проекте: *pipenv shell*. *exit* – для деакцивации.

### Docker Compose & PostgreSQL

Инструкция по разворачиванию Docker с Docker-compose с Postgres [здесь](https://django.fun/tutorials/dokerizaciya-django-s-pomoshyu-postgres-gunicorn-i-nginx/).

[Команды для работы процессами в портах](https://ask-dev.ru/info/10471/find-and-kill-process-locking-port-3000-on-mac).

Собрать образ и поднять докер компоуз: *docker-compose up -d --build*. Посмотреть логи активного контейнера: *docker-compsoe logs -f*.

Обращаться к сервисам (web – приложение, db – база данных) через запущенный контейнер: *docker-compose exec web(db) ...*. Остановить контейнер и удалить его: *docker-compose down -v*.

## Django

### Создание Django проекта

Создадим новый проект: *django-admin startproject main_project .* - точка установит проект в данную папку, уберёт лишнюю вложенность из проекта.

Устанвоим необходимые приложения в *python manage.py startapp*.

### Регистрация приложений в __settings.py__ в __core__. Создание моделей и регистрация

Регистрируем все приложения и все сторонние пакеты в __settings.py__, настраиваем переменные и базу данных. 

Привязываем пути к приложениям с адресами в __urls.py__.
Для каждого приложения в проекте создаём модели таблиц, модели регистрируются в __admin.py__ приложения.

## Django Rest Framework

### Создание API приложения

В каждом приложении прописаны сериализаторы и вьюсеты. Все вьюсеты вынесены в роутеры в __admoin__ __urls.py__ и привязаны к адресам.

#### 1. Представления (View)

Прописываем класс __...APIView(generics.ListAPIView)__ в __views.py__.

Во вьюсете есть две переменные __queryset__ и __serializer_class__. Первая принимает значения из базы, вторая ссылается на класс для сериализации данных их таблицы в JSON строку.

Классы представления имеют набор стандартных методов (GET, POST и тд) и автоматически их обрабатывают при поступлении соотвествующих запросов.

При написании [вьюх](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions) можно наследовании от класса __viewsets.ModelViewSet__, который наследуется под капотом от (mixins.CreateModelMixin [create()] – создание, mixins.RetrieveModelMixin [retrieve()] – выделение, mixins.UpdateModelMixin [update()], [partial_update()] – изменение, mixins.DestroyModelMixin [destroy()] – удаление, mixins.ListModelMixin [list()] – получение списка статей, GenericViewSet – базовый класс)  под капотом имеет все необходимые методы для работы с API. Или использовать некотрые наследуемые классы выборочно для регулирования функционала API.


#### 2. Сериализатор (Serializer)

Прописываем класс для сериализации данных – __...Serializer(serializer.ModelSeriaizer)__ в новом файле __serializer.py__. Туда, в классы моделей прописываем мета класс с переменной __model__, которая принимает модель приложения. В __fields__, соответственно, кортежем перечисляются поля для сериализации.


#### 3. Маршрутизация (Router)

В __admin.py__ -> __urls.py__ указываем маршрут получения API. Прописанные [роутеры](https://www.django-rest-framework.org/api-guide/routers/) позволяют обращаться по адресу (<http://0.0.0.0:8000/api/buyer/>) работать GET и POST запросами. И при добавлении идентификатора записи к адресу (/<int:pk>/) для PUT, PUTCH, DELETE запросов. __Routers.register__ 3им аргументом может принимать __base_name__, который явлется обязательным при отсутвсвии во вьюсете __queryset__, по которому проиходит подстановка.

## Скрипт для заполнения таблиц базы данных



## Подключение Django Toold Bar

[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

Установка __django-debug-toolbar__ через __pipenv__. Прописываем установленный пакет в __INSTALLED_APPS__, в коллекцию __MIDDLEWARE__ так же указываем установленный пакет. Потом прописываем новую коллекцию __INTERNAL_IPS__ со списком отслеживаемых IP-адресов.

Так же необходимо добавить __DEBUG_TOOLBAR_CONFIG__ для корректной работы его с __DRF__.


## Подключение Swagger

[Swagger](https://gadjimuradov.ru/post/swagger-dlya-django-rest-framework/)

Скачиваем модуль __drf-yasg__ и устанавливаем в __INSTALLED_APPS__. Определяем Swagger в отдельном файле __swagger.py__ в головной директории.

http://0.0.0.0:8000/Swagger - адрес для работы со Swagger'ом.
