# main.py
import streamlit as st
import pandas as pd

import Website_Configuration
import Tickers_List
import Daten_aus_Yahoo_Finance
import Symbols

# -------------------------------
# Funktionen
# -------------------------------

def filter_by_date(df: pd.DataFrame, time_filter: str): # df -> DataFrame
    """Filtert ein DataFrame nach dem ausgewählten Zeitraum, entfernt Zeilen mit fehlenden Werten 
    und gibt aus, wie viele Zeilen entfernt wurden."""
    
    now = pd.Timestamp.now()
    if time_filter == "Monat":
        start_date = now - pd.DateOffset(months=1)
    elif time_filter == "1 Jahr":
        start_date = now - pd.DateOffset(years=1)
    elif time_filter == "5 Jahre":
        start_date = now - pd.DateOffset(years=5)
    else:
        start_date = df.index.min()
    
    # Filter nach Datum
    df_filtered = df[df.index >= start_date]
    
    # Anzahl Zeilen vor dem Entfernen
    rows_before = len(df_filtered)
    
    # Zeilen entfernen, die in wichtigen Spalten NaN enthalten
    df_filtered = df_filtered.dropna(subset=["Close", "Volume"])
    
    # Anzahl Zeilen nach dem Entfernen
    rows_after = len(df_filtered)
    
    # Ausgabe in Streamlit
    removed = rows_before - rows_after
    if removed > 0:
        st.info(f"{removed} Zeilen mit fehlenden Werten wurden entfernt.")
    
    return df_filtered


def calculate_revenue(df: pd.DataFrame):
    """Berechnet Umsatz = Close * Volume, falls vorhanden."""
    if "Close" in df.columns and "Volume" in df.columns:
        df["Umsatz"] = df["Close"] * df["Volume"]
    return df


def extract_close_prices(data_dict: dict):
    """Extrahiert alle Close-Preise aus dem Dictionary in einen DataFrame."""
    return pd.concat([df["Close"].rename(ticker) for ticker, df in data_dict.items()], axis=1)


def display_charts(close_prices: pd.DataFrame, filtered_data: dict, show_volume: bool):
    """Zeigt Liniendiagramm für Close-Preise und Balkendiagramme für Umsatz."""
    st.header(f"{Symbols.symbols['curve_up']} Echtzeit-Aktienkurse") # Überschrift: Echtzeit-Aktienkurse
    if not close_prices.empty:
        # --- Fix: Wenn nur eine Aktie gewählt wurde ---
        # -> bei nur einer Spalte benenne sie explizit als "Close", damit Werte nicht verschwinden
        if close_prices.shape[1] == 1:
            close_prices = close_prices.copy()
            close_prices.columns = ["Close"]
        
        st.line_chart(close_prices)

    if show_volume:
        st.header(f"{Symbols.symbols['money']} Umsätze") # Überschrift: Umsätze
        for ticker, df in filtered_data.items():
            df = calculate_revenue(df)
            st.subheader(f"{ticker} - Umsatz")
            st.bar_chart(df["Umsatz"])


def calculate_KPIs(filtered_data: dict):
    """
    Berechnet KPIs für die gefilterten Ticker.
    Gibt ein DataFrame mit max, min, Durchschnitt und Volatilität zurück.
    
    filtered_data: dict {ticker: DataFrame}
    """
    kpi_dict = {
        "Max": {},
        "Min": {},
        "Durchschnitt": {},
        "Volatilität": {}
    }

    for ticker, df in filtered_data.items():
        if "Close" in df.columns and not df["Close"].empty:
            kpi_dict["Max"][ticker] = df["Close"].max()
            kpi_dict["Min"][ticker] = df["Close"].min()
            kpi_dict["Durchschnitt"][ticker] = df["Close"].mean()
            kpi_dict["Volatilität"][ticker] = df["Close"].std()

    kpi_df = pd.DataFrame(kpi_dict)
    return kpi_df

# -------------------------------
# Hauptprogramm
# -------------------------------

def main():
    """
    Hauptfunktion des Dashboards.
    
    Führt alle Schritte aus:
    1. Website konfigurieren
    2. Sidebar mit Auswahl erstellen
    3. Daten laden
    4. Daten filtern
    5. Kennzahlen berechnen
    6. Visualisierung und Portfolioanalyse
    ...
    """
    # 1. Webseite konfigurieren
    logo = "Logo_StockTechPros_mit_Name.png"
    Website_Configuration.config_website(logo)

    # 2. Ticker-Liste abrufen
    tickers_dict = Tickers_List.get_tickers_dict()

    # 3. Seitenleiste erstellen & Infos holen
    selected_tickers, time_filter, show_volume = Website_Configuration.create_sidebar(tickers_dict)
    ticker_symbole = [selected_ticker.split(" ")[0] for selected_ticker in selected_tickers]

    # Prüfen, ob mindestens ein Ticker ausgewählt wurde
    if not ticker_symbole:
        st.warning("Bitte wähle mindestens eine Aktie aus, um die Analyse zu starten.")
        st.stop()  # Stoppt den Rest des Codes

    # 4. Alle Daten aus API abrufen
    all_data = Daten_aus_Yahoo_Finance.load_data_multiple_tickers(tickers_dict)

    # 5. Nur ausgewählte Ticker berücksichtigen
    filtered_data = {ticker: all_data[ticker] for ticker in ticker_symbole if ticker in all_data}

    # 6. Zeitfilter anwenden
    for ticker in filtered_data:
        filtered_data[ticker] = filter_by_date(filtered_data[ticker], time_filter)

    # 7. KPIs berechnen und anzeigen
    kpi_df = calculate_KPIs(filtered_data)
    st.header(f"{Symbols.symbols["bar_chart"]} Kennzahlen der ausgewählten Aktien")
    st.dataframe(kpi_df)
    
    # 8. Close-Preise extrahieren
    close_prices = extract_close_prices(filtered_data)

    # 9. Diagramme anzeigen
    display_charts(close_prices, filtered_data, show_volume)


# -------------------------------
# Streamlit ausführen
# -------------------------------
if __name__ == "__main__":
    main()

# Streamlit im Browser ausführen -> Befehl: streamlit run main.py

