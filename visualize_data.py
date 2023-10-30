import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Verbindung zur MySQL Datenbank herstellen
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword',
    database='supermarkt_db'
)

desktop_directory = '/app/csv_data_desktop'

# Daten aus der Datenbank abrufen und in DataFrame konvertieren
def fetch_data(query):
    return pd.read_sql(query, conn)

# 1. Monatlicher Gesamtumsatz pro Supermarkt
monthly_sales_query = """
SELECT MONTH(Datum) as Monat, YEAR(Datum) as Jahr, Supermarkt, SUM(Umsatz) as Gesamtumsatz
FROM umsatz
GROUP BY Jahr, Monat, Supermarkt
ORDER BY Jahr, Monat, Supermarkt;
"""
monthly_sales = fetch_data(monthly_sales_query)
monthly_sales_pivot = monthly_sales.pivot_table(index=['Jahr', 'Monat'], columns='Supermarkt', values='Gesamtumsatz')
monthly_sales_pivot.plot(kind='bar', figsize=(15, 7))
plt.title('Monatlicher Gesamtumsatz pro Supermarkt')
plt.ylabel('Umsatz')
plt.xlabel('Monat, Jahr')
plt.tight_layout()
plt.savefig("/app/csv_data/monthly_sales.png")
plt.savefig(f"{desktop_directory}/monthly_sales.png")
plt.close()

# 2. Top 5 Artikel pro Supermarkt
top_articles_query = """
SELECT Supermarkt, Artikelnummer, SUM(Umsatz) as Gesamtumsatz
FROM umsatz
GROUP BY Supermarkt, Artikelnummer
ORDER BY Supermarkt, Gesamtumsatz DESC;
"""
top_articles = fetch_data(top_articles_query)
top_5_articles = top_articles.groupby("Supermarkt").head(5)
for market in top_5_articles['Supermarkt'].unique():
    subset = top_5_articles[top_5_articles['Supermarkt'] == market]
    subset.plot(x='Artikelnummer', y='Gesamtumsatz', kind='bar', legend=False)
    plt.title(f'Top 5 Artikel für {market}')
    plt.ylabel('Umsatz')
    plt.tight_layout()
    plt.savefig(f"/app/csv_data/top_articles_{market}.png")
    plt.savefig(f"{desktop_directory}/top_articles_{market}.png")
    plt.close()

# 3. Umsatz pro Kassiererin in jedem Supermarkt
sales_per_cashier_query = """
SELECT Supermarkt, Kassiererin_ID, SUM(Umsatz) as Gesamtumsatz
FROM umsatz
GROUP BY Supermarkt, Kassiererin_ID;
"""
sales_per_cashier = fetch_data(sales_per_cashier_query)
for market in sales_per_cashier['Supermarkt'].unique():
    subset = sales_per_cashier[sales_per_cashier['Supermarkt'] == market]
    subset.plot(x='Kassiererin_ID', y='Gesamtumsatz', kind='bar', legend=False)
    plt.title(f'Umsatz pro Kassiererin in {market}')
    plt.ylabel('Umsatz')
    plt.tight_layout()
    plt.savefig(f"/app/csv_data/sales_per_cashier_{market}.png")
    plt.savefig(f"{desktop_directory}/sales_per_cashier_{market}.png")
    plt.close()

# 4. Tageszeit und Wochentag abhängigen Umsatz pro Supermarkt
time_sales_query = """
SELECT HOUR(Uhrzeit) as Stunde, DAYNAME(Datum) as Wochentag, Supermarkt, SUM(Umsatz) as Gesamtumsatz
FROM umsatz
GROUP BY Wochentag, Stunde, Supermarkt;
"""
time_sales = fetch_data(time_sales_query)
time_sales_pivot = time_sales.pivot_table(index=['Wochentag', 'Stunde'], columns='Supermarkt', values='Gesamtumsatz')
time_sales_pivot.plot(kind='line', figsize=(15, 7))
plt.title('Tageszeit und Wochentag abhängiger Umsatz pro Supermarkt')
plt.ylabel('Umsatz')
plt.xlabel('Wochentag, Stunde')
plt.tight_layout()
plt.savefig("/app/csv_data/time_sales.png")
plt.savefig(f"{desktop_directory}/time_sales.png")
plt.close()

# Schließen der Verbindung
conn.close()