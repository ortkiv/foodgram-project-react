#!/bin/sh

if [ "$DB_NAME" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
        echo "Waiting PG service"
        sleep 0.1
    done
        echo "PostrgeSQL started"
fi

python manage.py makemigrations --noinput

python manage.py migrate --noinput

python manage.py collectstatic --no-input --clear

python manage.py add_ingredients

python manage.py add_tags

python manage.py createsuperuser --noinput

exec "$@"
