import bluetooth
import logging
from utils.config import ConfigHandler
from simple_term_menu import TerminalMenu

def discover(scanDuration, ConfigHandlerInstance: ConfigHandler = None):
    logging.info("Cercando i dispositivi Bluetooth disponibili per %s secondi...", scanDuration)
    devices_found = bluetooth.discover_devices(duration=scanDuration, lookup_names=True)
    menu_options = list()
    for i in range(0, len(devices_found)):
        menu_options.append(devices_found[i][0] + " - " + devices_found[i][1])

    menu = TerminalMenu(
        menu_options,
        title="Seleziona i dispositivi con cui vuoi connetterti:",
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        multi_select_empty_ok=True
    )
    selected = menu.show()

    """
    "devices": {
        "name": String!,
        "address": String!,
        "sensors": Dict,
        "actuators": Dict
    }
    """
    """
    deviceList: [("address", "name"), (...)]
    """
    saved_devices = list()
    if selected != None:
        for i in selected:
            # questa roba dovrebbe essere fatta solo per un nuovo dispositivo
            # in caso si vuole semplicemente cambiare dispositivo (quindi solo nome e indirizzo),
            # bisogna prendere dal config anche i parametri sensors e actuators
            device_dict = dict()
            device_dict.update({"name": devices_found[i][1]})
            device_dict.update({"address": devices_found[i][0]})
            device_dict.update({"sensors": dict()})
            device_dict.update({"actuators": dict()})
            saved_devices.append(device_dict)
        ConfigHandlerInstance.writeConfig(devices = saved_devices, firstTime = False)
        device_names = list()
        for device in saved_devices:
            device_names.append(device["name"])
        logging.info("Dispositivi salvati nella configurazione! (%s)", *device_names)
    else:
        logging.error("Nessun dispositivo selezionato! Ciò comporterà l'interruzione del programma!")

    return saved_devices

# DA USARE SOLO IN DEVELOPMENT, NON IN PROD
if __name__ == "__main__":
    device_list = discover(5)
    print(device_list)
