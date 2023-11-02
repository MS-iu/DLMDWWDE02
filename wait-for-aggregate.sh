#!/bin/bash

# Beendet das Skript bei Fehlern, um trotz Fehler einen Durchlauf zu ermöglichen
set -e

DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="supermarkt_db"
FLAG_TABLE="aggregate_status"
COMPLETION_FLAG="completed"

while true; do
    # Überprüft, ob die Fertigstellungsflagge in der Datenbank gesetzt ist.
    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then
        # Verlässt die Schleife, wenn die Flagge gefunden wird
        break
    fi
    # Gibt eine Meldung aus und wartet, wenn die Flagge noch nicht gesetzt ist
    echo "Warten auf Aggregate-Fertigstellungsflagge..."
    sleep 60 # Wartet 60 Sekunden bis zur Erneuten Prüfung.
done

# Nach Auffinden der Flagge wird das vorgesehene Skript ausgeführt.
echo "Aggregate-Fertigstellungsflagge gefunden, fahre fort..."
exec "$@"
