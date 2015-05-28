FROM phusion/baseimage:0.9.16

MAINTAINER Jack Twilley <mathuin@gmail.com>

# Port 8000 may be in use by squid-deb-proxy.
ENV PORTNUM 8001

# Use squid-deb-proxy if present.
ENV DIRECT_HOSTS ppa.launchpad.net

RUN route -n | awk '/^0.0.0.0/ {print $2}' > /tmp/host_ip.txt
RUN echo "HEAD /" | nc `cat /tmp/host_ip.txt` 8000 | grep squid-deb-proxy \
  && (echo "Acquire::http::Proxy \"http://$(cat /tmp/host_ip.txt):8000\";" > /etc/apt/apt.conf.d/30proxy) \
  && (for host in ${DIRECT_HOSTS}; do echo "Acquire::http::Proxy::$host DIRECT;" >> /etc/apt/apt.conf.d/30proxy; done) \
  || echo "No squid-deb-proxy detected on docker host"

# Never ask for confirmations
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    libpq-dev \
    python-dev \
    python-pip

ENV PYTHONUNBUFFERED 1

# Environment settings
#ENV DEBUG True
ENV SECRET_KEY 'qkmm6qcxz9npoCxtt8ofRu5vVFeTEfbDIJdmIKiEBIiVCi2ef9'
ENV PUBLIC_ROOT /opt/public
ENV ALLOWED_HOSTS localhost,127.0.0.1

RUN mkdir -p /opt/app /opt/public
COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

WORKDIR /opt/app
EXPOSE ${PORTNUM}
CMD [ "python", "manage.py", "runserver", "0.0.0.0:${PORTNUM}" ]
