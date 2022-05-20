# Instruction to Trade cars application

При запуске приложения через __docker-compose__ будет автоматически произовдиться удаление __Celery__ логов, очистка базы данных. Выполнение всех миграций, запуск сервера, и заполнение базы данных новыми значениям с двумя суперпользователями ((root, 1234), (admin, admin)).


## Git commits

Общепринятые информативные коммиты [тут](https://habr.com/ru/post/183646/), [вот тут](https://habr.com/ru/company/otus/blog/537196/) и [здесь](https://drbrain.ru/articles/git-commit-message/), [и вот](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser).


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

Обращаться к сервисам (web – приложение, db – база данных) через запущенный контейнер: *docker-compose exec web(db) ...*. Остановить контейнер и удалить его: *docker-compose down -v*. Если возникла проблема с активными ендпоинтами, то останавливаем так: *docker-compose down --remove-orphans*.


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


## Авторизация пользователей

### Переопределение User object

Можно переопределить объект user одни из трёх классов, предпочтителен abstract base. Использовал Permission mixins.

Установливаем модуль __djangorestframework-simplejwt__ в проект и добавляем словарь __REST_FRAMEWORK__ значения для авторизации.

Использование [djoser и jwt](https://django.fun/tutorials/registraciya-i-avtorizaciya-polzovatelej-v-django-s-pomoshyu-djoser-i-veb-tokenov-json/). Переопределение объекта user [тут](https://django.fun/tips/polzovatelskaya-model-user/) и [тут](https://tproger.ru/translations/extending-django-user-model/#var3).

Регистрация с [подтверждением](https://www.youtube.com/watch?v=PC0S1dkRNtg&ab_channel=DjangoSchool) почты пользователя.

Для корректной регистрации пользователей создаём форму с указанием поля 'role' для категории ползователей.


### Регистрация и аутентификация с помощью JWT через API адреса

В __settings.py__ устанавливаем Djoser, Simple_JWT и переменные в REST_FRAMEWORK.

Используем POSTMAN для отправки запросов на сервер.

http://0.0.0.0:8000/api/auth/users/ - адрес выводит всех пользователей и позволяет регистрировать новых пользователей.

http://0.0.0.0:8000/api/token/ – передаём POST запросом (Body - form-data) следующие поля: __username__ & __password__. Они нужны для логина зарегистрированного пользователя на сайте. Получаем __access__ и __refresh__ token'ы ответом.

http://0.0.0.0:8000/api/buyer/ - GET запросом в Header'е передаём определяем ещё один параметр __Authorization__, а в значении тип токена (заголовок) __JWT__ и сам __access токен__. Отправляя запрос сервер видит токен и понимает, что получен от авторизованного пользователя, разрешая просмотр запрошенного ресурса, или нет.

http://0.0.0.0:8000/api/token/refresh/ - по истечению жизни __access токена__ передаём POST запросом (Body - form-data) поле __refresh__ c __refresh токеном__ на сервер, чтобы получить новый __access токен__.


Определяем вложенную сериализацияю для получения покупетеля, автосалона и поставщика со связанным значением их пользователя.

Настроены права доступа пользователей только к собственным данным и общий доступ для суперпользователей.


## Подключение Django Toold Bar

[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

Установка __django-debug-toolbar__ через __pipenv__. Прописываем установленный пакет в __INSTALLED_APPS__, в коллекцию __MIDDLEWARE__ так же указываем установленный пакет. Потом прописываем новую коллекцию __INTERNAL_IPS__ со списком отслеживаемых IP-адресов.

Так же необходимо добавить __DEBUG_TOOLBAR_CONFIG__ для корректной работы его с __DRF__.


## Подключение Swagger

[Swagger](https://gadjimuradov.ru/post/swagger-dlya-django-rest-framework/)

Скачиваем модуль __drf-yasg__ и устанавливаем в __INSTALLED_APPS__. Определяем Swagger в отдельном файле __swagger.py__ в головной директории.

http://0.0.0.0:8000/Swagger - адрес для работы со Swagger'ом.


## Django-filter 

[Django-filter](https://django-filter.readthedocs.io/en/stable/index.html)

Создание фильтрации через открыте API DRF, скачиваем, устанавливаем, всё как обычно. Создаём в ядре сайта __service.py__, где определяем фильтрующие классы. [Инструкция с примерами](https://russianblogs.com/article/1476297017/).

Во __views.py__ импортируем  определяем кортеж фильтрующих элементов и переменные с полями для поиска, сортировки - *from rest_framework import filters*, и для фильтарции данных - *from django_filters.rest_framework import DjangoFilterBackend*.


## Скрипт для заполнения таблиц базы данных

Скрипт для заполнения таблиц базы данных реализуется через обязательное добавление директорий в приложение, в данном случае __core__, __management/commands__. 

В скрипте прописываем класс __Command__, который наследуется от __BaseCommand__. В нём переопределяем метод __handle__, где и прописываем необходимый для исполнения по команду код.

Код исполняется внутри контейнера, и запускается: *docker-compose exec web python manage.py fill_db*.


## Celery + Flower & Redis

[Celere](https://docs.celeryq.dev/en/v4.0.2/django/first-steps-with-django.html#using-celery-with-django) & [more](https://docs.celeryq.dev/en/stable/reference/cli.html#celery).

Устанавливаем в проект __Celery__ + __Flower__ & __Redis__. Создаём файл __celery.py__ в __admin app__. Куда пропиываем необходимые значения и создаём экземпляр класса __Celery__ __app__, который хранит зачение своего каталога, через который будет производиться запуск __Celery__ в проекте. Так же в этой директории обновим **__init.py__**, зарегестрировав сам __Celery__. И добавим две новые переменные в __.env__ (CELERY_BROKER_URL, CELERY_RESULT_BACKEND).

В __core app__ создаём __tasks.py__ в которым перечислены заданные таски. 

__Docker-compose.yml__ расширим файл новыми сервисами (Celery & Redis).

Исструкции по установке в проект [Вот тут](https://khashtamov.com/ru/celery-best-practices/), [здесь](https://soshace.com/dockerizing-django-with-postgres-redis-and-celery/) и  [тут](https://hashsum.ru/celery-django-redis/), [а и вот ещё](https://webdevblog.ru/celery-django-i-redis/), [и ещё](https://habr.com/ru/company/otus/blog/503380/).

[Пример](https://github.com/mher/flower/blob/master/docker-compose.yml) __docker-compose.yml__ для __Celery__.

http://localhost:5555/dashboard - адрес __Celery Flower__.

Запуск всех компонентов с воркером и с планировщиком происходит при сборке контейнера __Docker__.


## Nginx & Gunicorn

[Продолжение](https://django.fun/tutorials/dokerizaciya-django-s-pomoshyu-postgres-gunicorn-i-nginx/#:~:text=manage.py%20migrate-,Gunicorn,-%D0%94%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D1%80%D0%B5%D0%B4) инструкции по девопс штучкам.


