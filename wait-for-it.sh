#!/bin/bash
# wait-for-it.sh

set -e

host="mysql_db"
shift
port="3306"
shift
shift

until nc -z -v -w30 $host $port; do
  echo "Warten auf $host:$port..."
  sleep 30
done

echo "$host:$port ist verfügbar, fahre fort..."

exec "$@"
