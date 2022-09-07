'''import bluetooth
import logging

def receiveData(sock, id):
    data: bytes = sock.recv(4096)
    num = data[1] | (data[2] << 8) | (data[3] << 16) | (data[4] << 24)
    logging.debug("(THREAD %s) Ricevuto: %s --- Sensore: %s --- Valore: %s", id, data, chr(data[0]), num)
    return [data[0], num]

def connect(id, address, device_name):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((address, port))
    logging.info("(THREAD %s) Dispositivo connesso! %s - %s", id, device_name, address)

    while True:
        data = receiveData(sock, id)
        filename = "data/data" + str(id) + "_" + str(chr(data[0])) +  ".txt"
        with open(filename, 'w') as d:
            d.write(str(data[1]))
            d.close()
'''

import bluetooth
import logging
import traceback
import time
import random

'''
def receiveData(sock, id):
    # data: bytes = sock.recv(4096)
    num = data[1] | (data[2] << 8) | (data[3] << 16) | (data[4] << 24)
    logging.debug("(THREAD %s) Ricevuto: %s --- Sensore: %s --- Valore: %s", id, data, chr(data[0]), num)
    return [data[0], num]
'''
def connect(id, address, device_name):
    try:
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((address, port))
        logging.info("(THREAD %s) Dispositivo connesso! %s - %s", id, device_name, address)

        while True:
            data: bytes = sock.recv(4096)

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
            '''sock.send(bytes('a', 'ascii'))         
            print(bin(ord('a')))'''
            with open("data/input" + str(id) + ".txt", 'r') as d:
                #read = d.read()
                read = "a1234#"
                if read:
                    for i in range(len(read)):
                        sock.send(read[i])
                        sock.send(read[i])
                        #print(ord(read[i]))
                        print(ord(read[i]), bin(ord(read[i])))
                        time.sleep(0.025)
                    d.close()
                    with open("data/input" + str(id) + ".txt", 'w') as dw:
                        dw.close()
            '''for i in range(6):
                sock.send(bytes('a1578#', 'ascii'))
                time.sleep(0.05)'''

    except Exception as error:
        logging.fatal(traceback.format_exc())