from src.database import Database
from datetime import datetime, date, timedelta


class UserService:
    def __init__(self):
        self.db = Database()  # Singleton, DB wird nur einmal geöffnet

    def register_user(self, email: str, name: str):
        """
        Business-Logik zum Anlegen eines Nutzers
        Prüft Pflichtfelder, E-Mail-Format und vorhandene Nutzer.
        Gibt Tuple (success: bool, message: str) zurück
        """
        # Pflichtfelder prüfen
        if not email or not name:
            return False, "Bitte alle Pflichtfelder (*) ausfüllen!"
        
        # E-Mail-Format prüfen
        if "@" not in email:
            return False, "Ungültige E-Mail-Adresse!"
        
        # Prüfen, ob Nutzer bereits existiert
        existing_user = self.db.users.search(lambda u: u.get("email") == email)
        if existing_user:
            return False, "Nutzer mit dieser E-Mail existiert bereits."
        
        # Nutzer in DB anlegen
        self.db.users.insert({"email": email, "name": name})
        return True, f"Nutzer '{name}' mit E-Mail '{email}' wurde erfolgreich angelegt!"
    
    def get_all_users(self):

        return self.db.users.all()
    
    def delete_user_by_email(self, email: str):
        user = self.db.users.search(lambda u: u.get("email") == email)
        
        if not user:
            return False, f"Nutzer mit E-Mail '{email}' nicht gefunden."
        
        # Nutzer löschen (ID aus Treffer holen)
        user_id = user[0].doc_id
        self.db.users.remove(doc_ids=[user_id])
        
        return True, f"Nutzer mit E-Mail '{email}' wurde erfolgreich gelöscht."
    
    def update_user_name(self, email: str, new_name: str):
        """
        Aktualisiert den Namen eines Nutzers anhand der E-Mail.
        """
        # Nutzer suchen
        user = self.db.users.search(lambda u: u.get("email") == email)

        if not user:
            return False, f"Nutzer mit E-Mail '{email}' nicht gefunden."

        user_id = user[0].doc_id
        self.db.users.update({"name": new_name.strip()}, doc_ids=[user_id])
        return True, f"Nutzer '{email}' wurde erfolgreich aktualisiert."
    
class DeviceManagementService:
    def __init__(self):
        self.db = Database()

    from datetime import date, datetime, timedelta
from src.database import Database

class DeviceManagementService:
    def __init__(self):
        self.db = Database()  # Singleton-Datenbank

    def add_device(
        self,
        device_id: int,
        name: str,
        responsible_email: str,
        first_maintenance: date,
        maintenance_interval_days: int,
        maintenance_cost_eur: float,
        end_of_life: date
    ):
        """
        Business-Logik zum Anlegen eines Geräts.
        Prüft Pflichtfelder, doppelte Device-ID und berechnet next_maintenance.
        Gibt Tuple (success: bool, message: str) zurück.
        """

        # Pflichtfelder prüfen
        if not device_id or not name or not responsible_email or not first_maintenance or not end_of_life:
            return False, "Bitte alle Pflichtfelder (*) ausfüllen!"

        # Prüfen, ob Device-ID bereits existiert
        existing = self.db.devices.search(lambda d: int(d.get("device_id", -1)) == device_id)
        if existing:
            return False, f"Ein Gerät mit der Inventarnummer {device_id} existiert bereits."

        # Nächste Wartung berechnen
        next_maintenance = first_maintenance + timedelta(days=maintenance_interval_days)

        # Gerät in die DB einfügen
        self.db.devices.insert({
            "device_id": device_id,
            "name": name.strip(),
            "responsible_email": responsible_email.strip().lower(),
            "first_maintenance": first_maintenance.isoformat(),
            "maintenance_interval_days": maintenance_interval_days,
            "maintenance_cost_eur": float(maintenance_cost_eur),
            "next_maintenance": next_maintenance.isoformat(),
            "end_of_life": end_of_life.isoformat(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "last_update": datetime.now().isoformat(timespec="seconds")
        })

        return True, f"Gerät '{name}' mit ID {device_id} wurde erfolgreich hinzugefügt."
    
    def get_all_devices(self):
        """
        Liefert eine Liste aller Geräte aus der Datenbank zurück.
        Gibt leere Liste zurück, falls keine Geräte vorhanden sind.
        """
        return self.db.devices.all()
