from tinydb import TinyDB, Query
from pathlib import Path


class Database:
    """
    Singleton-Klasse für Datenbankzugriff
    Stellt sicher, dass nur eine DB-Instanz existiert
    """
    
    _instance = None
    _db = None
    
    def __new__(cls, db_path='data/geraete.json'):
        """
        Singleton Pattern: Nur eine Instanz der Datenbank
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            
            # Stelle sicher, dass data/ Ordner existiert
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Initialisiere TinyDB
            cls._db = TinyDB(db_path, indent=4, ensure_ascii=False)
            
            print(f"✅ Datenbank initialisiert: {db_path}")
        
        return cls._instance
    
    @property
    def users(self):
        """
        Gibt die Users-Tabelle zurück
        """
        return self._db.table('users')
    
    @property
    def devices(self):
        """
        Gibt die Devices-Tabelle zurück
        """
        return self._db.table('devices')
    
    @property
    def reservations(self):
        """
        Gibt die Reservations-Tabelle zurück
        """
        return self._db.table('reservations')
    
    def close(self):
        """
        Schließt die Datenbank-Verbindung
        """
        if self._db:
            self._db.close()
            print("✅ Datenbank geschlossen")
    
    def clear_all(self):
        """
        ACHTUNG: Löscht ALLE Daten aus ALLEN Tabellen!
        Nur für Entwicklung/Testing!
        """
        self.users.truncate()
        self.devices.truncate()
        self.reservations.truncate()
        print("⚠️  Alle Tabellen geleert!")
    
    def get_stats(self):
        """
        Gibt Statistiken über die Datenbank zurück
        """
        return {
            'users': len(self.users),
            'devices': len(self.devices),
            'reservations': len(self.reservations)
        }


# Query-Objekt für Abfragen (wird in services.py benutzt)
QueryDB = Query