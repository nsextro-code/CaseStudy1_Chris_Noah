"""
Geräteverwaltungssystem für Hochschulen
Haupteinstiegspunkt der Anwendung
"""

import streamlit as st
from src.ui import show_users, show_devices, show_reservations, show_maintenance

# Seiten-Konfiguration (muss als erstes kommen!)
st.set_page_config(
    page_title="Geräteverwaltung",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titel der Anwendung
st.title("🏫 Geräteverwaltungssystem")
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("Wählen Sie einen Bereich:")

page = st.sidebar.radio(
    "Menü",
    [
        "👥 Nutzerverwaltung",
        "🖨️ Geräteverwaltung",
        "📅 Reservierungssystem",
        "🔧 Wartungs-Management"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Hinweis:** Alle Änderungen werden automatisch gespeichert.")

# Page Routing - Zeigt die ausgewählte Seite an
if page == "👥 Nutzerverwaltung":
    show_users()

elif page == "🖨️ Geräteverwaltung":
    show_devices()

elif page == "📅 Reservierungssystem":
    show_reservations()

elif page == "🔧 Wartungs-Management":
    show_maintenance()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Geräteverwaltung v1.0 | MCI 2024")