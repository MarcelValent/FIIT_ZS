import socket
import zlib
import os
import math


def data_packet(crc, data):
    packet = crc.to_bytes(4, byteorder="big") + data.encode()
    return packet


def decode_data(data_to_decode):
    crc = int.from_bytes(data_to_decode[0:4], byteorder="big")
    data = data_to_decode[4:].decode()
    return crc, data


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


def keep_alive(socket, port, ip):
    while True:
        socket.sendto(info_packet(7), (ip, port))
        socket.settimeout(10)


def printdata(listik):
    stringik = ""
    for x in range(len(listik)):
      stringik += listik[x]
    print(stringik)

def startserver():
    fragments = 0
    data = []
    print("Port you want to listen on: ", end="")
    port = int(input())
    localIP = socket.gethostbyname(socket.gethostname())
    print(localIP)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((localIP, port))
    received, messagefrom = serverSocket.recvfrom(1500)
    print("Connected from", messagefrom[0])
    flag = decode_info(received)[0]
    pocet = decode_info(received)[1]
    if flag == 3:
        while fragments < pocet:
            received, messagefrom = serverSocket.recvfrom(1500)
            if decode_data(received)[0] == zlib.crc32(decode_data(received)[1].encode()):
                data.append(decode_data(received)[1])
                serverSocket.sendto(info_packet(1), messagefrom)
                fragments += 1
            else:
                serverSocket.sendto(info_packet(2), messagefrom)
        print("You received a message: ", end="")
        serverSocket.sendto(info_packet(6), messagefrom)
        printdata(data)
    #if flag == 4:

    #if flag == 7:



#1- ACK
#2 - NACK
#3 - message
#4 - file
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
        temp = math.ceil(len(data)/(frag - 4))
        if temp == 0:
            temp = 1
        info = info_packet(3, "", temp)
        clientSocket.sendto(info, (ip, port))
        for i in range(temp):
            help = data[(frag - 4)*i:(frag - 4)*(i+1)]
            crc = zlib.crc32(help.encode())
            x = data_packet(crc, help)
            clientSocket.sendto(x, (ip, port))
            bytesPair, messagefrom = clientSocket.recvfrom(1500)
            if decode_info(bytesPair) == 1:
                print("Packet successfully sent.")
            elif decode_info(bytesPair) == 2:
                print("Packet number", i+1, "was not sent right")
                while decode_info(bytesPair) != 1:
                    clientSocket.sendto(x, (ip, port))
                    bytesPair, messagefrom = clientSocket.recvfrom(1500)

        bytesPair, messagefrom = clientSocket.recvfrom(1500)
        if decode_info(bytesPair) == 6:
            print("Message successfully sent.")
                #keep_alive(ip, port)
    if choice == "f":
        print("Input path to file you want to send: ", end="")
        data = input()
        print("How do you want to save the file on other PC?: ", end="")
        filename = input()
        f = open(data, "rb")
        filesize = os.path.getsize(data)
        tmp = math.ceil(len(data)/(frag - 4))
        x = info_packet(4, filename, tmp)
        clientSocket.sendto(x, (ip, port))
        for i in range(tmp):
            help = f.read(frag).decode()
            if not help:
                break
            crc = zlib.crc32(help.encode())
            x = data_packet(crc, help)
            clientSocket.sendto(x, (ip, port))
            bytesPair, messagefrom = clientSocket.recvfrom(1500)
            if decode_info(bytesPair) == 1:
                print("Packet successfully sent.")
            elif decode_info(bytesPair) == 2:
                print("Packet number", i+1, "was not sent right")
                while decode_info(bytesPair) != 1:
                    clientSocket.sendto(x, (ip, port))
                    bytesPair, messagefrom = clientSocket.recvfrom(1500)
            elif decode_info(bytesPair) == 6:
                print("File was successfully sent.")
                #keep_alive(ip, port)


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