[![foodgram_project_react](https://github.com/ortkiv/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](http//158.160.9.27/admin/)



# Продуктовый помощник

# Описание
- Мини социальная сеть для кулинаров и любителей готовить и вкусно поесть
- Регистрируемся, создаём рецепты блюд с фотографиями и тэгами
- Подписываемся на интересных авторов
- Сортируем рецепты по тэгам
- Добавляем любимые рецепты в избранное
- Так же можно добавить понравившиеся рецепты в список покупок,
- алгоритм посчитает нужное кол-во ингредиентов для приготовления из всех добавленных рецептов
- и при нажатии на кнопку скачать во вкладке "Список покупок" выдаст вам список pdf-файлом. Удобно :-)

# Технологии
- Python 3.9.8 
- Django 4.1.2
- Gunicorn 20.1.0
- Nginx 1.21.3-alpine
- PostgreSQL 13.0-alpine
- Docker

# Запуск проекта локально:

- Клонируйте репозитроий с проектом:
`````
git@github.com:ortkiv/foodgram-project-react.git
`````
- Зайдите в директорию с проектом, создайте и активируйте виртуальное окружение:

`````
python -m venv venv
source venv/Scripts/activate
`````
- Зайдите в директирию, содержащую requirements.txt и установить зависимости:
`````
cd backend/
pip install -r requirements.txt
`````
- Запустите миграции:
`````
python manage.py makemigrations
python manage.py migrate
`````
- Запустите сервер:
`````
python manage.py runserver
`````

# Запуск проекта в Docker

- Установите Docker
- Конфигурационный файл nginx находится в директории infra/nginx/
- Изучите его и, если необходимо, внесите измения, в частности, server name/адрес проекта
- Параметры запуска указаны в файле docker-compose.yml в директории infra/
- Для запуска выполните команду:
`````
docker compose up
`````

# Особенности
- Для успешного старта создайте в папка infra .env файл и заполните его по шаблону: 
`````
DataBase

DB_ENGINE=django.db.backends.postgresql
DB_NAME=database name - укажите своё
POSTGRES_USER=database username - укажите свой
POSTGRES_PASSWORD=password for database user - укажите свой
DB_HOST=db
DB_PORT=5432

Django

DJANGO_SUPERUSER_USERNAME=superuser name - укажите своё
DJANGO_SUPERUSER_PASSWORD=password for superuser - укажите свой
DJANGO_SUPERUSER_EMAIL=email for suoeruser - укажите свой
SECRET_KEY=секретный ключ django
`````

# Автор
ortkiv
