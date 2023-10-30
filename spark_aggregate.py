from pyspark.sql import SparkSession
from pyspark.sql.functions import month, year, hour, date_format, row_number, desc
from pyspark.sql.window import Window
import mysql.connector

spark = SparkSession.builder \
    .appName("MySQL Integration") \
    .getOrCreate()

# Daten aus MySQL lesen
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .load()

print("Laden abgeschlossen.")

# Monatlicher Gesamtumsatz pro Supermarkt
monthly_sales = df.groupBy(month("Datum").alias("Monat"), year("Datum").alias("Jahr"), "Supermarkt") \
    .sum("Umsatz") \
    .orderBy("Jahr", "Monat", "Supermarkt")


# Top 5 Artikel pro Supermarkt
windowSpec = Window.partitionBy("Supermarkt").orderBy(desc("sum(Umsatz)"))
top_articles = df.groupBy("Supermarkt", "Artikelnummer").sum("Umsatz") \
    .withColumn("rank", row_number().over(windowSpec)) \
    .filter("rank <= 5") \
    .drop("rank")


# Umsatz pro Kassiererin in jedem Supermarkt
sales_per_cashier = df.groupBy("Supermarkt", "Kassiererin_ID").sum("Umsatz")

# Tageszeit und Wochentag abhängigen Umsatz pro Supermarkt
time_sales = df.groupBy(hour("Uhrzeit").alias("Stunde"), date_format("Datum", 'E').alias("Wochentag"), "Supermarkt") \
    .sum("Umsatz")

print("Aggregierung abgeschlossen.")

# Daten zurück in MySQL schreiben
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



# Verbindung zur MySQL Datenbank herstellen
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword',
    database='supermarkt_db'
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregate_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("INSERT INTO aggregate_status (status) VALUES ('completed')")
conn.commit()  # Änderungen an der Datenbank speichern

cursor.close()  # Cursor schließen
conn.close()    # Verbindung schließen


print("Flagge wurde erfolgreich gesetzt.")

spark.stop()
