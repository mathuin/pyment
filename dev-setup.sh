#!/bin/bash

# clean up current situation
docker-compose stop
docker-compose rm --force

# rebuild containers
docker-compose build

# start data containers
docker-compose up -d db public

# jumpstart database configuration
docker-compose run web true

# collectstatic
docker-compose run web python manage.py collectstatic --noinput

# create database
# due to race conditions, this may require multiple attempts
retcode=1
count=0
while [ $retcode -ne 0 ]; do
    count=$((count+1))
    if [ $count -gt 10 ]; then
      echo "FAIL: ten failed attempts to run syncdb"
      echo "one last run with stdout and stderr displayed follows!"
      docker-compose run web python manage.py syncdb --noinput
      break
    fi
    docker-compose run web python manage.py syncdb --noinput >/dev/null 2>/dev/null
    retcode=$?
done

# load fixtures
apps="checkout meadery inventory"
fixtures=`for app in $apps; do echo $app/fixtures/$app.json; done | xargs echo`
docker-compose run web python manage.py loaddata $fixtures

# populate media directory
# docker-compose run web tar -C /opt/public -xf /opt/app/media.tar
