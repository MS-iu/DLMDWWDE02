# Apache Spark Service
# Dieser Service nutzt Apache Spark, um die Daten zu aggregieren oder zu analysieren.
# Ausgangspunkt ist ein vorkonfiguriertes Jupyter-Notebook mit PySpark, um die Einrichtung zu erleichtern.

from pyspark.sql import SparkSession
from pyspark.sql.functions import month, year, hour, date_format, row_number, desc
from pyspark.sql.window import Window
import mysql.connector

# Initialisierung einer SparkSession, die für die Verwendung von Apache Spark erforderlich ist
spark = SparkSession.builder \
    .appName("MySQL Integration") \
    .getOrCreate()

# Laden der Daten aus unserer MySQL-Datenbanktabelle in einen Spark DataFrame
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .load()

print("Laden abgeschlossen.")

# Berechnung des monatlichen Gesamtumsatzes für jeden Supermarkt
monthly_sales = df.groupBy(month("Datum").alias("Monat"), year("Datum").alias("Jahr"), "Supermarkt") \
    .sum("Umsatz") \
    .orderBy("Jahr", "Monat", "Supermarkt")


# Ermittlung der Top 5 Artikel nach Umsatz in jedem Supermarkt
windowSpec = Window.partitionBy("Supermarkt").orderBy(desc("sum(Umsatz)"))
top_articles = df.groupBy("Supermarkt", "Artikelnummer").sum("Umsatz") \
    .withColumn("rank", row_number().over(windowSpec)) \
    .filter("rank <= 5") \
    .drop("rank")


# Berechnung des Gesamtumsatzes jeder Kassiererin in jedem Supermarkt
sales_per_cashier = df.groupBy("Supermarkt", "Kassiererin_ID").sum("Umsatz")

# Berechnung des Umsatzes nach Tageszeit und Wochentag in jedem Supermarkt
time_sales = df.groupBy(hour("Uhrzeit").alias("Stunde"), date_format("Datum", 'E').alias("Wochentag"), "Supermarkt") \
    .sum("Umsatz")

print("Aggregierung abgeschlossen.")

# Schreiben der aggregierten Daten zurück in neue Tabellen in der MySQL-Datenbank
monthly_sales.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "monthly_sales") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

top_articles.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "top_articles") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

sales_per_cashier.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "sales_per_cashier") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

time_sales.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "time_sales") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

print("Export abgeschlossen.")



# Herstellen einer Verbindung zur MySQL-Datenbank mit mysql.connector
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword',
    database='supermarkt_db'
)
cursor = conn.cursor()
# Erstellen einer Tabelle für den Aggregationsstatus, falls diese nicht existiert
cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregate_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
# Einfügen des completed Datensatzes, um den Abschluss des Aggregationsprozesses anzuzeigen
# Das ist das Startsignal für die Aggregation.
cursor.execute("INSERT INTO aggregate_status (status) VALUES ('completed')")
#Speichern der Änderungen in der Datenbank und beenden der Verbindung.
conn.commit()
cursor.close()
conn.close()


print("Flagge wurde erfolgreich gesetzt.")

# Beenden der Spark-Session
spark.stop()
