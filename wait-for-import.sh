#!/bin/bash
# Das Bash-Skript läuft in einer Endlosschleife und prüft regelmäßig die Datenbank auf eine spezifische Bedingung,
# um mit der Ausführung des eigentlichen Skriptes fortzufahren.,


# Beendet das Skript bei Fehlern, um trotz Fehler einen Durchlauf zu ermöglichen
set -e

DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="supermarkt_db"
FLAG_TABLE="import_status"
COMPLETION_FLAG="completed"

# Endlosschleife, um auf die Fertigstellungsflagge zu warten
while true; do
    # Überprüft, ob die Fertigstellungsflagge in der Datenbank gesetzt ist
    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then
        # Verlässt die Schleife, wenn die Flagge gefunden wird
        break
    fi
    # Gibt eine Meldung aus und wartet, wenn die Flagge noch nicht gesetzt ist
    echo "Warten auf Datenimport-Fertigstellungsflagge..."
    sleep 60  # Wartet 60 Sekunden bis zur Erneuten Prüfung.
done

# Nach Auffinden der Flagge wird das vorgesehene Skript ausgeführt.
echo "Datenimport-Fertigstellungsflagge gefunden, fahre fort..."
exec "$@"
