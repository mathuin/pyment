#!/usr/bin/env bash
set -x

# clean up current situation
docker-compose down -v

# rebuild containers
docker-compose build

# populate public directory and nginx directory and development SSL directory
docker run --rm -it -v pyment_public:/public -v $(pwd):/backup busybox tar -C /public -xf /backup/public.tar
docker run --rm -it -v pyment_nginx:/nginx -v $(pwd):/backup busybox cp /backup/nginx/pyment.conf /nginx
docker run --rm -it -v pyment_devssl:/devssl -v $(pwd):/backup busybox tar -C /devssl -xf /backup/devssl.tar

# collectstatic
docker-compose run --rm web python manage.py collectstatic --noinput

# create database
docker-compose run --rm web python manage.py migrate

# output logs if error
if [[ $? == 1 ]]; then
  docker logs pyment_db_1
fi

# load fixtures
apps="accounts checkout meadery inventory"
fixtures=`for app in $apps; do echo $app/fixtures/$app.json; done | xargs echo`
docker-compose run --rm web python manage.py loaddata $fixtures
