#!/bin/bash

# Beendet das Skript bei Fehlern, um trotz Fehler einen Durchlauf zu ermöglichen
set -e

host="mysql_db"
shift
port="3306"
shift
shift
# Die Schleife versucht eine Netzwerkverbindung zum Host und Port aufzubauen.
until nc -z -v -w30 $host $port; do
  echo "Warten auf $host:$port..."  # Gibt eine Nachricht aus zu warten, solange die Datenbank nicht erreichbar ist
  sleep 30 # Wartet 30 sek bis zum nächsten Versuch
done
# Wenn die Verbindung erfolgreich war, wird die Nachricht ausgegeben, dass der Service verfügbar ist.
echo "$host:$port ist verfügbar, fahre fort..."
sleep 20  # Wartet zusätzliche 20 Sekunden, um sicherzustellen, dass auch wirklich alle Daten generiert worden sind.
# Hier könnte ebenfalls auf eine Flagge in der Datenbank gewartet werden.
echo "Import gestartet. Der Import kann bis zu 5 Minuten dauern."

# Führt das Import Skript aus.
exec "$@"
