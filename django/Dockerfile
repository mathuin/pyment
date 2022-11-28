FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN apk add --no-cache bash
WORKDIR /code
COPY requirements.txt /code
RUN apk add --no-cache --virtual .build-deps \
gcc \
jpeg-dev \
freetype-dev \
musl-dev \
postgresql-dev \
python3-dev \
zlib-dev \
&& pip install --no-cache-dir -r requirements.txt
COPY . /code/
