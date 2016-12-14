#!/bin/bash

# clean up current situation
docker-compose down -v

# rebuild containers
docker-compose build

# populate public directory and nginx directory
docker run --rm -it -v public:/public -v $(pwd):/backup busybox tar -C /public -xf /backup/public.tar
docker run --rm -it -v nginx:/nginx -v $(pwd):/backup busybox cp /backup/nginx/pyment.conf /nginx

# collectstatic
docker-compose run --rm web python manage.py collectstatic --noinput

# create database
docker-compose run --rm web python manage.py migrate

# load fixtures
apps="accounts checkout meadery inventory"
fixtures=`for app in $apps; do echo $app/fixtures/$app.json; done | xargs echo`
docker-compose run --rm web python manage.py loaddata $fixtures
