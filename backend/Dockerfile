FROM python:3.9.8-slim

RUN apt update

RUN apt install -y netcat

WORKDIR /usr/src/app/web

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgramm.wsgi:application", "--bind", "0:8000" ]
