#!/bin/sh
set -e

mkdir -p /app/db

python manage.py migrate --noinput

exec "$@"
