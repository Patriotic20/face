#!/bin/bash
set -e


# Если ваши миграции (папка alembic) лежат в подпапке /app/app
# то может потребоваться переход: cd /app

cd /face/app
echo "Running migrations..."
alembic upgrade head

exec "$@"