import logging
import os.path
import concurrent.futures
from utils.bluetooth import discover, connect
# vedi se è per forza necessario passare la instance di confighandler alle altre funzioni, 
# al posto di prenderle come assunto come fa logging
from utils.config import ConfigHandler
# from utils.threads import ThreadManager (?)

# SISTEMA LA FORMATTAZIONE DI TUTTI I NOMI VARIABILI/FUNZIONI/CLASSI:
# variabile: snake_case
# funzione: camelCase
# classe: PascalCase
# al momento ConfigHandler, discover rispettano queste regole

log_format = "%(asctime)s,%(msecs)d | [%(levelname)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG, datefmt="%H:%M:%S")

logging.info("RoboTranslator, by Kristian Ceribashi and Andrea Gennaioli")
logging.info("https://github.com/TheTecnoKing/RoboTranslator")

exec_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigHandler(f"{exec_path}/config.json", f"{exec_path}/schema.json")
config.loadConfig()
config.watchConfig()
settings = config.settings

# USARE FIRSTBOOT SOLO COME PARAMETRO DEV!
if settings["devices"] == [] or settings["scanDevices"]:
    logging.warning("Nessun dispositivo memorizzato nella configurazione!")
    discover(settings["scanDuration"], config)
    config.writeConfig(ad_canis = True) # a quanto pare viene aggiunto come nuovo nel JSON... NO! dev'essere severo e non aggiungere roba al di fuori della struttura base presente!

logging.info("Connessione ai dispositivi in corso...")
logging.debug("Avvio di %s thread in corso...", len(settings["devices"]))

# try:
#     # bisogna vedere se gli sto passando una copia o un "puntatore"
#     # in modo da avere le impostazioni sempre aggiornate, anche in caso di live refresh
#     with concurrent.futures.ThreadPoolExecutor(max_workers=len(settings["devices"])) as executor:
#         # CERCA DI CAPIRE MEGLIO COME LI VUOLE GLI ARGOMENTI DELLA FUNZIONE MULTITHREAD
#         executor.map(connect, range(len(settings["devices"])), settings["devices"][0]["address"], settings["devices"][0]["name"], refresh)
# except ValueError:
#     logging.fatal("Impossibile avviare i thread per la connessione ai dispositivi:")
#     logging.fatal("Non sono stati trovati dispositivi nella configurazione!")

connect(0, settings["devices"][0]["address"], settings["devices"][0]["name"], settings["dataRefresh"])

print("siamo entrati nell'infinito")
while True:
    pass