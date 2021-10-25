import time
import random
global size
steps = 0
#definovanie moznych pohybov kona
possible_x_moves = [2, 1, -1, -2, -2, -1, 1, 2]
possible_y_moves = [1, 2, 2, 1, -1, -2, -2, -1]

#funkcia na skontrolovanie, ci policko je volne a je v rozmeroch sachovnice
def checkBounds(x, y, size, chessboard):
    if x >= 0 and y >= 0 and x < size and y < size and chessboard[x][y] == -1:
        return True
    return False

#funkcia sluziaca na print sachovnice po dokonceni cesty kona
def printChessboard(size, chessboard):
    for i in range(size):
        for j in range(size):
            print(chessboard[i][j], end=' ')
        print()

#funkcia na generovanie alebo zadávanie súradníc
def randomCoord(size):
    global x_start
    global y_start
    is_random = input("Chceš randomne vygenerovať začiatočnú súradnicu?(y/n): ")
    if is_random == "n":
        print("Zadaj počiatočnú súradnicu x(0-", size-1, "): ", end="")
        x_start = int(input())
        print("Zadaj počiatočnú súradnicu y(0-", size-1, "): ", end="")
        y_start = int(input())
    elif is_random == "y":
        x_start = random.randint(0, size - 1)
        y_start = random.randint(0, size - 1)
        print("Začiatočná súradnica x je: ", x_start)
        print("Začiatočná súradnica y je: ", y_start)
    else:
        print("Nesprávny vstup")
    return x_start, y_start

#funkcia na generovanie sachovnice + print udajov do konzole
def solver(size, x, y, timestart, limit):
    position = 1
    #vygenerovanie šachovnice
    chessboard = [[-1 for a in range(size)] for a in range(size)]
    #nastavenie zaciatocneho policka na 0
    chessboard[y][x] = 0
    #pokial sa nenajde cesta do zadanych limitov, alebo po vycerpani vsetkych krokov
    if solverHelp(size, chessboard, x, y, possible_x_moves, possible_y_moves, position, timestart, limit) == False:
        print("Pre dané súradnice/limit neexistuje riešenie")
    else:
        printChessboard(size, chessboard)
        print("Počet krokov: " + str(steps))

#funkcia na  prehladavanie s backtrackingom
def solverHelp(size, chessboard, x, y, next_x, next_y, position, timestart, limit):
    global steps
    cas=time.time()
    #ked sme na poslednom policku tak sa naslo riesenie
    if position == size * size:
        return True
    #kontrola podmienok casu a krokov
    if (cas-timestart) < limit and steps <= 10000000:
        #for cyklus na prehladavanie
        for i in range(8):
            new_x = x + next_x[i]
            new_y = y + next_y[i]
            #ked je volna dana pozicia a je v sachovnici tak sa presunie kon na nu
            if checkBounds(new_x, new_y, size, chessboard) == True:
                chessboard[new_x][new_y] = position
                steps += 1
                #ked je z noveho policka mozny krok tak sa tam presunieme, inak backtracking
                if solverHelp(size, chessboard, new_x, new_y, next_x, next_y, position + 1, timestart, limit) == True:
                    return True
                chessboard[new_x][new_y] = -1
    #ked vyprsi cas
    elif(cas-timestart) >= limit:
        print("Vypršal čas na hľadanie, program trval: ", int(cas-timestart), "sekúnd")
        return True
    return False

#main kde volam funkcie
def main():
    global time_start
    time_start = time.time()
    size = int(input("Zadaj veľkosť: "))
    limit = int(input("Zadaj časový limit hľadania (s): "))
    randomCoord(size)
    solver(size, x_start, y_start, time_start, limit)


main()
