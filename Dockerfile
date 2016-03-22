FROM python:2.7
MAINTAINER Jack Twilley <mathuin@gmail.com>
ENV PYTHONUNBUFFERED 1

# Environment settings
ENV DEBUG True
ENV SECRET_KEY 'qkmm6qcxz9npoCxtt8ofRu5vVFeTEfbDIJdmIKiEBIiVCi2ef9'
ENV PUBLIC_ROOT /public
ENV ALLOWED_HOSTS localhost,127.0.0.1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
