FROM phusion/baseimage:0.9.16
MAINTAINER mathuin@gmail.com
EXPOSE 8000

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    libfontconfig1 \
    libfreetype6 \
    libpq-dev \
    nodejs-legacy \
    npm \
    python-dev \
    python-pip

RUN npm -g install phantomjs

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app /opt/public
COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

#ENV DJANGO_SETTINGS_MODULE pyment.settings
#ENV DATABASE_URL postgres://postgres@db/postgres

WORKDIR /opt/app
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
