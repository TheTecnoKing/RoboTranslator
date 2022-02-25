# al momento non ho modo di testare la connettività multipla tra dispositivi

import bluetooth
import json
import concurrent.futures
import logging
import uuid

with open("config.json", mode="r") as config:
    settings = json.load(config)
    config.close()

def connectDevices(threadID: int, uuid: str):
    ssock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    ssock.bind(("", bluetooth.PORT_ANY))
    ssock.listen(1)
    port = ssock.getsockname()[1]

    bluetooth.advertise_service(
        sock=ssock,
        name="RoboTranslator",
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE]
    )
    logging.info("(THREAD %s) Servizio Bluetooth attivo! In ascolto nel canale: %s", threadID, port)
    logging.debug("(THREAD %s) UUID: %s", threadID, uuid)

    csock, cinfo = ssock.accept()
    if cinfo[0] in settings["devices"].keys():
        logging.info("(THREAD %s) Dispositivo connesso! %s - %s", threadID, cinfo[0], settings["devices"].get(cinfo[0]))
    else:
        csock.close()
        logging.warning("(THREAD %s) Tentativo di connessione da parte di %s negato! Dispositivo non riconosciuto!", threadID, cinfo[0])

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
    # fine copiaticcio

# un giorno questo andrà dritto dritto nel main.py
if __name__ == "__main__":
    format = "%(asctime)s | [%(levelname)s] %(message)s"
    # il livello di log verrà definito tramite parametro CLI in futuro
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    # questa variabile dovrà essere ricavata dal n. di dispositivi nel JSON
    devices = 5

    # devo vedere se uuid diversi servano effettivamente o posso usarne sempre uno e basta
    uuids = list()
    for i in range(devices):
        uuids.append(str(uuid.uuid4()))

    with concurrent.futures.ThreadPoolExecutor(max_workers=devices) as executor:
        executor.map(connectDevices, range(devices), uuids)