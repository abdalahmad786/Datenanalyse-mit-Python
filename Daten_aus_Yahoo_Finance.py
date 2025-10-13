import streamlit as st
import yfinance as yf
import pandas as pd
import xlsxwriter

# Cache-Decorator: Funktion wird nur einmal ausgeführt
@st.cache_data(show_spinner=False)
def load_data_multiple_tickers(ticker_dict, filename="Daten.xlsx", period="5y"):
    """
    Holt historische Kursdaten von yfinance und speichert sie als CSV.
    
    ticker_symbol: z. B. "AAPL"
    filename: Name der CSV-Datei
    period: Zeitraum, z. B. "1mo", "3mo", "1y"
    
    Lädt historische Kursdaten für mehrere Ticker von yfinance
    und speichert sie in separaten Reitern einer Excel-Datei.
    
    ticker_list: Liste von Tickersymbolen
    filename: Name der Excel-Datei (.xlsx)
    period: Zeitraum, z. B. "1mo", "3mo", "1y"
    """

    all_data = {}
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for ticker_symbol, ticker_beschreibung in ticker_dict.items():
            print(f"Lade Daten für {ticker_symbol} ({ticker_beschreibung}) ...")
            ticker = yf.Ticker(ticker_symbol)
            data = ticker.history(period=period)

            if data.empty:
                print(f"Keine Daten für {ticker_symbol} gefunden.")
                continue

            # Zeitzone entfernen
            data.index = data.index.tz_localize(None)

            # In Excel schreiben
            sheet_name = ticker_symbol[:31]  # max. 31 Zeichen für Excel
            data.to_excel(writer, sheet_name=sheet_name)
            print(f"{ticker_symbol} hinzugefügt.")

            # In Dictionary speichern
            all_data[ticker_symbol] = data
    

    print(f"\nAlle Daten wurden in '{filename}' gespeichert.")
    return all_data