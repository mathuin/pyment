#!/bin/bash

# This script currently requires two additional files:
# - pyment_db.bak -- a backup of the production database
# - media.tar -- a backup of the production media files

# The goal is to build a minimal set of data which can then be
# integrated as fixtures.  For now, real data works!

# import fixtures
#docker-compose run web python manage.py syncdb --noinput  # <-- once fixtures are ready
docker-compose start db && \
    docker run --link pyment_db_1:pyment_db_1 aanand/wait && \
    docker exec -i pyment_db_1 psql -U pyment < pyment_db.bak && \
    docker-compose stop db
# to *export* fixtures, do this:
# docker-compose start db && \
#     sleep 15 && \
#     docker exec -i pyment_db_1 pg_dump -U pyment pyment > newpyment.bak && \
#     docker-compose stop db
# populate media directory
docker-compose run web tar -C /opt/public -xf /opt/app/media.tar
