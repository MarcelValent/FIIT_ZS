import random


class Garden:
    def __init__(self, rows, columns):
        self.garden = []
        self.row = []
        for x in range(rows+1):
            self.row = []
            for y in range(columns):
                z = random.random()
                if z < 0.05:
                    self.row.append("K")
                else:
                    self.row.append(0)
            self.garden.append(self.row)
        self.row.clear()
        self.garden.remove(self.garden[rows])
        self.raked = 0
        self.row = rows
        self.column = columns
        self.size = rows*columns
        self.rocks = sum(row.count("K") for row in self.garden)


def move_up(garden, x, y, actually=False):
    if actually:
        tempx = x - 1
        tempy = y
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0 :
            return tempx, tempy
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "K" and tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "0":
            return 1
        else: return False
    else:
        tempx = x - 1
        tempy = y
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return True
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        else: return False


def move_down(garden, x, y, actually=False):
    if actually:
        tempx = x + 1
        tempy = y
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
           return tempx, tempy
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "K" and tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "0":
            return 1
        else:
            return False
    else:
        tempx = x+1
        tempy = y
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return True
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        else: return False


def move_left(garden, x, y, actually=False):
    if actually:
        tempx = x
        tempy = y - 1
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return tempx, tempy
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "K" and tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "0":
            return 1
        else:
            return False
    else:
        tempx = x
        tempy = y-1
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return True
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        else: return False


def move_right(garden, x, y, actually=False):
    if actually:
        tempx = x
        tempy = y + 1
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return tempx,tempy
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "K" and tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] != "0":
            return 1
        else:
            return False
    else:
        tempx = x
        tempy = y+1
        if tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == 0:
            return True
        elif tempx > -1 and tempy > -1 and tempx < garden.row and tempy < garden.column and garden.garden[tempx][tempy] == "K":
            return "Kamen"
        else: return False


def print_garden(garden):
    for i in garden:
        for j in i:
            print("{0: >2}".format(j), end=' ')
        print()
    print()


def generate_start(x, y):
    global start_sur
    start_sur = [[]]
    for l in range(x):
        if [l, 0] not in start_sur:
            start_sur.append([l, 0])
    for k in range (y):
        if [0, k] not in start_sur:
            start_sur.append([0, k])
    for m in range(x):
        if [m, y-1] not in start_sur:
            start_sur.append([m, y-1])
    for n in range (y):
        if [x-1, n] not in start_sur:
            start_sur.append([x-1, n])
    del start_sur[0]
    return start_sur


def rake(garden, sur):
    number = 1
    for k in range(99):
        x = len(sur)-1
        x = random.randint(0, x)
        start_monk = sur[x]
        z = random.randint(0, 1)
        if garden.garden[start_monk[0]][start_monk[1]] != 0:
            sur.remove(sur[x])
            continue
        elif start_monk[1] == (garden.row - 1) and start_monk[0] == 0:
            if z == 0:
                move = move_down(garden, start_monk[0], start_monk[1])
                direction = "d"
                if move == True:
                    move = move_down(garden, start_monk[0], start_monk[1], True)
            elif z == 1:
                move = move_left(garden, start_monk[0], start_monk[1])
                direction = "l"
                if move == True:
                    move = move_left(garden, start_monk[0], start_monk[1], True)
        elif start_monk[1] == (garden.row - 1) and start_monk[0] == (garden.row - 1):
            if z == 0:
                move = move_up(garden, start_monk[0], start_monk[1])
                direction = "u"
                if move == True:
                    move = move_up(garden, start_monk[0], start_monk[1], True)
            if z == 1:
                move = move_left(garden, start_monk[0], start_monk[1])
                direction = "l"
                if move == True:
                    move = move_left(garden, start_monk[0], start_monk[1], True)
        elif start_monk[0] == 0 and start_monk[1] == 0:
            if z == 0:
                move = move_down(garden, start_monk[0], start_monk[1])
                direction = "d"
                if move == True:
                    move = move_down(garden, start_monk[0], start_monk[1], True)
            if z == 1:
                move = move_right(garden, start_monk[0], start_monk[1])
                direction = "r"
                if move == True:
                    move = move_right(garden, start_monk[0], start_monk[1], True)
        elif start_monk[0] == (garden.row - 1) and start_monk[1] == 0:
            if z == 0:
                move = move_up(garden, start_monk[0], start_monk[1])
                direction = "u"
                if move == True:
                    move = move_up(garden, start_monk[0], start_monk[1], True)
            if z == 1:
                move = move_right(garden, start_monk[0], start_monk[1])
                direction = "r"
                if move == True:
                    move = move_right(garden, start_monk[0], start_monk[1], True)
        elif start_monk[0] == 0:
            direction = "d"
            move = move_down(garden, start_monk[0], start_monk[1], True)
        elif start_monk[1] == garden.row - 1:
            direction = "l"
            move = move_left(garden, start_monk[0], start_monk[1], True)
        elif start_monk[0] == garden.row - 1:
            direction = "u"
            move = move_up(garden, start_monk[0], start_monk[1], True)
        elif start_monk[1] == 0:
            direction = "r"
            move = move_right(garden, start_monk[0], start_monk[1], True)



        if move == "Kamen":
            continue
        if move == 1:
            continue

        garden.garden[start_monk[0]][start_monk[1]] = number
        while move != False:
            temp = move
            if move != "Kamen"and move!= 1 and move != False:
                garden.garden[move[0]][move[1]] = number
                temp = move
            if direction == "r":
                move = move_right(garden,move[0], move[1], True)
                if move != False and move != "Kamen"and move!= 1:
                    garden.garden[move[0]][move[1]] = number
                    temp = move
                elif move == "Kamen":
                    if move_up(garden,temp[0], temp[1]):
                        move = move_up(garden, temp[0], temp[1], True)
                        garden.garden[move[0]][move[1]] = number
                        temp = move
                        direction = "u"
                    elif move_down(garden,temp[0], temp[1]):
                        move = move_down(garden, temp[0], temp[1], True)
                        garden.garden[move[0]][move[1]] = number
                        temp = move
                        direction = "d"
                elif move == 1:
                    if z == 1:
                        if move_up(garden, temp[0], temp[1], True) != 1 and move_up(garden, temp[0], temp[1], True) != "Kamen"  and move_up(garden, temp[0], temp[1], True) != False:
                            move =move_up(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "u"
                        else:
                            move = move_down(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "d"
                    elif z == 0:
                        if move_down(garden, temp[0], temp[1], True) != 1 and move_down(garden, temp[0], temp[1], True) != "Kamen" and move_down(garden, temp[0], temp[1], True) != False:
                            move = move_down(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "d"
                        else:
                            move = move_up(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "u"
                    else:
                        return 0




            if direction == "l":
                move = move_left(garden,move[0], move[1], True)
                if move != False and move != "Kamen"and move!= 1:
                    garden.garden[move[0]][move[1]] = number
                    temp = move
                elif move == "Kamen":
                    if move_up(garden,temp[0], temp[1]):
                        move = move_up(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "u"
                    elif move_down(garden,temp[0], temp[1]):
                        move = move_down(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "d"
                elif move == 1:
                    if z == 1:
                        if move_up(garden, temp[0], temp[1], True) != 1 and move_up(garden, temp[0], temp[1],
                                                                                   True) != "Kamen" and move_up(garden, temp[0], temp[1], True) != False:
                            move = move_up(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "u"
                        else:
                            move = move_down(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "d"
                    elif z == 0:
                        if move_down(garden, temp[0], temp[1], True) != 1 and move_down(garden, temp[0], temp[1],
                                                                                       True) != "Kamen"and move_down(garden, temp[0], temp[1], True) != False:
                            move = move_down(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "d"
                        else:
                            move = move_up(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "u"
                    else:
                        return 0






            if direction == "u":
                move = move_up(garden,move[0], move[1], True)
                if move != False and move != "Kamen"and move!= 1:
                    garden.garden[move[0]][move[1]] = number
                    temp = move
                elif move == "Kamen":
                    if move_left(garden,temp[0], temp[1]):
                        move = move_left(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "l"
                    elif move_right(garden,temp[0], temp[1]):
                        move = move_right(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "r"
                elif move == 1:
                    if z == 1:
                        if move_right(garden, temp[0], temp[1], True) != 1 and move_right(garden, temp[0], temp[1],
                                                                                         True) != "Kamen" and move_right(garden, temp[0], temp[1], True) != False:
                            move = move_right(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "r"
                        else:
                            move = move_left(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "l"
                    elif z == 0:
                        if move_left(garden, temp[0], temp[1], True) != 1 and move_left(garden, temp[0], temp[1],
                                                                                       True) != "Kamen" and move_left(garden, temp[0], temp[1], True) != False:
                            move = move_left(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "l"
                        else:
                            move = move_right(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "r"
                    else:
                        return 0







            if direction == "d":
                move = move_down(garden,move[0], move[1], True)
                if move != False and move != "Kamen" and move!= 1:
                    garden.garden[move[0]][move[1]] = number
                    temp = move
                elif move == "Kamen":
                    if move_left(garden, temp[0], temp[1]):
                        move = move_left(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "l"
                    elif move_right(garden, temp[0], temp[1]):
                        move = move_right(garden, temp[0], temp[1], True)
                        if move == 1 or move == False or move == "Kamen":
                            print("A SI DOHRABAL KAMARADE")
                        else:
                            garden.garden[move[0]][move[1]] = number
                            temp = move
                            direction = "r"
                elif move == 1:
                    if z == 1:
                        if move_right(garden, temp[0], temp[1], True) != 1 and move_right(garden, temp[0], temp[1],
                                                                                         True) != "Kamen" and move_right(garden, temp[0], temp[1], True) != False:
                            move = move_right(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "r"
                        else:
                            move = move_left(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "l"
                    elif z == 0:
                        if move_left(garden, temp[0], temp[1], True) != 1 and move_left(garden, temp[0], temp[1],
                                                                                       True) != "Kamen" and move_left(garden, temp[0], temp[1], True) != False:
                            move = move_left(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "l"
                        else:
                            move = move_right(garden, temp[0], temp[1], True)
                            if move == 1 or move == False or move == "Kamen":
                                print("A SI DOHRABAL KAMARADE")
                            else:
                                garden.garden[move[0]][move[1]] = number
                                temp = move
                                direction = "r"
                    else:
                        return 0
            if (move == 1 or move == "Kamen") and (temp[0] != 0 or temp[0] != garden.column -1 or temp[1] != 0 or temp != garden.row -1):
                if move_right(garden,temp[0],temp[1]) == True:
                    move = move_right(garden,temp[0],temp[1], True)
                    direction = "r"
                if move_down(garden,temp[0],temp[1]) == True:
                    move = move_down(garden,temp[0],temp[1], True)
                    direction = "d"
                if move_up(garden,temp[0],temp[1]) == True:
                    move = move_up(garden,temp[0],temp[1], True)
                    direction = "u"
                if move_left(garden,temp[0],temp[1]) == True:
                    move = move_left(garden,temp[0],temp[1], True)
                    direction = "l"
                garden.raked = (garden.size - sum(row.count(0) for row in garden.garden) - garden.rocks)
                print("Stihol som pohrabat ", garden.raked, " štrku predtym jak som siel na pivko")
                return 0
            else:
                continue
        number += 1
        sur.remove(sur[x])
    garden.raked = (garden.size - sum(row.count(0) for row in garden.garden) - garden.rocks)
    print("Stihol som pohrabat ", garden.raked, " štrku predtym jak som siel na pivko")


def main():
    x = int(input("Zadaj počet riadkov záhrady: "))
    y = int(input("Zadaj počet stĺpcov záhrady: "))
    zahrada = Garden(x, y)
    print_garden(zahrada.garden)
    rake(zahrada, generate_start(x, y))
    print_garden(zahrada.garden)


main()
