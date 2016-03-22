#!/bin/bash

# clean up current situation
docker-compose down -v

# rebuild containers
docker-compose build

# collectstatic
docker-compose run --rm web python manage.py collectstatic --noinput

# create database
docker-compose run --rm web ./wait-for-it.sh db:5432 -- python manage.py syncdb --noinput

# load fixtures
apps="accounts checkout meadery inventory"
fixtures=`for app in $apps; do echo $app/fixtures/$app.json; done | xargs echo`
docker-compose run --rm web python manage.py loaddata $fixtures

# populate media directory
# docker-compose run web tar -C /opt/public -xf /opt/app/media.tar
