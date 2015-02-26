#!/bin/bash

# dev-setup.sh - sets up containers for development and testing

# This script currently requires two additional files:
# - pyment_db.bak -- a backup of the production database
# - media.tar -- a backup of the production media files

# The goal is to build a minimal set of data which can then be
# integrated as fixtures.  For now, real data works!

# destroys existing containers
fig stop
# removes existing containers
fig rm --force
# builds containers
fig build
# first-run database autoconfig
fig run web true
# import fixtures
#fig run web python manage.py syncdb --noinput  # <-- once fixtures are ready
fig start db && \
    sleep 15 && \
    docker exec -i pyment_db_1 psql -U pyment < pyment_db.bak && \
    fig stop db
# to *export* fixtures, do this:
# fig start db && \
#     sleep 15 && \
#     docker exec -i pyment_db_1 pg_dump -U pyment pyment > newpyment.bak && \
#     fig stop db
# populate media directory
fig run web tar -C /opt/public -xf /opt/app/media.tar
