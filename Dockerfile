FROM phusion/baseimage:0.9.16
MAINTAINER mathuin@gmail.com
EXPOSE 8000

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python-dev \
    python-pip

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app /opt/public
COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

#ENV DJANGO_SETTINGS_MODULE pyment.settings
#ENV DATABASE_URL postgres://postgres@db/postgres

WORKDIR /opt/app
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
