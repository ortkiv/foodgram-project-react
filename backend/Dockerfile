FROM python:3.9.8-slim

RUN apt update

RUN apt install -y netcat

WORKDIR /usr/src/app/web

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN chmod 777 /usr/src/app/web/docker-entrypoint.sh

RUN ls -l /usr/src/app/web/docker-entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/web/docker-entrypoint.sh"]
