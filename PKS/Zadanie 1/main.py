from scapy.all import *
from binascii import hexlify, unhexlify

file = rdpcap("trace-27.pcap")
encoding = "UTF-8"


def print_packet(packet_data):
    pocet = 0
    for i in packet_data:
        print('{:02X} '.format(i), end='')
        pocet += 1
        if pocet % 16 == 0:
            print("")
            continue
        if pocet % 8 == 0:
            print('  ', end='')


def print_info(file):
    global riadok
    for l in range(0, len(file)):
        riadok = bytes(file[l])
        riadok = hexlify(riadok)
        print("\n\nRámec: " + str(l+1))
        print("Dĺžka rámca poskytnutá pcap API: " + str(len(riadok)/2)[:-2] + "B")
        if len(riadok)/2 + 4 > 64:
            print("Dĺžka rámca prenášaného po médiu: " + str(len(riadok)/2 + 4)[:-2] + "B")
        else:
            print("Dĺžka rámca prenášaného po médiu: 64B")
        riadok = unhexlify(riadok)
        print_mac(riadok)
        ether = extract_data(riadok, 12, 13)
        ieee = extract_data(riadok, 14, 15)
        ether = int(hexlify(ether), 16)
        ieee = int(hexlify(ieee), 16)
        print_type(ether, ieee)
        inside_protocol(riadok, ether, ieee)
        #print_packet(riadok)


def print_type(ether, ieee):
    print("\nTyp rámca: ", end='')
    if ether >= 1536:
        print("Ethernet II")
    elif ieee == 0xFFFF:
        print("IEEE 802.3 raw")
    elif ieee == 0xAAAA:
        print("IEEE 802.3 LLC + SNAP")
    else:
        print("IEEE 802.3 LLC")


def extract_data(packet_data, start, end, integ=False):
    if integ:
        return int(hexlify(packet_data[start:(end + 1)]), 16)
    else:
        return packet_data[start:(end + 1)]


def print_mac(riadok):
    source_mac = extract_data(riadok, 0, 5)
    receive_mac = extract_data(riadok, 6, 11)
    print("Zdrojová MAC adresa: ", end="")
    print_packet(source_mac)
    print("\nCieľová MAC adresa: ", end="")
    print_packet(receive_mac)


def load_from_file(file_name, dictionary):
    for line in open(file_name, "r"):
        processed = line.split(' ', 1)
        dictionary[int(processed[0], 16)] = processed[1].replace("\n", "")


def print_ip(sour_start, sour_end, dest_start, dest_end):
    count = 0
    source = extract_data(riadok, sour_start, sour_end)
    destination = extract_data(riadok, dest_start, dest_end)
    print("Zdrojová IP adresa: ", end='')
    for k in source:
        count += 1
        if count == len(source):
            print(str(k), end='')
        else:
            print(str(k) + ".", end='')


    print("\nCieľová IP adresa: ", end='')
    count2 = 0
    for l in destination:
        count2 += 1
        if count2 == len(destination):
            print(str(l))
        else:
            print(str(l) + ".", end='')


def transport_protocol(help):
    head = (extract_data(help, 14, 14, True) - int(extract_data(help, 14, 14, True) / 16) * 16) * 4
    return help[14 + head:len(help)]


def inside_protocol(riadok, ether, ieee):
    print("Typ vnoreného protokolu: ", end='')
    ether_type = {}
    llc = {}
    ip = {}
    ports = {}
    load_from_file("ether_types.txt", ether_type)
    load_from_file("llc_saps.txt", llc)
    load_from_file("ip_protocols.txt", ip)
    load_from_file("udp_ports.txt", ports)
    ip_header = extract_data(riadok, 23, 23, True)
    help3 = extract_data(riadok, 14, 14, True)
    if ip_header == 17:
        load_from_file("udp_ports.txt", ports)
    elif ip_header == 6:
        load_from_file("tcp_ports.txt", ports)
    elif ip_header == 1:
        icmp = {}
        load_from_file("icmp_types.txt", icmp)

    if ether >= 1500:
        if ether in ether_type:
            print(ether_type.get(ether))
        else:
            print("Neznámy Ethertype")
    if ether == 2054:
        print_ip(28, 31, 38, 41)
        if (extract_data(riadok, 20, 21, True)) == 2:
            print("ARP REPLY")
        else:
            print("ARP REQUEST")
    if ether == 2048:
        print_ip(26, 29, 30, 33)
        if ip_header in ip:
            print(ip.get(ip_header))

        if ip_header == 1:
            print("Správa: ", end="")
            if extract_data(transport_protocol(riadok), 0, 0, True) in icmp:
                print(icmp.get(extract_data(transport_protocol(riadok), 0, 0, True)))

        help = extract_data(transport_protocol(riadok), 0, 1, True)
        help2 = extract_data(transport_protocol(riadok), 2, 3, True)
        if len(ports) != 0:
            print("Zdrojový port: ", end="")
            print(help)
            print("Cieľový port: ", end="")
            print(help2)
        if help in ports:
            print(ports.get(help))
        elif help2 in ports:
            print(ports.get(help2))
        else:
            print("Neznámy port")
    elif help3 in llc:
        print(llc.get(help3))
    elif ieee == 65535:
        print("IPX")


print_info(file)