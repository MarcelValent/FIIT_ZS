import socket
import zlib
import os
import math

def data_packet(crc, sequence, data, file=False):
    if file:
        packet = crc.to_bytes(4, byteorder="big") + sequence.to_bytes(1, byteorder="big") + data
    else:
        packet = crc.to_bytes(4, byteorder="big") + sequence.to_bytes(1, byteorder="big") + data.encode()
    return packet


def decode_data(data_to_decode, file=False):
    crc = int.from_bytes(data_to_decode[0:4], byteorder="big")
    sequence = int.from_bytes(data_to_decode[4:5], byteorder="big")
    if not file:
        data = data_to_decode[5:].decode()
    else:
        data = data_to_decode[5:]
    return crc, sequence, data


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


def printfile(listik):
    out = b""
    for x in range(len(listik)):
        out += listik[x]
    return out


def printdata(listik):
    stringik = ""
    for x in range(len(listik)):
      stringik += listik[x]
    print(stringik)


def startserver():
    fragments = 0
    data = []
    previous_seq_num = 1
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
    if flag == 4:
        file_name = decode_info(received)[2]
        kkt = os.path.basename(str(file_name))
    if flag == 3 or flag == 4:
        while True:
            if fragments == pocet:
                serverSocket.sendto(info_packet(6), messagefrom)
                break
            received, messagefrom = serverSocket.recvfrom(1500)
            if flag == 3:
                crc = decode_data(received)[0]
                seq_num = decode_data(received)[1]
                data_received = decode_data(received)[2]
                crchelp = data_received.encode()
            if flag == 4:
                crc = decode_data(received, True)[0]
                seq_num = decode_data(received, True)[1]
                data_received = decode_data(received, True)[2]
                crchelp = data_received
            if crc == zlib.crc32(crchelp):
                if previous_seq_num != seq_num:
                    data.append(data_received)
                    previous_seq_num = seq_num
                    serverSocket.sendto(info_packet(1), messagefrom)
                    print("Received fragment number: ", fragments+1, "it was correct")
                    fragments += 1
                elif previous_seq_num == seq_num:
                    if data_received not in data:
                        data.append(data_received)
                        serverSocket.sendto(info_packet(1), messagefrom)
                    else:
                        serverSocket.sendto(info_packet(1), messagefrom)
            elif crc != zlib.crc32(crchelp):
                serverSocket.sendto(info_packet(2), messagefrom)
                print("Packet number", fragments+1,"was wrong.")
        if flag == 3:
            print("You received a message: ", end="")
            printdata(data)
        if flag == 4:
            print("Enter path where you want to save: ", end="")
            file = input()
            file += "\\" + kkt
            fileout = open(file, "wb")
            premenna = printfile(data)
            fileout.write(premenna)
            print("SERVER DORUČIL")
    #if flag == 7:



#1- ACK
#2 - NACK
#3 - message
#4 - file
#5 - switch role
#6 - Global ack(uspesny konec prenosu)
#7 - keep alive flag


def startclient():
    print("IP address you want to send to: ", end="")
    ip = input()
    print("Port you want to send to: ", end="")
    port = int(input())
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Enter fragment size (6-1400): ", end="")
    frag = int(input())
    while frag <= 5:
        print("Enter fragment size (6-1400): ", end="")
        frag = int(input())
    print("Do you want to implement fault? (y/n)" )
    fault = input()
    print("Do you want to send 1 fault(1) or faulty every second fragment(2)?")
    option_fault = int(input())
    og = option_fault
    print("Do you want to send message(m) or file(f) ?")
    choice = input()
    if choice == "m":
        i = 0
        counter = -1
        print("Message you want to send: ", end="")
        data = input()
        temp = math.ceil(len(data)/(frag - 5))
        if temp < 0:
            temp = 1
        info = info_packet(3, "", temp)
        clientSocket.sendto(info, (ip, port))
        while i < temp:
            help = data[(frag - 5)*i:(frag - 5)*(i+1)]
            if i % 2 == 1:
                check = 1
            else:
                check = 0
                if counter != i and og == 2:
                    option_fault = 2
            crc = zlib.crc32(help.encode())
            if option_fault == 2:
                if fault == "y" and counter != i and check == 0:
                    counter = i
                    option_fault = -1
                    broken = help[:-1]
                    x = data_packet(crc, check, broken)
            elif option_fault == 1:
                if fault == "y" and i == 0 and counter != i:
                    counter = i
                    option_fault = -1
                    broken = help[:-1]
                    x = data_packet(crc, check, broken)
            else:
                x = data_packet(crc, check, help)
            clientSocket.sendto(x, (ip, port))
            print("Sending packet number: ", i+1)
            bytesPair, messagefrom = clientSocket.recvfrom(1500)
            if decode_info(bytesPair) == 1:
                print("Packet successfully sent.")
                i += 1
            elif decode_info(bytesPair) == 2:
                print("Packet number", i+1, "was not sent right")
            else:
                print("No reply from server, terminating communication")
                return -1
        bytesPair, messagefrom = clientSocket.recvfrom(1500)
        if decode_info(bytesPair) == 6:
            print("Message successfully sent.")
                #keep_alive(ip, port)






    if choice == "f":
        print("Input path to file you want to send: ", end="")
        data = input()
        f = open(data, "rb")
        file = f.read()
        filesize = os.path.getsize(data)
        print("Enter fragment size (6-1400): ", end="")
        while frag <= 5:
            print("Enter fragment size (6-1400): ", end="")
            frag = int(input())
        i = 0
        counter = -1
        temp = math.ceil(filesize / (frag - 5))
        if temp < 0:
            temp = 1
        info = info_packet(4, data, temp)
        clientSocket.sendto(info, (ip, port))
        while i < temp:
            help = file[(frag - 5) * i:(frag - 5) * (i + 1)]
            if i % 2 == 1:
                check = 1
            else:
                check = 0
                if counter != i and og == 2:
                    option_fault = 2
            crc = zlib.crc32(help)
            if option_fault == 2:
                if fault == "y" and counter != i and check == 0:
                    counter = i
                    option_fault = -1
                    broken = help[:-1]
                    x = data_packet(crc, check, broken, True)
            elif option_fault == 1:
                if fault == "y" and i == 0 and counter != i:
                    counter = i
                    option_fault = -1
                    broken = help[:-1]
                    x = data_packet(crc, check, broken, True)
            else:
                x = data_packet(crc, check, help, True)
            clientSocket.sendto(x, (ip, port))
            print("Sending packet number: ", i + 1)
            bytesPair, messagefrom = clientSocket.recvfrom(1500)
            if decode_info(bytesPair) == 1:
                print("Packet successfully sent.")
                i += 1
            elif decode_info(bytesPair) == 2:
                print("Packet number", i + 1, "was not sent right")
            else:
                print("No reply from server, terminating communication")
                return -1
        bytesPair, messagefrom = clientSocket.recvfrom(1500)
        if decode_info(bytesPair) == 6:
            print("Message successfully sent.")
            # keep_alive(ip, port)





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