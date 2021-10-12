import sys
import time
import random

possible_x_moves = [2, 1, -1, -2, -2, -1, 1, 2]
possible_y_moves = [1, 2, 2, 1, -1, -2, -2, -1]
global size

def checkBounds(x, y, size, chessboard):
    if (x >= 0 and y >= 0 and x < size and y < size and chessboard[x][y] == -1):
        return True
    return False


def printChessboard(size, chessboard):
    for i in range(size):
        for j in range(size):
            print(chessboard[i][j], end=' ')
        print()


def randomCoord(size):
    global x_start
    global y_start
    is_random = input("Chceš randomne vygenerovať začiatočnú súradnicu?(y/n): ")
    if is_random == "n":
        print("Zadaj počiatočnú súradnicu x(0-",size-1,"): ",end="")
        x_start = int(input())
        print("Zadaj počiatočnú súradnicu y(0-",size-1,"): ",end="")
        y_start = int(input())
    elif is_random == "y":
        x_start = random.randint(0, size - 1)
        y_start = random.randint(0, size - 1)
        print("Začiatočná súradnica x je: ", x_start)
        print("Začiatočná súradnica y je: ", y_start)
    else:
        print("Nesprávny vstup")
    return x_start, y_start


def solver(size, x, y, timestart, limit):
    chessboard = [[-1 for i in range(size)] for i in range(size)]
    position = 1
    chessboard[y][x] = 0

    if (not solverHelp(size, chessboard, x, y, possible_x_moves, possible_y_moves, position, timestart, limit)):
        print("Pre dané súradnice/limit neexistuje riešenie")
    else:
        printChessboard(size, chessboard)


def solverHelp(size, chessboard, x, y, next_x, next_y, position, timestart, limit):
    cas=time.time()
    if (position == size * size):
        return True
    if (cas-timestart) < limit:
        for i in range(8):
            new_x = x + next_x[i]
            new_y = y + next_y[i]
            if (checkBounds(new_x, new_y, size, chessboard)):
                chessboard[new_x][new_y] = position
                if (solverHelp(size, chessboard, new_x, new_y, next_x, next_y, position + 1, timestart, limit)):
                    return True
                chessboard[new_x][new_y] = -1
    elif(cas-timestart) >= limit:
        print("Vypršal čas na hľadanie, program trval: ",int(cas-timestart), "sekúnd")
        return True
    return False


def main():
    global time_start
    time_start = time.time()
    size = int(input("Zadaj veľkosť: "))
    limit = int(input("Zadaj časový limit hľadania (s): "))
    randomCoord(size)
    solver(size, x_start, y_start, time_start, limit)
