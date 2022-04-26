# Instruction to Trade cars application

## Git commits

Общепринятые информативные коммиты [тут](https://habr.com/ru/post/183646/), [вот тут](https://habr.com/ru/company/otus/blog/537196/) и [здесь](https://drbrain.ru/articles/git-commit-message/).

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

## Скрипт для случайного заполнения таблиц базы данных

Скрипт для заполнения таблиц базы данных реализуется через обязательное добавление директорий в приложение, в данном случае __core__, __management/commands__. 

В скрипте прописываем класс __Command__, который наследуется от __BaseCommand__. В нём переопределяем метод __handle__, где и прописываем необходимый для исполнения по команду код.

Код исполняется внутри контейнера, и запускается: *docker-compose exec web python manage.py fill_db*.

## Авторизация пользователей

*Осуществлять следующим образом: переопределить объект user одни из трёх классов, предпочтителен abstract base. Использовать Permission mixins.*

Устанавливаем модуль __djangorestframework-simplejwt__ в проект и добавляем словарь __REST_FRAMEWORK__ значения для авторизации.

Использование [djoser и jwt](https://django.fun/tutorials/registraciya-i-avtorizaciya-polzovatelej-v-django-s-pomoshyu-djoser-i-veb-tokenov-json/). Переопределение объекта user [тут](https://django.fun/tips/polzovatelskaya-model-user/) и [тут](https://tproger.ru/translations/extending-django-user-model/#var3).

Регистрация с [подтверждением](https://www.youtube.com/watch?v=PC0S1dkRNtg&ab_channel=DjangoSchool) почты пользователя

