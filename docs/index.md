# :robot: RoboTranslator
Software del layer di traduzione per la comunicazione tra microcontrollori e server web.<br>Parte del progetto di Robotica "Costruiamo un robot" [[↪]](#crediti-e-licenze).

!!! todo
    Work in progress!

## Panoramica
RoboTranslator è un software scritto in Python che si occupa di fare da ponte tra dei robot comandati da microcontrollori (in questo caso, degli Arduino) e un server di controllo.
Spiegando meglio, esso scambia dati con i microcontrollori tramite una connessione seriale via Bluetooth, li elabora per facilitarne le interazioni, e infine li rende disponibili tramite una API in REST oppure WebSocket.

## Crediti e licenze
Software sviluppato da [Kristian Ceribashi](https://github.com/TheTecnoKing), 3A-AU, e da [Andrea Gennaioli](https://github.com/AndreaGennaioli), 3B-IN, ITIS "E. Mattei" - Urbino, 2021-2022.<br>
Software sviluppato per il progetto PON di robotica "Costruiamo un robot".<br>
Il progetto in sè non ha una licenza, ma, se decidi di usarlo da qualche parte, una menzione sarebbe gradita!

Librerie Open Source utilizzate per lo sviluppo del progetto:

- [PyBluez](https://github.com/pybluez/pybluez), licenza [GPLv2](https://github.com/pybluez/pybluez#license)
- [FastAPI](https://fastapi.tiangolo.com/), licenza [MIT](https://github.com/tiangolo/fastapi/blob/master/LICENSE)
- [Uvicorn](https://github.com/encode/uvicorn), licenza [BSD 3-Clause "New" or "Revised" License](https://github.com/encode/uvicorn/blob/master/LICENSE.md)
- [Simple Terminal Menu](https://github.com/IngoMeyer441/simple-term-menu), licenza [MIT](https://github.com/IngoMeyer441/simple-term-menu/blob/develop/LICENSE)
