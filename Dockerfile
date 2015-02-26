FROM phusion/baseimage:0.9.16
MAINTAINER mathuin@gmail.com
EXPOSE 8001

# https://gist.github.com/dergachev/8441335
# If host is running squid-deb-proxy on port 8000, populate /etc/apt/apt.conf.d/30proxy
# By default, squid-deb-proxy 403s unknown sources, so apt shouldn't proxy ppa.launchpad.net
RUN route -n | awk '/^0.0.0.0/ {print $2}' > /tmp/host_ip.txt
RUN echo "HEAD /" | nc `cat /tmp/host_ip.txt` 8000 | grep squid-deb-proxy \
  && (echo "Acquire::http::Proxy \"http://$(cat /tmp/host_ip.txt):8000\";" > /etc/apt/apt.conf.d/30proxy) \
  && (echo "Acquire::http::Proxy::ppa.launchpad.net DIRECT;" >> /etc/apt/apt.conf.d/30proxy) \
  || echo "No squid-deb-proxy detected on docker host"

ENV DEBIAN_FRONTEND noninteractive
#RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

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

WORKDIR /opt/app
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001" ]
