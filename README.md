#DLMDWWDE02 - Batch-basierte Datenarchitektur für eine datenintensive Applikation

Die im Rahmen des Moduls DLMDWWDE02 gebaute Pipeline ist ein robustes, Docker-basiertes System, 
das für die Verarbeitung und Analyse von Supermarktdaten konzipiert wurde. 
Das System verwendet eine Serie von Microservices, um eine Million Datensätze zu generieren, diese zu importieren, 
zu aggregieren und anschließend zu visualisieren.


#Repository
Das gesamte Projekt ist auf GitHub unter https://github.com/MS-iu/DLMDWWDE02 verfügbar.

#Projektstruktur
Das Repository ist wie folgt strukturiert:

csv_data: Ein Volume, das die generierten CSV-Daten enthält.
docker-compose.yml: Die Docker Compose-Konfigurationsdatei, die die Dienste definiert.
Dockerfile-generate: Das Dockerfile für den Daten Generator Service.
Dockerfile-import: Das Dockerfile für den Daten Import Service.
Dockerfile-spark: Das Dockerfile für den Apache Spark Service.
Dockerfile-visualize: Das Dockerfile für den Daten Visualisierung Service.
generate_supermarkt_daten.py: Das Skript zum Generieren der Daten.
import_to_mysql.py: Das Skript zum Importieren der Daten in die MySQL-Datenbank.
init.sql: Ein SQL-Skript zur Initialisierung der Datenbank und Tabellen.
README.md: Diese Anleitung.
spark_aggregate.py: Das Skript, das Apache Spark zur Datenaggregation verwendet.
visualize_data.py: Das Skript zur Visualisierung der Daten.
wait-for-import.sh und wait-for-it.sh: Shell-Skripte, die sicherstellen, dass die Dienste in der richtigen Reihenfolge gestartet werden.

#Voraussetzungen
Bevor Sie beginnen, stellen Sie sicher, dass Sie folgende Software installiert haben:

Docker
Docker Compose
Python 3.x

Bitte ändern Sie den angegebenen Pfad in der docker-compose.yml Datei, um die Dateien auf den gewünschten lokalen Pfad zu speichern.
Die lokale Speicherung ermöglicht eine optimale Übersicht über die Ein- und Ausgaben der Pipeline.

#Schnellstart
Führen Sie die folgenden Schritte aus, um die Pipeline in Ihrer IDE Umgebung zu starten:

git clone https://github.com/MS-iu/DLMDWWDE02 /
cd DLMDWWDE02 / 
docker-compose build --no-cache / 
docker-compose up


Die Dienste werden in der festgelegten Reihenfolge durch docker-compose orchestriert. 
Nach dem Starten der Container können Sie die Logs verfolgen, um den Fortschritt zu beobachten:

docker-compose logs -f

#Beenden und Aufräumen
Um die Container zu stoppen und zu entfernen, nutzen Sie:

docker-compose down

Um alle Volumes zu entfernen und somit alle Daten zu löschen, verwenden Sie:

docker-compose down -v

Pipeline wurde zuletzt getestet am 11.11.2023 um 16:23