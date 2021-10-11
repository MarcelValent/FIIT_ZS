import random
import time

X = [1,  1, 2,  2, -1, -1, -2, -2]
Y = [2, -2, 1, -1,  2, -2,  1, -1]



def makeboard(velkost):
    if 7 < velkost < 6:
        print("Zadaj inú veľkosť.")
    else:
        board = {1: {'susedia': [], 'navstiveny': '', 'poradie': '', 'tatko': ''}}

        for i in range(1, velkost+1):
            for l in range(1, velkost+1):
                if i == 1:
                    k = l
                else:
                    k = (((i-1)*velkost)+l)
                board[k] = {}
                board[k]['navstiveny'] = False
                board[k]['poradie'] = 0
                xpohyb = createmoves(velkost, l, i)
                board[k]['susedia'] = xpohyb

    return board


def solver(chessboard, size, visited, timelimit, stvorcek):
    if visited == size*size:
        return True
    chessboard[stvorcek]['navstiveny'] = True
    chessboard[stvorcek]['poradie'] = visited
    sused = chessboard[stvorcek]['susedia']
    for l in range(len(sused)):
        x = random.choice(sused)
        #x = sused [l]
        if isvisited(chessboard, x) == False:
            chessboard[x]['navstiveny'] = True
            chessboard[x]['poradie'] = visited
            chessboard[x]['tatko'] = chessboard[stvorcek]['poradie']
            if solver(chessboard, size, visited + 1, timelimit, x) == False:
                break

    return False


def isvisited(chessboard, num):
    if chessboard[num]['navstiveny'] == True:
        return True
    else:
        return False


def printsachovnica(chessboard, size):

    for y in range(1,size+1):
        print()
        for x in range(1,size+1):
            cislo = ((size*size) - (y * size) + x)
            print(chessboard[cislo]['poradie'], end="   ")


def createmoves(velkost, x, y):
    dalsimore = []
    for l in range(8):
        next1 = y + Y[l]
        next2 = x + X[l]
        dalsi = surnacislo(next2, next1, velkost)
        if next2 > velkost or next1 > velkost:
            continue
        if dalsi > 0 and dalsi <= velkost*velkost:
            dalsimore.append(dalsi)
    #dalsimore.sort(reverse=True)
    #dalsimore.sort()
    return dalsimore


def randomsuradnice(velkost):
    global xzac
    global yzac
    je_random = int(input("Chceš randomne vygenerovať začiatočnú súradnicu?(0/1): "))
    if je_random == 0:
        xzac = int(input("Zadaj počiatočnú súradnicu x: "))
        yzac = int(input("Zadaj počiatočnú súradnicu y: "))
    elif je_random == 1:
        xzac = random.randint(1, velkost)
        yzac = random.randint(1, velkost)
        print("Začiatočná súradnica x je: ", xzac)
        print("Začiatočná súradnica y je: ", yzac)
    else:
        print("Nesprávny vstup")
    return xzac, yzac


def surnacislo(xsur, ysur, velkost):
    if xsur <= 0 or ysur <= 0:
        return 0
    if ysur == 1:
        cislo = xsur
    else:
        cislo = ((ysur-1) * velkost) + xsur
    return cislo


def main():
    global cas
    cas = int(time.time())
    velkost = int(input("Zadaj veľkosť: "))
    limit = int(input("Zadaj časový limit hľadania (s): "))
    randomsuradnice(velkost)
    while ((time.time()-cas) < limit):
        sachovnica = makeboard(velkost)
        solver(sachovnica, velkost, 1, limit, surnacislo(xzac, yzac, velkost))
        if solver(sachovnica, velkost, 1, limit, surnacislo(xzac, yzac, velkost)) == True:
            printsachovnica(sachovnica, velkost)
        elif (time.time()-cas) > limit:
            print("Cesta sa nenašla.\n")
            printsachovnica(sachovnica, velkost)
    print("\n\nProgram trval ", int(time.time()-cas), "sekúnd.")


main()
