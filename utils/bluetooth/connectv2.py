import bluetooth
import logging
import traceback
import time

# va sistemata parecchia roba qui

'''
def receiveData(sock, id):
    # data: bytes = sock.recv(4096)
    num = data[1] | (data[2] << 8) | (data[3] << 16) | (data[4] << 24)
    logging.debug("(THREAD %s) Ricevuto: %s --- Sensore: %s --- Valore: %s", id, data, chr(data[0]), num)
    return [data[0], num]
'''
def connect(id, address, device_name, refresh):
    try:
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((address, port))
        logging.info(f"(THREAD {id}) Dispositivo connesso! {device_name} - {address}")

        while True:
            with open("data/input" + str(id) + ".txt", 'rb') as d:
                read = d.read()
                #read = "a" + chr(0xE8) + chr(0x03)
                if read:
                    cmd = read[0]
                    for i in range(0, len(read)-1, 2):
                        msg = []
                        msg.append(cmd)
                        try:
                            msg.append(read[i+1])
                            msg.append(read[i+2])
                        except IndexError:
                            msg.append(0)

                        if i+2 >= len(read) - 1:
                            msg.append(ord('#'))
                        logging.debug(msg)
                        sock.send(bytes(msg))

                        with open("data/input" + str(id) + ".txt", 'w') as dw:
                            dw.close()
                        logging.debug(f"mandato comando {msg}")
                        """ data: bytes = sock.recv(4096)
                        logging.debug(f"ricevuto {data}")
                        # todo: leggere i dati dei sensori
                        if data[-1] == '!':
                            i -= 2 """
                    d.close()
                else:
                    sock.send('@')
                    logging.debug('mandato comando @')
                    # todo: leggere i dati dei sensori
                data: bytes = sock.recv(4096)

                # Lettura dei dati
                new = True
                num = 0
                buffer = 0
                filename = ""
                i = 0
                sensorname = ""
                for i in range(len(data)):
                    if new and ((chr(data[i]) >= 'a' and chr(data[i]) <= 'z') or (chr(data[i]) >= 'A' and chr(data[i]) <= 'Z')):
                        sensorname = chr(data[i])
                        filename = "data/data" + str(id) + "_" + str(sensorname) +  ".txt"
                        new = False
                    elif not new and chr(data[i]) != '#':
                        #print(i, data[i], chr(data[i]))
                        num = num | (data[i] << 8*buffer)
                        buffer += 1
                    elif not new and chr(data[i]) == '#':
                        #logging.debug("(THREAD %s) Ricevuto: %s --- Sensore: %s --- Valore: %s", id, data, filename, num)
                        with open(filename, 'w') as d:
                            d.write(str(num))
                            d.close()
                        new = True
                        buffer = 0
                        num = 0
                logging.debug(f"ricevuto {data}")
            time.sleep(refresh)
            #
    except Exception as error:
        logging.fatal(traceback.format_exc())