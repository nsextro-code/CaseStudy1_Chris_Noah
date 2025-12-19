"""
UI Layer - Streamlit User Interface
Enthält alle UI-Funktionen für die 4 Use Cases
"""

import streamlit as st
import pandas as pd
from datetime import datetime


# ==================== USE CASE 1: NUTZERVERWALTUNG ====================
def show_users():
    """
    UI für Nutzerverwaltung
    """
    st.header("👥 Nutzerverwaltung")
    
    # Neuen Nutzer anlegen
    st.subheader("Neuen Nutzer anlegen")
    
    with st.form("user_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input(
                "E-Mail-Adresse *",
                placeholder="beispiel@mci.edu",
                help="Die E-Mail dient als eindeutige ID"
            )
        
        with col2:
            name = st.text_input(
                "Name *",
                placeholder="Max Mustermann",
                help="Vollständiger Name des Nutzers"
            )
        
        submitted = st.form_submit_button("✅ Nutzer anlegen", width="stretch")
        
        if submitted:
            if email and name:
                if "@" in email:
                    st.success(f"✅ Nutzer **{name}** mit E-Mail **{email}** wurde angelegt!")
                    st.info("ℹ️ Daten wurden gespeichert")
                else:
                    st.error("❌ Ungültige E-Mail-Adresse!")
            else:
                st.error("❌ Bitte alle Pflichtfelder (*) ausfüllen!")
    
    st.markdown("---")
    
    # Alle Nutzer anzeigen
    st.subheader("Alle Nutzer")
    
    # DUMMY-DATEN 
    dummy_users = pd.DataFrame([
        {"Name": "Max Mustermann", "E-Mail": "max.mustermann@mci.edu"},
        {"Name": "Anna Schmidt", "E-Mail": "anna.schmidt@mci.edu"},
        {"Name": "Peter Huber", "E-Mail": "peter.huber@mci.edu"},
        {"Name": "Lisa Müller", "E-Mail": "lisa.mueller@mci.edu"}
    ])
    
    st.dataframe(
        dummy_users,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Gesamt: {len(dummy_users)} Nutzer")
    
    # Aktionen
    st.markdown("---")
    st.subheader("Aktionen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Nutzer löschen", width="stretch"):
            st.warning("⚠️ Löschen-Funktion noch nicht implementiert")
    
    with col2:
        if st.button("✏️ Nutzer bearbeiten", width="stretch"):
            st.warning("⚠️ Bearbeiten-Funktion noch nicht implementiert")
    
    with col3:
        if st.button("🔄 Liste aktualisieren", width="stretch"):
            st.rerun()


# ==================== USE CASE 2: GERÄTEVERWALTUNG ====================
def show_devices():
    """
    UI für Geräteverwaltung
    """
    st.header("🖨️ Geräteverwaltung")
    
    st.subheader("Neues Gerät anlegen")
    
    with st.form("device_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            device_id = st.number_input(
                "Inventarnummer *",
                min_value=1,
                step=1,
                help="Eindeutige ID des Geräts"
            )
            device_name = st.text_input(
                "Gerätename *",
                placeholder="3D-Drucker Prusa MK4"
            )
            responsible = st.selectbox(
                "Verantwortliche Person *",
                ["Max Mustermann", "Anna Schmidt", "Peter Huber", "Lisa Müller"],
                help="Wählen Sie einen bestehenden Nutzer aus"
            )
            end_of_life = st.date_input(
                "End-of-Life Datum *",
                help="Datum ab welchem das Gerät nicht mehr gewartet wird"
            )
        
        with col2:
            first_maintenance = st.date_input(
                "Erste Wartung *",
                help="Datum der ersten Wartung"
            )
            maintenance_interval = st.number_input(
                "Wartungsintervall (Tage) *",
                min_value=1,
                value=90,
                help="Intervall zwischen Wartungen in Tagen"
            )
            maintenance_cost = st.number_input(
                "Wartungskosten (€) *",
                min_value=0.0,
                value=150.0,
                step=10.0,
                help="Kosten pro Wartung"
            )
        
        submitted = st.form_submit_button("✅ Gerät anlegen", width="stretch")
        
        if submitted:
            if device_name:
                st.success(f"✅ Gerät **{device_name}** mit ID **{device_id}** wurde angelegt!")
                st.info("ℹ️ Daten wurden gespeichert")
            else:
                st.error("❌ Bitte alle Pflichtfelder (*) ausfüllen!")
    
    st.markdown("---")
    st.subheader("Alle Geräte")
    
    # DUMMY-DATEN (später durch echte Datenbank ersetzen)
    dummy_devices = pd.DataFrame([
        {
            "ID": 1,
            "Name": "3D-Drucker Prusa",
            "Verantwortlich": "Max Mustermann",
            "Nächste Wartung": "2025-03-15",
            "Wartungskosten": "150 €"
        },
        {
            "ID": 2,
            "Name": "Laser-Cutter",
            "Verantwortlich": "Anna Schmidt",
            "Nächste Wartung": "2025-02-28",
            "Wartungskosten": "200 €"
        },
        {
            "ID": 3,
            "Name": "CNC-Fräse",
            "Verantwortlich": "Peter Huber",
            "Nächste Wartung": "2025-04-10",
            "Wartungskosten": "300 €"
        }
    ])
    
    st.dataframe(dummy_devices, use_container_width=True, hide_index=True)
    st.caption(f"📊 Gesamt: {len(dummy_devices)} Geräte")


# ==================== USE CASE 3: RESERVIERUNGSSYSTEM ====================
def show_reservations():
    """
    UI für Reservierungssystem
    """
    st.header("📅 Reservierungssystem")
    
    st.subheader("Neue Reservierung anlegen")
    
    with st.form("reservation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            device = st.selectbox(
                "Gerät *",
                ["3D-Drucker Prusa", "Laser-Cutter", "CNC-Fräse"],
                help="Wählen Sie ein verfügbares Gerät"
            )
            user = st.selectbox(
                "Nutzer *",
                ["Max Mustermann", "Anna Schmidt", "Peter Huber", "Lisa Müller"],
                help="Wählen Sie einen Nutzer für die Reservierung"
            )
        
        with col2:
            start_date = st.date_input(
                "Von *",
                help="Startdatum der Reservierung"
            )
            end_date = st.date_input(
                "Bis *",
                help="Enddatum der Reservierung"
            )
        
        submitted = st.form_submit_button("✅ Reservieren", width="stretch")
        
        if submitted:
            if start_date <= end_date:
                st.success(
                    f"✅ **{device}** für **{user}** von **{start_date}** bis **{end_date}** reserviert!"
                )
                st.info("ℹ️ Reservierung wurde gespeichert")
            else:
                st.error("❌ Enddatum muss nach oder gleich dem Startdatum liegen!")
    
    st.markdown("---")
    st.subheader("Aktive Reservierungen")
    
    # DUMMY-DATEN (später durch echte Datenbank ersetzen)
    dummy_reservations = pd.DataFrame([
        {
            "Gerät": "3D-Drucker Prusa",
            "Nutzer": "Max Mustermann",
            "Von": "2025-01-15",
            "Bis": "2025-01-20",
            "Status": "Aktiv"
        },
        {
            "Gerät": "Laser-Cutter",
            "Nutzer": "Anna Schmidt",
            "Von": "2025-01-22",
            "Bis": "2025-01-25",
            "Status": "Aktiv"
        },
        {
            "Gerät": "CNC-Fräse",
            "Nutzer": "Peter Huber",
            "Von": "2025-01-18",
            "Bis": "2025-01-21",
            "Status": "Aktiv"
        }
    ])
    
    st.dataframe(dummy_reservations, use_container_width=True, hide_index=True)
    st.caption(f"📊 Gesamt: {len(dummy_reservations)} aktive Reservierungen")
    
    # Aktionen
    st.markdown("---")
    if st.button("🗑️ Reservierung stornieren", width="stretch"):
        st.warning("⚠️ Stornieren-Funktion noch nicht implementiert")


# ==================== USE CASE 4: WARTUNGS-MANAGEMENT ====================
def show_maintenance():
    """
    UI für Wartungs-Management
    """
    st.header("🔧 Wartungs-Management")
    
    st.subheader("Nächste Wartungen")
    
    # DUMMY-DATEN (später durch echte Datenbank ersetzen)
    dummy_maintenance = pd.DataFrame([
        {
            "Gerät": "Laser-Cutter",
            "Verantwortlich": "Anna Schmidt",
            "Datum": "2025-02-28",
            "Kosten": "200 €",
            "Status": "Geplant"
        },
        {
            "Gerät": "3D-Drucker Prusa",
            "Verantwortlich": "Max Mustermann",
            "Datum": "2025-03-15",
            "Kosten": "150 €",
            "Status": "Geplant"
        },
        {
            "Gerät": "CNC-Fräse",
            "Verantwortlich": "Peter Huber",
            "Datum": "2025-04-10",
            "Kosten": "300 €",
            "Status": "Geplant"
        }
    ])
    
    st.dataframe(dummy_maintenance, use_container_width=True, hide_index=True)
    st.caption(f"📊 Gesamt: {len(dummy_maintenance)} anstehende Wartungen")
    
    st.markdown("---")
    st.subheader("Wartungskosten pro Quartal 2025")
    
    # Quartalskalkulation (DUMMY - später aus DB berechnen)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Q1 (Jan-Mär)",
            value="650 €",
            delta="+150 €",
            help="Wartungskosten im ersten Quartal"
        )
    
    with col2:
        st.metric(
            label="Q2 (Apr-Jun)",
            value="800 €",
            delta="+150 €",
            help="Wartungskosten im zweiten Quartal"
        )
    
    with col3:
        st.metric(
            label="Q3 (Jul-Sep)",
            value="450 €",
            delta="-350 €",
            help="Wartungskosten im dritten Quartal"
        )
    
    with col4:
        st.metric(
            label="Q4 (Okt-Dez)",
            value="600 €",
            delta="+150 €",
            help="Wartungskosten im vierten Quartal"
        )
    
    st.markdown("---")
    st.info("💰 **Gesamtkosten 2025:** 2.500 €")
    
    # Optionen
    st.markdown("---")
    st.subheader("Aktionen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✏️ Wartungsdatum ändern", width="stretch"):
            st.warning("⚠️ Ändern-Funktion noch nicht implementiert")
    
    with col2:
        if st.button("✅ Wartung durchgeführt", width="stretch"):
            st.warning("⚠️ Abschließen-Funktion noch nicht implementiert")