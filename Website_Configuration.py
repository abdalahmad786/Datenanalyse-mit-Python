import streamlit as st

import Symbols

# App-Konfiguration
def config_website(logo):
    
    # Titel links und Logo rechts einfügen
    col1, col2 = st.columns([3, 1])  # Verhältnis: 3x Platz für Text, 1x für Logo

    with col1:
        st.title("Live Stock Dashboard mit Python & Streamlit")

    with col2:
        st.image(logo, width=400)  # Logo rechts oben


    st.set_page_config(
        page_title="Webseite von Abdal Ahmad",        # Titel der Browser-Tab-Leiste
        page_icon=logo,          # Dein Logo (lokale Datei) oder Emoji
        layout="wide"                  # optional: "centered" oder "wide"
    )

    # Hintergrundfarbe über Markdown + Style ändern
    st.markdown(
        """
        <style>
        .stApp {
        background-color: #f9f9f9; /* Dark gray */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Seitenleiste erstellen
def create_sidebar(tickers_dict):
    
    # Ticker-Liste erzeugen
    options = [f"{key} ({value})" for key, value in tickers_dict.items()]

    # Auswahlfeld
    # Auswahl von max. 3 Aktien mit multiselect
    
    selected_tickers = st.sidebar.multiselect(
        label="Aktien",
        options=options,
        placeholder="Bitte eine Aktie auswählen")

    # Zeitfilter
    time_filter = st.sidebar.radio(f"{Symbols.symbols['clock']} Zeitraum filtern nach:", ["Monat", "1 Jahr", "5 Jahre"]) # https://symbols.cool/time

    # Umsatz anzeigen
    show_volume = st.sidebar.checkbox("Umsätze anzeigen")

    # --- Rückgabe oder Anzeige der Auswahl ---
    st.sidebar.markdown("---") # horizontale Linie erzeugen
    st.sidebar.write(f"**Ticker:** {', '.join(selected_tickers)}")
    st.sidebar.write(f"**Zeitraum:** {time_filter}")
    st.sidebar.write(f"**Umsätze anzeigen:** {'Ja' if show_volume else 'Nein'}")
    
    return selected_tickers, time_filter, show_volume