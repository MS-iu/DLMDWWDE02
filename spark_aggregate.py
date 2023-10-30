from pyspark.sql import SparkSession

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

# Daten aggregieren (Beispiel: Summe des Umsatzes pro Supermarkt)
agg_df = df.groupBy("Supermarkt").sum("Umsatz")

# Daten zurück in MySQL schreiben
agg_df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/supermarkt_db") \
    .option("dbtable", "aggregated_umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

spark.stop()
