import bluetooth
import json
from simple_term_menu import TerminalMenu

with open("config.json", mode="r") as config:
    settings = json.load(config)
    config.close()

print("Cercando i dispositivi Bluetooth disponibili per {0} secondi...".format(settings["scanDuration"]))
devices = bluetooth.discover_devices(duration=settings["scanDuration"], lookup_names=True)
deviceList = []
for i in range(0, len(devices)):
    deviceList.append(devices[i][0] + " - " + devices[i][1])

terminal_menu = TerminalMenu(
    deviceList,
    title="Seleziona i dispositivi con cui vuoi connetterti:",
    multi_select=True,
    show_multi_select_hint=True,
    multi_select_select_on_accept=False,
    multi_select_empty_ok=True,
    clear_menu_on_exit=False
)
menu_entry_indices = terminal_menu.show()

with open("config.json", mode="w") as config:
    deviceList.clear()
    for i in range (0, len(menu_entry_indices)):
        deviceList.append(devices[menu_entry_indices[i]][0])
    settings["devices"] = deviceList
    json.dump(settings, config)
    config.close()

print("Dispositivi salvati nella configurazione!")