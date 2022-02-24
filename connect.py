# al momento non ho modo di testare la connettività multipla tra dispositivi
# inoltre non è neanche predisposto per più connessioni per ora

import bluetooth
import json

with open("config.json", mode="r") as config:
    settings = json.load(config)
    config.close()

ssock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
ssock.bind(("", bluetooth.PORT_ANY))
ssock.listen(1)
uuid = settings["uuid"]

bluetooth.advertise_service(
    sock=ssock,
    name="RoboTranslator",
    service_id=uuid,
    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE]
)
print("Servizio Bluetooth attivo! In attesa di connessione dai dispositivi...")

csock, cinfo = ssock.accept()
if cinfo[0] in settings["devices"].keys():
    print("Dispositivo connesso!", cinfo[0] + " - " + settings["devices"].get(cinfo[0]))
else:
    csock.close()
    print("Tentativo di connessione da parte di {0} negato! Dispositivo non riconosciuto!".format(cinfo[0]))

# da qui inizia il copiaticcio per gli esperimenti, nulla di definitivo da qui in poi
try:
    while True:
        data = csock.recv(1024)
        if not data:
            break
        print("Received", data)
except OSError:
    pass

print("Disconnected.")

csock.close()
ssock.close()
print("All done.")