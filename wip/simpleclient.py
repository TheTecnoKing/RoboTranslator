import bluetooth
import threading
import re

def sendData():
    while True:
        data = input("Send: ")
        sock.send(data)

def receiveData():
    while True:
        data: bytes = sock.recv(4096)
        #data_format = re.sub('1?..', lambda m: chr(int(m.group())), data.decode("ascii"))
        print("Received: " +  str(data[0]), "Bytes: " + str(data), "Dim:" + str(len(data)), sep=" | ")

        # dividiamo i dati
        # nome del sensore
        print("\nSensor name: " + str(chr(data[0])))
        # dato numerico
        num = data[1] | (data[2] << 8) | (data[3] << 16) | (data[4] << 24)
        print("Num: " + str(num))
        print("*********************")

address = "00:21:09:01:26:ED"
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((address, port))

print("Connected. Type something...")

# com = threading.Thread(target=receiveData)
# com.start()

receiveData()