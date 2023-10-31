import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Verbindung zur MySQL Datenbank herstellen
def establish_connection():
    return mysql.connector.connect(
        host='mysql_db',
        user='user',
        password='rootpassword',
        database='supermarkt_db'
    )

desktop_directory = '/app/csv_data_desktop'
volume_directory = '/app/csv_data'  # Zusätzliches Verzeichnis

# Daten aus der Datenbank abrufen und in DataFrame konvertieren
def fetch_data(query, connection):
    return pd.read_sql(query, connection)

# 1. Monatlicher Gesamtumsatz pro Supermarkt
def monthly_sales_per_supermarket(connection):
    monthly_sales_query = """
    SELECT Monat, Supermarkt, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM monthly_sales
    GROUP BY Monat, Supermarkt
    """
    monthly_sales = fetch_data(monthly_sales_query, connection)
    pivot_monthly_sales = monthly_sales.pivot(index='Monat', columns='Supermarkt', values='Gesamtumsatz')
    pivot_monthly_sales.plot(kind='bar', figsize=(15, 7))
    plt.ylim([pivot_monthly_sales.values.min()-10000, pivot_monthly_sales.values.max()+10000])  # y-Achse anpassen
    plt.title('Monatlicher Gesamtumsatz pro Supermarkt')
    plt.ylabel('Umsatz')
    plt.tight_layout()
    plt.savefig(f"{desktop_directory}/monthly_sales.png")
    plt.savefig(f"{volume_directory}/monthly_sales.png")  # Speichern im zusätzlichen Verzeichnis
    plt.close()

# 2. Top 20 Artikel über alle Supermärkte
def top_20_articles_over_all_supermarkets(connection):
    top_articles_query = """
    SELECT Artikelnummer, Supermarkt, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM top_articles
    GROUP BY Artikelnummer, Supermarkt
    ORDER BY Gesamtumsatz DESC
    """
    top_articles = fetch_data(top_articles_query, connection)
    top_20_articles = top_articles.groupby('Artikelnummer').Gesamtumsatz.sum().nlargest(20).index.tolist()
    filtered_top_articles = top_articles[top_articles['Artikelnummer'].isin(top_20_articles)]
    pivot_top_articles = filtered_top_articles.pivot(index='Artikelnummer', columns='Supermarkt', values='Gesamtumsatz')

    # Sortiere die Pivot-Tabelle basierend auf dem Gesamtumsatz für jeden Artikel
    sorted_articles = pivot_top_articles.sum(axis=1).sort_values(ascending=False).index
    pivot_top_articles = pivot_top_articles.loc[sorted_articles]

    pivot_top_articles.plot(kind='bar', stacked=True, figsize=(15, 7))
    plt.title('Top 20 Artikel über alle Supermärkte')
    plt.ylabel('Umsatz')
    plt.tight_layout()
    plt.savefig(f"{desktop_directory}/top_articles.png")
    plt.savefig(f"{volume_directory}/top_articles.png")  # Speichern im zusätzlichen Verzeichnis
    plt.close()

# 3. Umsatz pro Kassiererin in allen Supermärkten
def sales_per_cashier(connection):
    cashier_sales_query = """
    SELECT Kassiererin_ID, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM sales_per_cashier
    GROUP BY Kassiererin_ID
    """
    cashier_sales = fetch_data(cashier_sales_query, connection)
    cashier_sales = cashier_sales.sort_values(by='Gesamtumsatz', ascending=False)
    cashier_sales.plot(x='Kassiererin_ID', y='Gesamtumsatz', kind='bar', figsize=(15, 7))
    plt.ylim([cashier_sales['Gesamtumsatz'].min()-10000, cashier_sales['Gesamtumsatz'].max()+10000])  # y-Achse anpassen
    plt.title('Umsatz pro Kassiererin in allen Supermärkten')
    plt.ylabel('Umsatz')
    plt.tight_layout()
    plt.savefig(f"{desktop_directory}/cashier_sales.png")
    plt.savefig(f"{volume_directory}/cashier_sales.png")  # Speichern im zusätzlichen Verzeichnis
    plt.close()

# 4. Tageszeitabhängiger Umsatz aller Supermärkte über 24h
def day_time_sales(connection):
    time_sales_query = """
    SELECT Stunde, Supermarkt, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM time_sales
    GROUP BY Stunde, Supermarkt
    """
    time_sales = fetch_data(time_sales_query, connection)
    pivot_time_sales = time_sales.pivot(index='Stunde', columns='Supermarkt', values='Gesamtumsatz')
    pivot_time_sales.plot(kind='area', stacked=True, figsize=(15, 7))
    plt.title('Tageszeitabhängiger Umsatz aller Supermärkte über 24h')
    plt.ylabel('Umsatz')
    plt.xlabel('Stunde')
    plt.tight_layout()
    plt.savefig(f"{desktop_directory}/time_sales.png")
    plt.savefig(f"{volume_directory}/time_sales.png")  # Speichern im zusätzlichen Verzeichnis
    plt.close()

# Hauptfunktion, die alles ausführt
def main():
    connection = establish_connection()
    monthly_sales_per_supermarket(connection)
    top_20_articles_over_all_supermarkets(connection)
    sales_per_cashier(connection)
    day_time_sales(connection)
    connection.close()

# Ausführen des Hauptprogramms
if __name__ == '__main__':
    main()
