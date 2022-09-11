# Configurazione

RoboTranslator può essere configurato andando a modificare il file `config.json` incluso nella repository oppure generato automaticamente al primo avvio.

!!! todo
    - [ ] Vanno aggiornate le spiegazioni sui parametri e la struttura d'esempio, per via del nuovo schema.
    - [ ] Magari si potrebbero aggiungere anche informazioni sul comportamento in caso di errori/mancanze/ecc...

## Struttura di `config.json`
``` json
{
  "firstTime": false,
  "devices": [
    {
      "name": "HC-05",
      "address": "2C:54:91:88:C9:E3",
      "sensors": {
        "x": [0, 1024],
        "c": ["-", 0, 1],
        ...
      },
      "actuators": {
        "y": [0, 2048],
        "b": ["-", 0, 1],
        ...
      }
    }
  ],
  "scanDuration": 5,
  "refreshInterval": 0.05,
  "timeout": 1
}
```
_Lo schema è disponibile [qui](https://github.com/TheTecnoKing/RoboTranslator/blob/main/schema.json)._

## Parametri
### `#!python firstTime: bool`

Indica al programma se esso è mai stato eseguito. Se è la prima volta che viene avviato, effettuerà, come prima cosa, una fase di ricerca e salvataggio dei dispositivi Bluetooth, altrimenti avvierà la comunicazione con i dispositivi già salvati nella sezione [`devices`](#devices-list).

### `#!python devices: list`

Questa sezione contiene tutti i dati riguardanti i dispositivi configurati. Ogni elemento di questa lista è un `#!python dict` composto da 4 chiavi:

1. `#!python name: str`<br>Nome del dispositivo
2. `#!python address: str`<br>Indirizzo MAC del dispositivo
3. <a id="sensors">`#!python sensors: dict`</a><br>Insieme dei sensori presenti sul dispositivo. È composto a sua volta da:
    - `#!python key: str`<br>Carattere indicante il tipo di sensore.<br>Non deve obbligatoriamente fare parte del database dei sensori ed attuatori, ma è **altamente consigliato** che ne faccia. Questo permette un'identificazione più facile del dato, sia lato debugging, sia lato API.
    - `#!python value: list`<br>Range di valori che possono essere ricevuti.<br>Tipicamente questa lista è formata da due elementi: uno di partenza ed uno di fine, entrambi inclusi.
    ``` json hl_lines="2"
    "sensors": {
      "x": [0, 1024],
      "c": ["-", 0, 1, ...],
      ...
    }
    ```
    Se nel primo indice è presente un trattino (`"-"`), allora i valori non verranno interpretati come valori di inizio e fine, bensì come valori a se stanti. Di conseguenza, ^^solo in questo caso^^ è possibile avere più di due valori all'interno della lista, ed essi saranno gli unici valori ad essere accettati nella ricezione dati.
    ``` json hl_lines="3"
    "sensors": {
      "x": [0, 1024],
      "c": ["-", 0, 1, ...],
      ...
    }
    ```
4. `#!python actuators: dict`<br>Insieme dei sensori presenti sul dispositivo. La sua struttura e funzionamento è identica a quella di [`sensors`](#sensors), quindi rivolgersi a quella sezione per la documentazione. Unica differenza è che, mentre `sensors` si occupa di descrivere i dati che si possono ricevere dai dispositivi, `actuators` indica quali dati possono essere inviati dal Server ai Client.

### `#!python scanDuration: int`

Imposta la durata di scansione dei dispositivi (in secondi) in caso di primo avvio (forzato e non).

### `#!python refreshInterval: float`

Imposta l'intervallo di aggiornamento dei dati (in secondi), ossia il tempo tra l'invio di una richiesta dati dal Server e un'altra (per maggiori informazioni, vedi [Protocollo](/protocol)).

### `#!python timeout: float`

Imposta il tempo massimo di timeout ricezione dati (in secondi). Per maggiori informazioni, vedi [Protocollo](/protocol).