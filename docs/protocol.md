# Protocollo

!!! todo
    - [ ] separa comunicazione e protocollo in due file separati, ma cmq nella stessa cartella
    - [ ] descrivi la struttura del messaggio

Tutti i dati sono contenuti in messaggi da 4 byte ciascuno.

## Struttura del messaggio

## Comunicazione standard
``` mermaid
    sequenceDiagram
        autonumber
        Server->>Client: '@' (richiesta dati)
        activate Server
        Client->>Server: Dati sensori
        Note left of Server: Durata: `refreshInterval` + tempo di risposta
        Server->>Client: Comando
        deactivate Server
        Client->>Server: Dati sensori
```
_Immagine PNG disponibile <a href="https://mermaid.ink/img/pako:eNqdUT1rAzEM_SvCS1qa_gEPoZB06NIlq4eoZ11PcLavshwoIf-9CnfkOnWoJvE-xOPp4roSyXkHNpW-GuWODoyfgilkWAabltzSB8mKHUnOJM-73X5kyuph87KBB-FuYKqKEFH58deJTvmMSotvJWa73ZkJDwczWpRci_Aqey_mHalXKD3cpU1Q0cNJqBeqw1tWY3A8wRMopalAZBCuU7FEf0Tfl4Q5llUR6X953dYlkoQcrdLLzRScDpQoOG9rpB7bqMGFfDVpm6wkeo2sRZzvcay0dbeuj9-5uwOzavnJgl5_AIMMjn0" target="_blank">qui</a>_

1. Il Server effettua una richiesta dati al Client tramite l'invio di un singolo `char`: `'@'`.
2. Il Client risponde con i dati di tutti i suoi sensori, ognuno di essi seguente la struttura del messaggio descritta [sopra](#struttura-del-messaggio).
3. Il Server invia un comando al Client con la struttura definita nella sezione "[Struttura del messaggio](#struttura-del-messaggio)".
4. Il client effettua l'azione programmata nel suo codice e restituisce al Server i dati di tutti i suoi sensori.

## Comunicazione per errori lato client
``` mermaid
    sequenceDiagram
        autonumber
        Server->>Client: '@'/Comando
        loop MAX x3
        Client--xServer: Timeout/dati invalidi
        activate Server
        Note left of Server: Max. durata: `timeout`
        Server->>Client: Ripete '@'/Comando
        deactivate Server
        end
        alt FINE LOOP
        Note over Client: Guasto!
        end
        Client->>Server: Dati sensori
```
_Immagine PNG disponibile <a href="https://mermaid.ink/img/pako:eNp9UcFOAjEQ_ZWxFy4gB2972GgAjYmAEQ8e9sCwndUmbQe70w2G8O-W7OISI86pefPmvdeZvSpZk8oUpKrpM5IvaWrwPaArPHSFUdhHt6HQYysKDYVRnk-sIS8ZDG4H4wk79Jp7lmXewvzuDXY3PdhOjEa7ViODV-OIo4w1igHjG7RGmzP7UkyDQp1n31hwAi1VAlzBSWyOu2vQMaBgBmtppdf_BH8xW0o6f-bXdNGcvD6LaAXuHxczeFoun38F5DQGJ7OHiLXw1QWZbjN5fvrM9LiRmnzNwaihchQcGp3utT8OFUo-yFGhsvTUVGG0UqjCHxI1btM2aaaNcFBZhbamoToecvXlyx-gZXUH79DDNzSmpWw" target="_blank">qui</a>_

1. Il Server invia un comando generico al Client.
2. Il Client riceve il messaggio e restituisce i dati di tutti i suoi sensori, però, dal lato server:
    * Avviene un timeout (i dati ci hanno messo troppo ad arrivare, o non sono proprio partiti)
    * I dati ricevuti sono invalidi (fuori dal range impostato in [`config.json`](/config/#sensors))
3. Il Server riconosce l'errore e **rimanda l'ultimo messaggio inviato in precedenza**. Ciò può avvenire per ^^massimo 3 volte^^, alla fine delle quali il Client viene contrassegnato come guasto.
4. Il Client invia nuovamente i dati di tutti i suoi sensori correttamente.

## Comunicazione per errori lato server
``` mermaid
    sequenceDiagram
        autonumber
        loop MAX x3
        Server--xClient: '@'/Comando (problemi d'invio)
        activate Server
        Server-->>Server: In attesa...
        Note left of Server: Durata: `timeout`
        Server->>Client: Ripete '@'/Comando per timeout
        deactivate Server
        end
        alt FINE LOOP
        Note over Server: Guasto!
        end
        Client->>Server: Dati sensori
```
_Immagine PNG disponibile <a href="https://mermaid.ink/img/pako:eNp1UsFOwkAQ_ZVxL2gCePDWQ6MBNCQKRi4eemDoTnWT7k7dzhIM4d9d0kIbCXOavLz39k3e7lXOmlSiIE5NP4FcTlODXx5t5qAdDMIu2A35DiuZK3h7-oTdQweuyG_Jj0a7SWnISQKDx8H9hC06zXBbed6UZA3ogXFbw3e9F3IxWxRqHS4d07TZEpg7QBGqcTwed7wFR3FJhQAXcKJOg0fBBNZiLHGQ9YVvmp6SfpiKokU_cEUeWmUn1HQ1Kzndu6gUeJ4vZvC6XL7_y8lRdg75ErAWvrli08TrnT9FMbEpV7M3aqgseYtGxwb3R1Gm5JssZSqJq6YCQymZytwhUkOlY-qZNsJeJQWWNQ3VsdrVr8vPQMNqv0CLHv4AtaerGQ" target="_blank">qui</a>_

1. Il Server invia un comando generico al Client, ma il messaggio non riesce ad arrivare integro al Client a causa di errori o mancato invio.
2. Il Client, non avendo ricevuto un messaggio valido, non risponde al Server. Quest'ultimo si mette in attesa di una risposta dal Client, che non arriverà mai.
3. Passa un certo tempo di `timeout` [(`config.json`)](/config/#timeoutfloat) nel quale il Server non riceve i dati, ed esso capisce che è qualcosa è andato storto. Di conseguenza, il Server rimanda **l'ultimo messaggio inviato in precedenza**. Questa procedura può essere ripetuta ^^massimo 3 volte^^, dopo la quale il Server segnala un guasto alla comunicazione.
4. Il client riceve un messaggio valido ed invia i dati di tutti i suoi sensori.

## Riepilogo
``` mermaid
    sequenceDiagram
        rect rgba(76, 174, 79, 0.5)
        Server->>Client: '@'/Comando
        activate Server
        Client->>Server: Dati sensori
        end
        Note left of Server: Durata: `refreshInterval` + tempo di risposta
        rect rgba(172, 174, 76, 0.2)
        alt ERRORE CLIENT
        Server->>Client: '@'/Comando
        deactivate Server
        loop MAX x3
        Client--xServer: Timeout/dati invalidi
        activate Server
        Note left of Server: Max. durata: `timeout`
        Server->>Client: Ripete '@'/Comando
        deactivate Server
        end
        rect rgba(174, 76, 76, 0.5)
        alt FINE LOOP
        Note over Client: Guasto!
        end
        end
        Client->>Server: Dati sensori
        end
        end
        rect rgba(172, 174, 76, 0.2)
        alt ERRORE SERVER
        loop MAX x3
        Server--xClient: '@'/Comando (problemi d'invio)
        activate Server
        Server-->>Server: In attesa...
        Note left of Server: Durata: `timeout`
        Server->>Client: Ripete '@'/Comando per timeout
        deactivate Server
        end
        rect rgba(174, 76, 76, 0.5)
        alt FINE LOOP
        Note over Server: Guasto!
        end
        end
        Client->>Server: Dati sensori
        end
        end
```
_Immagine PNG disponibile <a href="https://mermaid.ink/img/pako:eNrFVE1P4zAQ_SuzvhREGpbPihzQrkpAlaBdpQjtIYcO8QQsJXbWmaAixH_HVRICbMsWJLQ-xZ43k3lvnv0gEiNJBALcKulPRTqhE4U3FvNYQ7MsJQz25ho3Boce7Az2PRgcefDdP9jsQFOyd2T7x8fDTJHmAHo_ettDk6OWpkNhwuoOmRp4F6izXHodCOAEWbmWdGms6mCkZbcZG1coo5TBpPCcV1lkDGBmKbVU3o40uwhmM9gCprwwIBVYVRamZFzGcWew25I8XJDcfUESM4YwiiZRCMPzUTi-_Ch_SSsVyIwp4OLnb5jv_SVLf97Su1Q5mYq35UIepR0xJdUa-i7V6gLnPshWMK5Lz97hFKmCXJ2PUns1tZdKNyLXQh-8Efp0NA7hfDL59YaFcbWh7eiswpLNtxX_erX5jMVWdr6WR6ZhdBVG_xhxI3J_vsQ4sFFYc51RrkD23LSV2Vxj1m3FjulIAzJTib7vr3t_PmUHKNxsmsz_ZY2WyddbQ3giJ5ujku4JfViEYsG3lFMsAvcpKcUq41jE-tFBq8JdWgqlYmNFkGJWkiewYjO918nzQY1q3uDm9PEJCj-l6A" target="_blank">qui</a>_