"""
UI Layer - Streamlit User Interface
Enthält alle UI-Funktionen für die 4 Use Cases
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.database import Database
from src.servicelayer import UserService
from src.servicelayer import DeviceManagementService
from datetime import datetime, timedelta

user_service = UserService()  # Service Layer instanziieren

@st.dialog("Nutzer per E-Mail löschen")
def delete_user_dialog():


    # Eingabefeld für E-Mail
    email = st.text_input(
        "E-Mail des Nutzers eingeben",
        placeholder="z.B. max.mustermann@mci.edu"
    )

    if st.button("Löschen"):
        if not email:
            st.warning("⚠️ Bitte eine E-Mail eingeben.")
            return

        # E-Mail in Kleinbuchstaben
        email = email.strip().lower()
        success, message = user_service.delete_user_by_email(email)

        if success:
            st.success(f"✅ {message}")
        else:
            st.warning(f"⚠️ {message}")

@st.dialog("Nutzer bearbeiten")
def edit_user_dialog():
    # Eingabefelder
    email = st.text_input(
        "E-Mail des Nutzers eingeben",
        placeholder="z.B. max.mustermann@mci.edu"
    )
    new_name = st.text_input(
        "Neuer Name",
        placeholder="z.B. Max Mustermann"
    )

    if st.button("Speichern"):
        if not email or not new_name:
            st.warning("⚠️ Bitte E-Mail und neuen Namen ausfüllen.")
            return

        success, message = user_service.update_user_name(email.strip().lower(), new_name)
        if success:
            st.success(f"✅ {message}")
        else:
            st.warning(f"⚠️ {message}")


# ==================== USE CASE 1: NUTZERVERWALTUNG ====================
def show_users():
    st.header("👥 Nutzerverwaltung")
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

        submitted = st.form_submit_button("✅ Nutzer anlegen", use_container_width=True)

        if submitted:
            success, message = user_service.register_user(email, name)

            if success:
                st.success(f"✅ {message}")
                st.info("💾 Daten wurden in der Datenbank gespeichert")
            else:
                st.warning(f"⚠️ {message}")

    st.markdown("---")
    st.subheader("📋 Alle Nutzer")

    users = user_service.get_all_users()
 
    if users:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("Noch keine Nutzer vorhanden.")
    st.markdown("---")
    st.caption(f"Gesamt: {len(users)} Nutzer")
    
    # Aktionen
    st.markdown("---")
    st.subheader("Aktionen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Nutzer löschen", width="stretch"):
            delete_user_dialog()   # ✅ SO ist es richtig

    
    with col2:
        if st.button("✏️ Nutzer bearbeiten", width="stretch"):
            edit_user_dialog()  # Dialog wird geöffnet

    
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
    
    
    user_service = UserService()
    device_service = DeviceManagementService()

    users = user_service.get_all_users()
    user_emails = [u["email"] for u in users] if users else []

    with st.form("device_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            device_id = st.number_input("Inventarnummer *", min_value=1, step=1)
            device_name = st.text_input("Gerätename *", placeholder="3D-Drucker Prusa MK4")
            if user_emails:
                responsible = st.selectbox(
                    "Verantwortliche Person (E-Mail) *",
                    user_emails,
                    help="Nur registrierte Nutzer können ausgewählt werden"
                )
            else:
                st.warning("⚠️ Noch keine Nutzer vorhanden – bitte zuerst in der Nutzerverwaltung einen Nutzer anlegen.")
                responsible = None  # Keine Auswahl möglich

            end_of_life = st.date_input("End-of-Life Datum *")

        with col2:
            first_maintenance = st.date_input("Erste Wartung *")
            maintenance_interval = st.number_input("Wartungsintervall (Tage) *", min_value=1, value=90)
            maintenance_cost = st.number_input("Wartungskosten (€) *", min_value=0.0, value=150.0, step=10.0)

        submitted = st.form_submit_button("✅ Gerät anlegen")

        if submitted:
            # Aufruf der Service-Methode
            success, message = device_service.add_device(
                device_id=device_id,
                name=device_name,
                responsible_email=responsible,
                first_maintenance=first_maintenance,
                maintenance_interval_days=maintenance_interval,
                maintenance_cost_eur=maintenance_cost,
                end_of_life=end_of_life
            )

            # Ausgabe
            if success:
                st.success(message)
            else:
                st.error(message)


        
        st.markdown("---")
        st.subheader("Alle Geräte")
        devices = device_service.get_all_devices()  # Holt alle Geräte über den Service

        if devices:
            import pandas as pd
            df = pd.DataFrame(devices)

            preferred_cols = ["device_id", "name", "responsible_email",
                            "next_maintenance", "maintenance_cost_eur", "end_of_life"]
            cols = [c for c in preferred_cols if c in df.columns] + [c for c in df.columns if c not in preferred_cols]
            df = df[cols]

            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"📊 Gesamt: {len(df)} Geräte")
        else:
            st.info("Noch keine Geräte vorhanden.")



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
    
    st.dataframe(dummy_reservations, width='stretch', hide_index=True)
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
    
    st.dataframe(dummy_maintenance, width='stretch', hide_index=True)
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
