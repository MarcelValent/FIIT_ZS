import socket
import threading
import zlib
import os


def data_packet(num, crc, data):
    packet = num.to_bytes(3, byteorder="big") + crc.to_bytes(4, byteorder="big") + data.encode()
    return packet


def decode_data(data_to_decode):
    number = int.from_bytes(data_to_decode[:3], byteorder="big")
    crc = int.from_bytes(data_to_decode[3:7], byteorder="big")
    data = data_to_decode[7:].decode()
    return number, crc, data


def info_packet(type, file="", numofpackets=0):
    if numofpackets != 0 and file == "":
        packet = type.to_bytes(1, byteorder="big") + numofpackets.to_bytes(3, byteorder="big")
        return packet
    elif numofpackets == 0 and file == "":
        packet = type.to_bytes(1, byteorder="big")
        return packet
    else:
        packet = type.to_bytes(1, byteorder="big") + numofpackets.to_bytes(3, byteorder="big") + file.encode()
        return packet


def decode_info(data_to_decode):
    if len(data_to_decode) == 1:
        type = int.from_bytes(data_to_decode[:1], byteorder="big")
        return type
    elif len(data_to_decode) == 4:
        type = int.from_bytes(data_to_decode[:1], byteorder="big")
        numofpackets = int.from_bytes(data_to_decode[1:4], byteorder="big")
        return type, numofpackets
    elif len(data_to_decode) > 3:
        type = int.from_bytes(data_to_decode[:1], byteorder="big")
        numofpackets = int.from_bytes(data_to_decode[1:4], byteorder="big")
        data = data_to_decode[4:].decode()
        return type, numofpackets, data


def keep_alive(dstsocket, port):

    while True:
        dstsocket.sendto(info_packet(7), port)
        try:
            dstsocket.settimeout(5)
        finally:
            return -1


def listen_to_wrong(client, dataToSend):
    while True:
        bytePair = client.recvfrom(1500)
        data = bytePair[0].decode()
        tmp, number_of_packet = decode_info(data)
        if tmp == 5:
            dataToSend.append(number_of_packet)
        elif tmp == 1:
            return dataToSend


def startserver():
    print("Port you want to listen on: ", end="")
    port = int(input())
    localIP = socket.gethostbyname(socket.gethostname())
    print(localIP)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((localIP, port))


#0 - zacatie kom.
#1- ACK (server->client)
#2 - NACK (server->client)
#3 - message
#4 - file
#5 - request na dodanie chybajucich fragmentov
#6 - Global ack(uspesny konec vsetkeho)
#7 - keep alive flag


def startclient():
    print("IP address you want to send to: ", end="")
    ip = input()
    print("Port you want to send to: ", end="")
    port = int(input())
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Enter fragment size: ", end="")
    frag = int(input())
    print("Do you want to send message(m) or file(f) ?")
    choice = input()
    if choice == "m":
        print("Message you want to send: ", end="")
        data = input()
        temp = int(len(data)/(frag - 7))
        info = info_packet(3, "", temp)
        if info == 0:
            info = 1
        clientSocket.sendto(info, (ip, port))
        dataToSend = []
        for i in range(temp):
            help = data[(frag - 7)*i:(frag - 7)*(i+1)]
            crc = zlib.crc32(help.encode())
            x = data_packet((i+1), crc, help)
            dataToSend.append(x)
            clientSocket.sendto(x, (ip, port))
        bytesPair = clientSocket.recvfrom(1500)
        message = decode_info(bytesPair[0].decode())
        messageFrom = bytesPair[1].decode()
        if message == 6:
            print("Message was successfully sent to : ", messageFrom)
        if message == 2:
            tempToSend = []
            print("Server is requesting additional data.")
            clientSocket.sendto(info_packet(1), (ip, port))
            thread1 = threading.Thread(target=listen_to_wrong(clientSocket, tempToSend))
            thread1.start()
            thread1.join()
            for k in range(len(tempToSend)):
                x = dataToSend[k]
                clientSocket.sendto(x, (ip, port))
            bytesPair = clientSocket.recvfrom(1500)
            message = decode_info(bytesPair[0].decode())
            messageFrom = bytesPair[1].decode()
            if message == 6:
                print("Sent all missing/faulty packets back to server at : ", messageFrom)
    if choice == "f":
        print("Input path to file you want to send: ", end="")
        data = input()
        f = open(data, "rb")
        filesize = os.path.getsize(data)
        tmp = int(len(data)/(frag - 7))
        x = info_packet(4, data, tmp)
        clientSocket.sendto(x, (ip, port))
        dataForSend = []
        for x in range(filesize):
            bytes_read = f.read(frag).decode()
            if not bytes_read:
                break
            crc = zlib.crc32(bytes_read.encode())
            packet = data_packet(x+1, crc, bytes_read)
            clientSocket.sendto(packet, (ip, port))
            dataForSend.append(packet)
        bytesPair = clientSocket.recvfrom(1500)
        message = decode_info(bytesPair[0].decode())
        messageFrom = bytesPair[1].decode()
        if message == 6:
            print("Message was successfully sent to : ", messageFrom)
        if message == 2:
            tempToSend = []
            print("Server is requesting additional data.")
            clientSocket.sendto(info_packet(1), (ip, port))
            thread2 = threading.Thread(target=listen_to_wrong(clientSocket, tempToSend))
            thread2.start()
            thread2.join()
            for k in range(len(tempToSend)):
                x = dataForSend[k]
                clientSocket.sendto(x, (ip, port))
            bytesPair = clientSocket.recvfrom(1500)
            message = decode_info(bytesPair[0].decode())
            messageFrom = bytesPair[1].decode()
            if message == 6:
                print("Sent all missing/faulty packets back to server at : ", messageFrom)

def main():
    print("For role server type \"server\"")
    print("For role client type \"client\"")
    print("To close the programme type \"quit\"")
    role = input()
    if role == "server":
        startserver()
        print("If you want to change role type \"change\"")
        c = input()
        if c == "change":
            main()
        else:
            startserver()
    elif role == "client":
        startclient()
        print("If you want to change role type \"change\"")
        c = input()
        if c == "change":
            main()
        else:
            startclient()
    elif role == "quit":
        return 0

main()