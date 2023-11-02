# DLMDWWDE02
# Um die korrekte Ausführung des Skriptes zu ermöglichen muss der lokale Pfad in der Docker-compose Datei angepasst werden.
# In den dort angegebenen Ordner werden die generierten .csv Dateien, wie auch die geplotteten Diagramme zusätzlich geladen.
# Dies dient allein der besseren Zugänglichkeit der Ergebnisse des Projekts.


Projekt: Data Engineering

Dieses Konzept beschreibt eine im Rahmen des Moduls Data Engineering entwickelte batch-orientierte Datenarchitektur, 
die sich mit der effektiven Verarbeitung von fiktiv erzeugten Umsatzdaten einer Supermarktkette beschäftigt. 

Innerhalb der Architektur werden Docker-Container für den Aufbau von Microservices eingesetzt um die Verfügbarkeit, 
Skalierbarkeit und Wartbarkeit des Systems sicherzustellen.

Die Realisierung des Konzepts findet in der Entwicklungsumgebung von PyCharm sowie Docker Desktop statt, 
wobei GitHub für die Verwaltung und Nachvollziehbarkeit der Entwicklung genutzt wird. 

Im initialen Container werden mittels eines Python-Skripts eine Million Supermarktumsatzdaten generiert. 
Diese Datensätze werden auf zehn separate CSV-Dateien verteilt und sowohl in einem spezifisch deklarierten Volume, 
als auch lokal auf dem Benutzerdesktop gespeichert.

Parallel zur Datengenerierung wird eine MySQL-Datenbank gestartet, die zum Abschluss des Projekts sieben Tabellen umfassen soll. 
Diese Datenbank dient als Speicherort sowohl für die ursprünglichen als auch für die später aggregierten Daten.

Ein weiteres Python-Skript, in einem separaten Container, ist als Import Service für die Übertragung der generierten Datensätze 
in die zuvor aufgesetzte MySQL-Datenbank verantwortlich. 

Für die Datenaggregierung wird auf Apache Spark zurückgegriffen, eine führende Technologie im Big-Data Bereich. 
Dieser spezialisierte Microservice übernimmt die Aufbereitung der Daten, wobei vier definierte Aggregationsprozesse durchgeführt werden sollen.
Nach Ende der Aggregierung werden die Daten in die MySQL Datenbank zurückgeschrieben.

Abschließend werden die neu erstellten Tabellen aus der Datenbank ausgelesen und in einem weiteren Container mit einem Python-Skript visualisiert. 
Dieses Skript erzeugt vier unterschiedliche Arten von Diagrammen, welche die Ergebnisse der Datenanalyse grafisch darstellen.

Die Gesamtheit der aufgebauten Datenarchitektur wird in einer Docker Compose-Datei definiert, 
was eine effiziente Orchestrierung der Microservices und ihrer zugehörigen Abhängigkeiten ermöglichen soll.
Zur zeitlichen Koordinierung, wird sowohl ein einfaches wait, wie auch Endlosschleifen, die nachfolgende Prozesse erst starten, 
wenn die Datenbank erreichbar ist oder gewissen Tabelleneinträge vorhanden sind, verwendet.

Die Projektstruktur wurde so konzipiert, dass sie modular, leicht verständlich und einfach erweiterbar ist. 
Dies wird durch die klare Aufteilung der unterschiedlichen Microservices und ihrer jeweiligen Aufgaben, 
wie in der Konzept-Zeichnung dargestellt, erreicht.
