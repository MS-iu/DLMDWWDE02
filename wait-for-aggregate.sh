#!/bin/bash

set -e

DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="supermarkt_db"
FLAG_TABLE="aggregate_status"
COMPLETION_FLAG="completed"

while true; do
    # Überprüfen, ob die Fertigstellungsflagge in der Datenbank gesetzt ist
    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then

        break
    fi
    echo "Warten auf Aggregate-Fertigstellungsflagge..."
    sleep 30
done

echo "Aggregate-Fertigstellungsflagge gefunden, fahre fort..."
exec "$@"
