import copy
import random


class Garden:
    def __init__(self, rows, columns):
        self.garden = []
        self.row = []
        for x in range(rows+1):
            self.row = []
            for y in range(columns):
                self.row.append(0)
            self.garden.append(self.row)
        self.row.clear()
        self.garden.remove(self.garden[rows])
        self.row = rows
        self.column = columns
        self.size = rows*columns


class Monk:
    def __init__(self, garden, moves):
        self.garden = garden
        self.moves = moves
        self.fitness = 0


def calculate_fitness(zahrada):
    tmp = 0
    for x in range(zahrada.row):
        for y in range(zahrada.column):
            if zahrada.garden[x][y] != 0 and zahrada.garden[x][y] != "K":
                tmp += 1
    return tmp


def print_garden(garden):
    for i in garden:
        for j in i:
            print("{0: >2}".format(j), end=' ')
        print()
    print()


def generate_start(x, y):
    global start_sur
    start_sur = []
    for l in range(x):
        start_sur.append([l, 0, "r"])
    for k in range(y):
        start_sur.append([0, k, "d"])
    for m in range(x):
        start_sur.append([m, y-1, "l"])
    for n in range(y):
        start_sur.append([x-1, n, "u"])
    return start_sur


def randomKamen(number,  zahrada):
    for x in range(zahrada.row):
        for i in range(zahrada.column):
            z = random.random()
            if z < number:
                zahrada.garden[x][i] = "K"


def zadajKamen(zahrada, listik):
    for i in range(len(listik)):
        zahrada.garden[listik[i][0]][listik[i][1]] = "K"


def rake_help(zahrada, sur, number):
    x = sur[0]
    y = sur[1]
    if zahrada.garden[x][y] == 0:
        zahrada.garden[x][y] = number
        direction = sur[2]
    else:
        return 1
    while True:
        if direction == "d":
            if x + 1 < zahrada.row:
                if zahrada.garden[x + 1][y] == 0:
                    zahrada.garden[x + 1][y] = number
                    x += 1
                else:
                    direction = check(x, y, zahrada, direction)
                    if direction == False:
                        return -1
            else:
                return 0
        elif direction == "u":
            if x - 1 >= 0:
                if zahrada.garden[x - 1][y] == 0:
                    zahrada.garden[x - 1][y] = number
                    x -= 1
                else:
                    direction = check(x, y, zahrada, direction)
                    if direction == False:
                        return -1
            else:
                return 0
        elif direction == "r":
            if y + 1 < zahrada.column:
                if zahrada.garden[x][y + 1] == 0:
                    zahrada.garden[x][y + 1] = number
                    y += 1
                else:
                    direction = check(x, y, zahrada, direction)
                    if direction == False:
                        return -1
            else:
                return 0
        elif direction == "l":
            if y - 1 >= 0:
                if zahrada.garden[x][y - 1] == 0:
                    zahrada.garden[x][y - 1] = number
                    y -= 1
                else:
                    direction = check(x, y, zahrada, direction)
                    if direction == False:
                        return -1
            else:
                return 0


def check(x, y, garden, direction):
    moznosti = []
    if direction == "l" or direction == "r":
        if x + 1 < garden.row:
            if garden.garden[x + 1][y] == 0:
                moznosti.append("d")
        else:
            moznosti.append("d")
        if x - 1 >= 0:
            if garden.garden[x - 1][y] == 0:
                moznosti.append("u")
        else:
            moznosti.append("u")
    else:
        if y + 1 < garden.column:
            if garden.garden[x][y + 1] == 0:
                moznosti.append("r")
        else:
            moznosti.append("r")
        if y - 1 >= 0:
            if garden.garden[x][y - 1] == 0:
                moznosti.append("l")
        else:
            moznosti.append("l")
    if len(moznosti) == 0:
        return False
    else:
        return random.choice(moznosti)


def rake(zahrada, sur):
    number = 1
    for x in range(len(sur)):
        help = rake_help(zahrada, sur[x], number)
        if help == -1:
            for i in range(len(zahrada.garden)):
                for j in range(len(zahrada.garden[i])):
                    if zahrada.garden[i][j] == number:
                        zahrada.garden[i][j] = 0
            return -1
        elif help == 0:
            number += 1
    return 2


def monastery(monk, garden, fitness):
    generations = 1000
    monks = 100
    tabu = []
    tabusize = 50
    head_monk = monk
    for x in range(generations):
        if x != 0:
            monk = copy.deepcopy(best_monk)
        best_monk = None
        for y in range(monks):
            garden_help = copy.deepcopy(garden)
            index1 = random.randint(0, len(monk.moves) - 1)
            index2 = random.randint(0, len(monk.moves) - 1)
            while index1 == index2:
                index1 = random.randint(0, len(monk.moves) - 1)
            moves = copy.deepcopy(monk.moves)
            moves[index1], moves[index2] = moves[index2], moves[index1]
            monk_curr = Monk(garden_help, moves)
            rake(garden_help, monk_curr.moves)
            monk_curr.fitness = calculate_fitness(garden_help)
            if y == 0:
                best_monk = monk_curr
            if monk_curr.fitness > best_monk.fitness and monk_curr.moves not in tabu:
                best_monk = monk_curr
        if best_monk.fitness > head_monk.fitness:
            head_monk = best_monk
        tabu.append(best_monk.moves)
        if len(tabu) > tabusize:
            tabu.pop(0)
        if best_monk.fitness == fitness:
            print_garden(best_monk.garden.garden)
            print("Monks to find this solution: ", x * y)
            print("Best monk raked: ", best_monk.fitness)
            exit()
    print_garden(head_monk.garden.garden)
    print("Monks to find this solution: ", x * monks)
    print("Best monk raked: ", head_monk.fitness)


def main():
    x = int(input("Zadaj počet riadkov záhrady: "))
    y = int(input("Zadaj počet stĺpcov záhrady: "))
    zahrada = Garden(x, y)
    listik = [[1, 5], [2, 1], [3, 4], [4, 2], [6, 8], [6, 9]]
    randomKamen(0.05, zahrada)
    best_fitness = 0
    for o in range(zahrada.row):
        for p in range(zahrada.column):
            if zahrada.garden[o][p] == 0:
                best_fitness += 1
    zahrada1 = copy.deepcopy(zahrada)
    monk = Monk(zahrada1, generate_start(x, y))
    rake(zahrada1, monk.moves)
    monk.fitness = calculate_fitness(zahrada1)
    if monk.fitness == best_fitness:
        print_garden(monk.garden.garden)
        print("Monks to find this solution: 1")
        print("Best monk raked: ", monk.fitness)
    else:
        monastery(monk, zahrada, best_fitness)

main()