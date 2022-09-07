import json
import logging
import os
import threading
import time
from jsonschema import validate, ValidationError

class ConfigHandler:
    def __init__(self, config_path: str, schema_path: str):

        self.config_path = config_path
        self.schema_path = schema_path
        self.settings = str()
        self.__schema = str()
        self.__skip_val = False
        self.modified_by_write = False

        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Il file di configurazione \"{self.config_path}\" non esiste!")
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Il file schema \"{self.schema_path}\" non esiste!\nScaricarlo dalla documentazione qui: <inserisci link>")

        with open(self.schema_path, mode="r") as schema:
            self.__schema = json.load(schema)
            schema.close()
    
    def loadConfig(self):
        issues = False
        with open(self.config_path, mode="r") as config_file:
            try:
                self.settings = json.load(config_file)
            except json.decoder.JSONDecodeError as error:
                issues = True
                logging.error("La configurazione non è in un formato JSON valido!")
                logging.error("Controllare eventuali errori di battitura. Per maggiori informazioni vedi sotto.")
                logging.error("JSONDecodeError: %s", error)
            config_file.close()
        if self.__skip_val:
            self.__skip_val = False
        else:
            # aggiusta il formato con cui sputa gli errori di validazione
            try:
                validate(self.settings, self.__schema)
            except ValidationError as error:
                issues = True
                logging.error("La configurazione non rispetta il suo schema!")
                logging.error("Controllare che i tipi dei dati siano corretti. Per maggiori informazioni vedi sotto.")
                logging.error("ValidationError: %s", error)
        if not issues:
            logging.debug("Configurazione (ri)caricata correttamente!")
        else:
            issues = False
            logging.warning("^^^ Si sono verificati degli errori nel (ri)caricare la configurazione. ^^^")

    def watchConfig(self):
        # mi tocca fare polling sul file...
        def watcher(self, config_path: str, refresh_interval: float):
            cached_time = os.stat(config_path).st_mtime
            while True:
                last_modified = os.stat(config_path).st_mtime
                if last_modified != cached_time and not self.modified_by_write:
                    logging.info("Rilevate modifiche nella configurazione!")
                    self.loadConfig()
                    cached_time = last_modified
                elif self.modified_by_write:
                    self.modified_by_write = False
                    cached_time = last_modified
                time.sleep(refresh_interval)

        config_watcher = threading.Thread(target=watcher, args=(self, self.config_path, self.settings["configRefresh"]), daemon=True)
        config_watcher.start()
        logging.debug("Monitoraggio del file di configurazione avviato!")
    
    
    # funziona solo per il primo livello di cambiamenti, non per nested
    def writeConfig(self, **changes):
        tmp_config = self.settings
        tmp_config.update(changes)
        validate(tmp_config, self.__schema)
        self.modified_by_write = True
        with open(self.config_path, mode="w") as config_file:
            json.dump(tmp_config, config_file, indent=2)
            config_file.close()

        logging.debug("Configurazione salvata correttamente!")

        self.__skip_val = True
        self.loadConfig()

        # (opzionale) verifica in che contesto sta avvenendo la scrittura file:
        # non posso scrivere dati sui dispositivi se chiedo una modifica da firstboot
        # posso solo scriverli se a richiederlo è stato il modulo giusto (connect.py)

"""
"sensors": {
    "name": String,
    "id": String,
    "min": roba,
    "max": roba,

    ...
}
"""

# STA ROBA NON DOVRÀ ESISTERE IN PROD
if __name__ == "__main__":
    config = ConfigHandler("/home/tecnoking/Documenti/translatorMain/config copy.json", "/home/tecnoking/Documenti/translatorMain/schema.json")
    config.loadConfig()
    config.watchConfig()
    print(config.settings["devices"])
    config.writeConfig(firstTime = True)
    while True:
        print(config.settings)
        time.sleep(1)