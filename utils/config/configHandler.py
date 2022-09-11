import json
import logging
import os
import threading
import time
import jsonschema

class ConfigHandler:
    def __init__(self, config_path: str, schema_path: str):

        self.config_path = config_path
        self.schema_path = schema_path
        self.settings = str()
        self.__schema = str()
        self.__skip_val = False
        self.__modified_by_write = False
        self.__issues = False

        # fate finta che non esista, è solo di supporto
        def getType(type):
            types = {
                "array": list(),
                "boolean": bool(),
                "number": float(),
                "string": str(),
                "object": dict(),
                "integer": int()
            }
            if type in types.keys():
                return types[type]

        # troppo tempo speso a fare sta roba...
        class RecursiveGenerator:
            def __init__(self, current_position, previous_key = None):
                self.current_position = current_position
                self.previous_key = previous_key
                self.result = None

            def recursive(self):
                template = dict()
                for key, value in self.current_position.items():
                    template.update({key: getType(value["type"])})
                    if value["type"] == "array":
                        new_instance = RecursiveGenerator(value["items"]["properties"], key)
                        new_instance.recursive()
                        template[new_instance.previous_key].append(new_instance.result)
                self.result = template

        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Il file schema \"{self.schema_path}\" non esiste!\nScaricarlo dalla documentazione qui:\nhttps://github.com/TheTecnoKing/RoboTranslator/blob/main/schema.json")

        with open(self.schema_path, mode="r") as schema:
            self.__schema = json.load(schema)
            schema.close()

        if not os.path.exists(self.config_path) or os.path.getsize(self.config_path) == 0:
            logging.warning(f"Il file di configurazione \"{self.config_path}\" non esiste oppure è vuoto! Generazione di una nuova configurazione...")
            rec = RecursiveGenerator(self.__schema["properties"])
            rec.recursive()
            rec.result.update({"scanDevices": True})
            with open(self.config_path, mode="w") as new_config:
                json.dump(rec.result, new_config, indent=2)
                new_config.close()
        logging.info("Configurazione creata correttamente!")

    def loadConfig(self):
        self.__issues = False
        with open(self.config_path, mode="r") as config_file:
            try:
                self.settings = json.load(config_file)
            except json.decoder.JSONDecodeError as error:
                self.__issues = True
                logging.error("La configurazione non è in un formato JSON valido!")
                logging.error("Controllare eventuali errori di battitura. Per maggiori informazioni vedi sotto.")
                logging.error("JSONDecodeError: %s", error)
            config_file.close()
        if self.__skip_val:
            self.__skip_val = False
        else:
            # aggiusta il formato con cui sputa gli errori di validazione
            try:
                jsonschema.validate(self.settings, self.__schema)
            except jsonschema.ValidationError as error:
                self.__issues = True
                logging.error("La configurazione non rispetta il suo schema!")
                logging.error("Controllare che i tipi dei dati siano corretti. Per maggiori informazioni vedi sotto.")
                logging.error("ValidationError: %s", error)
        if not self.__issues:
            logging.debug("Configurazione (ri)caricata correttamente!")
        else:
            logging.warning("^^^ Si sono verificati degli errori nel (ri)caricare la configurazione. ^^^")

    def watchConfig(self):
        # mi tocca fare polling sul file...
        def watcher(self, config_path: str, refresh_interval: float = 1, __temp: bool = False):
            cached_time = os.stat(config_path).st_mtime
            while True:
                last_modified = os.stat(config_path).st_mtime
                if last_modified != cached_time and not self.__modified_by_write:
                    logging.info("Rilevate modifiche nella configurazione!")
                    self.loadConfig()
                    cached_time = last_modified
                    if not self.__issues and refresh_interval != self.settings["configRefresh"]:
                        refresh_interval = self.settings["configRefresh"]
                        if __temp:
                            __temp = False
                            logging.info("La configurazione è ora valida! D'ora in avanti il file verrà monitorato seguendo i parametri impostati dall'utente.")
                elif self.__modified_by_write:
                    self.__modified_by_write = False
                    cached_time = last_modified
                time.sleep(refresh_interval)
        
        if self.__issues:
            logging.warning("Si sono verificati degli errori nel leggere la configurazione. Il monitoraggio del file verrà comunque avviato con un intervallo di 1 secondo.")
            config_watcher = threading.Thread(target=watcher, args=(self, self.config_path, 1, True), daemon=True)
        else:
            config_watcher = threading.Thread(target=watcher, args=(self, self.config_path), daemon=True)
        config_watcher.start()
        logging.debug("Monitoraggio del file di configurazione avviato!")

    # funziona solo per il primo livello di cambiamenti, non per nested
    def writeConfig(self, **changes):
        tmp_config = self.settings
        tmp_config.update(changes)
        jsonschema.validate(tmp_config, self.__schema)
        self.__modified_by_write = True
        with open(self.config_path, mode="w") as config_file:
            json.dump(tmp_config, config_file, indent=2)
            config_file.close()

        logging.debug("Configurazione salvata correttamente!")

        self.__skip_val = True
        self.loadConfig()

        # (opzionale) verifica in che contesto sta avvenendo la scrittura file:
        # non posso scrivere dati sui dispositivi se chiedo una modifica da firstboot
        # posso solo scriverli se a richiederlo è stato il modulo giusto (connect.py)

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