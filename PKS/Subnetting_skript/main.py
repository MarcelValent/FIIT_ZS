import sys


def calculate_subnet(net, size, order,r1, router=False):
    powers = [2 ** j for j in range(1,33)]
    #nemenit
    a = net.partition(".")[0]
    b = net.partition(".")[2].partition(".")[0]
    #predposledne
    x = net.partition(".")[2].partition(".")[2].partition(".")[0]
    #posledne
    y = net.partition(".")[2].partition(".")[2].partition(".")[2].partition("/")[0]
    #lomeno
    z = net.partition(".")[2].partition(".")[2].partition(".")[2].partition("/")[2]
    for i in range(len(powers)):
        if size <= powers[i]:
            power = powers[i]
            break
    subnetid = 31 - i
    if subnetid < int(z):
        print("Príliš veľká sieť.")
        return -1
    else:
        z = subnetid
    k = int(power / 256)
    x = int(x)
    if size >=256:
        y = 0
    else:
        y = int(y)
    print("Adresa siete: ",int(a),".",int(b),".",int(x),".",int(y),"/",int(z))
    if size >=256:
        print("Adresa broadcast: ", int(a), ".", int(b), ".", int(x+k-1), ".", "255", "/", int(z))
        netlist = [str(a), ".", str(b), ".", str(x+k), ".", str(int(0)), "/", str(z)]
    else:
        netlist = [str(a), ".", str(b), ".", str(x + k), ".", str(int(y+power)), "/", str(z)]
    net = "".join(netlist)
    if size < 256:
        print("Adresa broadcast: ", int(a), ".", int(b), ".", int(x), ".", int(y+power)-1, "/", int(z))
    if order >= 256:
        help = int(order / 256)
        x = int(x) + help
        y = order % 256
    else:
        y = (int(y)+order)
    if not router:
        print("Adresa PC: ",int(a),".",int(b),".",int(x),".",int(y),"/",int(z))

    if router:
        if r1 == 1:
            print("Adresa prvého routra: ", int(a), ".", int(b), ".", int(x), ".", int(y+1), "/", int(z))
            print("Adresa druhého routra: ", int(a), ".", int(b), ".", int(x), ".", int(y+2), "/", int(z))
        else:
            print("Adresa prvého routra: ", int(a), ".", int(b), ".", int(x), ".", int(y+2), "/", int(z))
            print("Adresa druhého routra: ", int(a), ".", int(b), ".", int(x), ".", int(y+1), "/", int(z))

    if z == 30:
        print("Maska: 255.255.255.252")
    if z == 29:
        print("Maska: 255.255.255.248")
    if z == 28:
        print("Maska: 255.255.255.240")
    if z == 27:
        print("Maska: 255.255.255.224")
    if z == 26:
        print("Maska: 255.255.255.192")
    if z == 25:
        print("Maska: 255.255.255.128")
    if z == 24:
        print("Maska: 255.255.255.0")
    if z == 23:
        print("Maska: 255.255.254.0")
    if z == 22:
        print("Maska: 255.255.252.0")
    if z == 21:
        print("Maska: 255.255.248.0")
    if z == 20:
        print("Maska: 255.255.240.0")
    if z == 19:
        print("Maska: 255.255.224.0")
    if z == 18:
        print("Maska: 255.255.192.0")
    if z == 16:
        print("Maska: 255.255.128.0")
    if z == 15:
        print("Maska: 255.255.0.0")
    if z == 14:
        print("Maska: 255.254.0.0")
    if z == 13:
        print("Maska: 255.252.0.0")
    if z == 12:
        print("Maska: 255.248.0.0")

    return net


def main():
    print("ZADAVAJ OD NAJVACSEJ SIETE PO NAJMENSIU, POSLEDNA SIET JE PRE ROUTRE")
    print("swedenko praje prijemny test zo subnettingu")
    povodna_siet = input("Zadaj povodnu sieť: ")
    siet1 = int(input("Zadaj velkosť siete 1:"))+3
    id1 = int(input("Zadaj poradie tejto siete:"))
    siet2 = int(input("Zadaj velkosť siete 2: "))+3
    id2 =int(input("Zadaj poradie tejto siete:"))
    siet3 = int(input("Zadaj velkosť siete 3: "))+3
    id3 = int(input("Zadaj poradie tejto siete:"))
    siet4 = int(input("Zadaj velkosť siete 4: "))+3
    id4 =int(input("Zadaj poradie tejto siete:"))
    siet5 = int(input("Zadaj velkosť siete 5 :"))+2
    pc1 = int(input("Zadaj poradie PC1: "))
    pc2 = int(input("Zadaj poradie PC2: "))
    pc3 = int(input("Zadaj poradie PC3: "))
    pc4 = int(input("Zadaj poradie PC4: "))
    first = int(input("Zadaj poradie routra 1: "))
    f = open(input("Zadaj output file: "), 'w')
    sys.stdout = f
    print("Povodna siet: ", povodna_siet)
    print("------------------------Sieť",id1,"--------------------------")
    print("Velkost siete: ", siet1)
    print("Poradie PC: ", pc1)
    povodna_siet = calculate_subnet(povodna_siet, siet1, pc1, 1, False)
    print("------------------------Sieť",id2,"--------------------------")
    print("Velkost siete: ", siet2)
    print("Poradie PC: ", pc2)
    povodna_siet = calculate_subnet(povodna_siet, siet2, pc2, 1, False)
    print("------------------------Sieť",id3,"--------------------------")
    print("Velkost siete: ", siet3)
    print("Poradie PC: ", pc3)
    povodna_siet = calculate_subnet(povodna_siet, siet3, pc3, 1, False)
    print("------------------------Sieť",id4,"--------------------------")
    print("Velkost siete: ", siet4)
    print("Poradie PC: ", pc4)
    povodna_siet = calculate_subnet(povodna_siet, siet4, pc4, 1, False)
    print("------------------------Sieť 5--------------------------")
    print("Velkost siete: ", siet5)
    calculate_subnet(povodna_siet, siet5, 0, first, True)
    f.close()


main()
