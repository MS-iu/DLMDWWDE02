# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.9

# Setzen Sie das Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Kopieren Sie die Anwendungsdateien in das Arbeitsverzeichnis
COPY . /app

# Installieren Sie die erforderlichen Python-Bibliotheken
RUN pip install pandas

# Führen Sie die Python-Anwendung aus, um Daten zu generieren und als CSV-Datei abzulegen
CMD ["python", "generate_supermarkt_daten.py"]

