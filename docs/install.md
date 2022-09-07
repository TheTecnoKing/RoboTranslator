# Installazione

!!! todo
    - [ ] **Rifare la documentazione per l'installazione!**

!!! note
    L'intero progetto è stato sviluppato su un Raspberry Pi 4 con `Ubuntu 20.04.4 aarch64`, e testato anche su un Raspberry Pi 3B+ con `Debian 11 aarch64`. Di conseguenza, anche le istruzioni d'installazione sono state scritte basandosi su questi dispositivi. Se si vuole installare il software su un'altra configurazione, le procedure potrebbero essere differenti. In tal caso, una ricerca su Google o nella documentazione delle varie dipendenze non fa mai male!

1. Installare Python 3.8 o versione superiore (dovrebbe essere preinstallato nelle ultime versioni LTS di Ubuntu e Debian), `libbluetooth-dev`, `bluetooth` e `bluez`:
    ```
    sudo apt-get install python3 libbluetooth-dev bluetooth bluez
    ```
2. Modificare il servizio `bluetoothd` in modo che si avvii in modalità compatibilità aggiungendo "-C" al parametro di avvio (fonte [qui](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory)):
    
    !!! attention
        Il file del servizio viene sovrascritto ad ogni suo aggiornamento! Andare alla fonte per maggiori informazioni.
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
    !!! attention
        Questo comando **non** lo renderà ricercabile _per sempre_! Per poter eseguire il comando ad ogni avvio consiglio di dare un'occhiata alla fonte.
    ```
    sudo hciconfig hci0 piscan
    ```
5. Cambiare i permessi d'accesso al server Bluetooth del dispositivo (fonte [qui](https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi/42306883)):
    !!! attention
        Anche questo comando è temporaneo... L'andazzo è sempre lo stesso: vedi fonte per maggiori info.
    ```
    sudo chmod o+rw /var/run/sdp
    ```
6. Clonare la repository:
    ```
    git clone https://github.com/TheTecnoKing/RoboTranslator.git
    ```
!!! todo
    7. (TODO) Installare le varie dipendenze per l'esecuzione del software:
        ```
        python3 -m pip install -r requirements.txt
        ```
**Et voilà!** Lavoro finito!