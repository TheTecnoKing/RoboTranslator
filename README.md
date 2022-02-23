# RoboTranslator
Software del layer di traduzione per la comunicazione tra microcontrollori e server web. Parte del progetto PON di Robotica dell'ITIS "E. Mattei", Urbino, A.S. 2021-2022.

## Panoramica
RoboTranslator è un software scritto in Python che si occupa di fare da ponte tra dei robot comandati da microcontrollori (Arduino in questo caso) e un server di gestione/comando.
Spiegando meglio, esso scambia dati con i microcontrollori tramite una connessione seriale via Bluetooth, li elabora per renderli più manipolabili, e infine li rende disponibili tramite una API in REST oppure WebSocket.

## Installazione
> Nota: <br> L'intero progetto è stato sviluppato su un Raspberry Pi 4 con `Ubuntu 20.04.4 aarch64`, e testato anche su un Raspberry Pi 3B+ con `Debian 11 aarch64`. Di conseguenza, anche le istruzioni d'installazione sono state scritte basandosi su questi dispositivi. Se si vuole installare il software su un'altra configurazione, le procedure potrebbero essere differenti. In tal caso, una ricerca su Google o nella documentazione delle varie dipendenze non fa mai male!

1. Installare Python 3.8 o versione superiore (dovrebbe essere preinstallato nelle ultime versioni LTS di Ubuntu e Debian), `libbluetooth-dev`, `bluetooth` e `bluez`:
    ```
    sudo apt-get install python3 libbluetooth-dev bluetooth bluez
    ```
2. Modificare il servizio `bluetoothd` in modo che si avvii in modalità compatibilità aggiungendo "-C" al parametro di avvio (fonte [qui](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory)):
    > **Attenzione!** Il file del servizio viene sovrascritto ad ogni suo aggiornamento! Andare alla fonte per maggiori informazioni.
    ```
    sudo nano /etc/systemd/system/dbus-org.bluez.service
        [...]
        ExecStart=/usr/lib/bluetooth/bluetoothd -C
    ```
3. Aggiungere il profilo seriale a SDP:
    ```
    sudo sdptool add SP
    ```
4. Rendere il dispositivo ricercabile (fonte [qui](https://unix.stackexchange.com/questions/92036/enabling-bluetooth-discoverability-upon-start-up)):
    > **Attenzione!** Questo comando **non** lo renderà ricercabile _per sempre_! Per poter eseguire il comando ad ogni avvio consiglio di dare un'occhiata alla fonte.
    ```
    sudo hciconfig hci0 piscan
    ```
5. Cambiare i permessi d'accesso al server Bluetooth del dispositivo (fonte [qui](https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi/42306883)):
    > **Attenzione!** Anche questo comando è temporaneo... L'andazzo è sempre lo stesso: vedi fonte per maggiori info.
    ```
    sudo chmod o+rw /var/run/sdp
    ```
6. Clonare la repository:
    ```
    git clone https://github.com/TheTecnoKing/RoboTranslator.git
    ```
7. (WORK IN PROGRESS) Installare le varie dipendenze per l'esecuzione del software:
    ```
    python3 -m pip install -r requirements.txt
    ```
**Et voilà!** Lavoro finito!

## Uso
WORK IN PROGRESS

## Documentazione
WORK IN PROGRESS

## Crediti e licenze
Software sviluppato da [Kristian Ceribashi](https://github.com/TheTecnoKing), 3A-AU, ITIS "E. Mattei" - Urbino, 2021-2022.<br>
Software sviluppato per il progetto PON di robotica "Costruiamo un robot".<br>
Licenza _GPLv3_ (per ora ignorare, grazie)

Progetti Open Source utilizzati per lo sviluppo del progetto:
- [Python](https://www.python.org/), licenza [PSF](https://docs.python.org/3/license.html#psf-license) _necessario?_
- [PyBluez](https://github.com/pybluez/pybluez), licenza [GPLv2](https://github.com/pybluez/pybluez#license)
- [FastAPI](https://fastapi.tiangolo.com/), licenza [MIT](https://github.com/tiangolo/fastapi/blob/master/LICENSE)
- [Uvicorn](https://github.com/encode/uvicorn), licenza [BSD 3-Clause "New" or "Revised" License](https://github.com/encode/uvicorn/blob/master/LICENSE.md)
- [Simple Terminal Menu](https://github.com/IngoMeyer441/simple-term-menu), licenza [MIT](https://github.com/IngoMeyer441/simple-term-menu/blob/develop/LICENSE)