import sys
from termcolor import colored, cprint
import copy
import time

# globalne premenne vyuzivane napriec programom
size_of_mapa = 0
d_stack = []
sum_of_state = 0
t1, t0 = 0, 0

auticka_dict = {
    1: "white",
    2: "yellow",
    3: "magenta",
    4: "red",
    5: "cyan",
    6: "green",
    7: "grey",
    8: "blue",
}

class Car:
    # constructor
    def __init__(self, id, size, x, y, orientation):
        # colour
        self.id = id
        # ako je dlhe, min je dva aby malo orientáciu
        self.size = size
        self.x = int(x)
        self.y = int(y)
        # ver (vertikalne) -> |
        # hor (horizontalne) -> -
        self.orientation = orientation

    # porovnavanie objetkov podla: https://www.pythontutorial.net/python-oop/python-__eq__/
    def __eq__(self, other):
        if isinstance(other, Car):
            return self.x == other.x and self.y == other.y and self.orientation == other.orientation

class State:
    def __init__(self, crossroad, cars, depth, parent):
        self.crossroad = crossroad
        self.cars = cars
        self.depth = depth
        self.note = ""
        self.parent = parent

    # porovnavanie objetkov podla: https://www.pythontutorial.net/python-oop/python-__eq__/
    def __eq__(self, other):
        if isinstance(other, State):
            return self.cars == other.cars

'''
POHYBOVANIE AUTICOK
'''
def go_right(state, id):
    car = state.cars[id - 1]
    if car.size == 2:
        state.crossroad[car.y][car.x] = False
        state.crossroad[car.y][car.x + 2] = True
    elif car.size == 3:
        state.crossroad[car.y][car.x] = False
        state.crossroad[car.y][car.x + 3] = True
    car.x += 1
def go_left(state, id):
    car = state.cars[id - 1]
    if car.size == 2:
        state.crossroad[car.y][car.x + 1] = False
        state.crossroad[car.y][car.x - 1] = True
    elif car.size == 3:
        state.crossroad[car.y][car.x + 2] = False
        state.crossroad[car.y][car.x - 1] = True
    car.x -= 1
def go_down(state, id):
    car = state.cars[id - 1]
    if car.size == 2:
        state.crossroad[car.y][car.x] = False
        state.crossroad[car.y + 2][car.x] = True
    elif car.size == 3:
        state.crossroad[car.y][car.x] = False
        state.crossroad[car.y + 3][car.x] = True
    car.y += 1
def go_up(state, id):
    car = state.cars[id - 1]
    if car.size == 2:
        state.crossroad[car.y + 1][car.x] = False
        state.crossroad[car.y - 1][car.x] = True
    elif car.size == 3:
        state.crossroad[car.y + 2][car.x] = False
        state.crossroad[car.y - 1][car.x] = True
    car.y -= 1

# vykreslovanie mapky farebne
def print_map(cars):
    temp_map = [[0 for x in range(size_of_mapa)] for y in range(size_of_mapa)]
    for car in cars:
        for i in range(car.size):
            if car.orientation == "ver":
                temp_map[car.y + i][car.x] = car.id
            elif car.orientation == "hor":
                temp_map[car.y][car.x + i] = car.id
    return temp_map
def term_print(cars):
    points = print_map(cars)
    for riadok in range(len(points)):
        for stlpec in range(len(points[riadok])):
            if points[riadok][stlpec] == 0:
                print("*", end=" ")
            else:
                cprint(points[riadok][stlpec], auticka_dict[points[riadok][stlpec]], end=" ")
                # print(points[riadok][stlpec], end=" ")
        print()
    print("----------------------")

# kolko je mozne posunut dane auto vzhladom na mapu prislusneho stavu
def max_of_car_step(car, crossroad, smer):
    steps = 0

    if smer == "go_right":
        while car.x + car.size + steps < size_of_mapa:
            if crossroad[car.y][car.x + car.size + steps]:
                return steps + 1
            steps += 1
    elif smer == "go_left":
        while car.x - steps - 1 >= 0:
            if crossroad[car.y][car.x - steps - 1]:
                return steps + 1
            steps += 1
    elif smer == "go_down":
        while car.y + car.size + steps < size_of_mapa:
            if crossroad[car.y + car.size + steps][car.x]:
                return steps + 1
            steps += 1
    elif smer == "go_up":
        while car.y - steps - 1 >= 0:
            if crossroad[car.y - steps - 1][car.x]:
                return steps + 1
            steps += 1

    return steps + 1

# vypis krokov pomocou prechadzania stavou od cieloveho k pociatocnemu
def printf_result(state):
    global t1
    act = state
    mess = []
    # prechadzaj stavy od cieloveho k zaciatocnemu
    while act != None:
        mess.append(act.note)
        act = act.parent
    # vypisovanie stavou z listu zozadu aby sedelo poradie
    for j in range(len(mess) - 1, -1, -1):
        print(mess[j])
    # farebny vypisok finalnej mapky
    term_print(state.cars)
    # vypis casu trvania progrmau
    t1 = time.time()
    x = t1 - t0
    print("sum_of_state: ", sum_of_state)
    print("Cas: %.2fs" % x)
    exit()

# otestuje ci moze cerveno auticko vyjst z krizovatky
def test_finish(state):
    global i
    car_red = state.cars[3]

    # test volnosti policok smerov vpravo od cerveneho auticka
    flag_skor = 0
    for i in range(car_red.x + car_red.size, size_of_mapa):
        if state.crossroad[car_red.y][i]:
            flag_skor = 2
            break
        else:
            flag_skor = 1
    # ak cervene auticko moze ist vpravo a vyjst z krizovatky
    # tak zapis tento krok k doterajsim krokom
    if flag_skor == 1:
        state.note += f"\n Last: auticko({auticka_dict[car_red.id]} {car_red.id}) go_right o {size_of_mapa - car_red.x - car_red.size}"
        printf_result(state)
        return True

    # este jedna podmienka pre kontrolu ciela
    if car_red.x + car_red.size >= size_of_mapa:
        printf_result(state)
        return True
    return False

# funkcia na posun auticok
def move_objs(state, id, visited, depth, smer):
    global d_stack
    global sum_of_state
    steps = max_of_car_step(state.cars[id - 1], state.crossroad, smer)
    # vytvorenie noveho stavu
    temp_state = copy.deepcopy(state)
    sum_of_state += 1
    temp_state.parent = state
    temp_state.depth += 1

    # ak je stav nad povolenu hlbku tak koniec
    if temp_state.depth > depth:
        return False

    # vytvaraj stavy pre dane kroky
    for step in range(1, steps):
        temp_state = copy.deepcopy(temp_state)
        sum_of_state += 1

        if smer == "go_right":
            go_right(temp_state, id)

        elif smer == "go_left":
            go_left(temp_state, id)

        elif smer == "go_down":
            go_down(temp_state, id)

        elif smer == "go_up":
            go_up(temp_state, id)

        # zapis kroku v danom stave do daneho stavu
        temp_state.note = f"auticko({auticka_dict[id]} {id}) {smer} o {step}"

        # ak uz stav bol navstiveny
        if temp_state in visited:
            i = visited.index(temp_state)
            # ak je novy stav navstiveny ale je lepsi (ma mensiu hlbku)
            if temp_state == visited[i] and temp_state.depth < visited[i].depth:
                # tak sa stavy vymenia
                d_stack.append(temp_state)
                visited.remove(visited[i])
                visited.append(temp_state)
                break
        # ak nebol navstiveny zaradi sa do zasobniku na spracovanie
        else:
            d_stack.append(temp_state)

        # otestovanie cielu pre dany stav
        if test_finish(state):
            return True
    return False

def dfs(state, depth):
    global d_stack
    visited = []

    while 1 != 0:

        if len(d_stack) == 0:
            return False
        state = d_stack.pop()
        visited.append(state)
        if state.depth > depth:
            continue

        # riešenie daného stavu
        for car in state.cars:

            if car.orientation == "hor":
                if move_objs(state, car.id, visited, depth, "go_right") or move_objs(state, car.id, visited, depth, "go_left"):
                    return True
            elif car.orientation == "ver":
                move_objs(state, car.id, visited, depth, "go_down")
                move_objs(state, car.id, visited, depth, "go_up")

    return False

def root_state(max_depht, cars):
    # vytvor prazdnu mapu, 2d pole vsade False
    crossroad = [[False for x in range(size_of_mapa)] for y in range(size_of_mapa)]

    # vyznacenie policov na kt. stoja auticka
    for car in cars:
        for i in range(car.size):
            if car.orientation == "ver":
                crossroad[car.y + i][car.x] = True
            elif car.orientation == "hor":
                crossroad[car.y][car.x + i] = True

    # vytvor root state
    root_state = State(crossroad, cars, 0, None)
    return root_state

# postupne sa zvysuje hlbka az do maxima
# pre danu hlbku sa zavola DFS
def iterative_deepening_search(max_depht, cars):
    global t0
    t0 = time.time()
    global d_stack
    flag = False
    d = 0

    # vypis pociatocneho stavu (farebna mapka)
    term_print(cars)
    # postupne zvysovanie hlbky
    while d != max_depht:
        print(f"***** Pokus c. {d} *****")
        state = root_state(max_depht, cars)
        d_stack.append(state)
        if dfs(state, d):
            flag = True
            break
        d += 1

    return flag

# Defining main function
def main():

    cars = []
    global size_of_mapa
    # vstup aky subor sa pouzije
    vstup = int(input("1. vstup.txt\n2. vstup_origo.txt\n3. vstup_2.txt\n4. vstup_3.txt\n5. vstup_4.txt\n6. vstup_5.txt\n7. vstup_6.txt\nVyberte vstup: "))

    if vstup == 1:
        file = "vstup.txt"
    if vstup == 2:
        file = "vstup_origo.txt"
    if vstup == 3:
        file = "vstup_2.txt"
    if vstup == 4:
        file = "vstup_3.txt"
    if vstup == 5:
        file = "vstup_4.txt"
    if vstup == 6:
        file = "vstup_5.txt"
    if vstup == 7:
        file = "vstup_6.txt"

    # nacitanie zvoleneho suboru so vstupmi
    with open(file, "r") as input_file:

        # nacitanie a vytvorenie objektov auticka v liste cars podla vstupneho suboru
        while True:
            line = input_file.readline()

            if line.startswith("*"):
                size_of_mapa = int(line.split(" ", 1)[1][:-1])
            elif line.startswith("#"):
                continue
            elif not line:
                input_file.close()
                del(input_file, line, id, size, x, y, orientation)
                break
            else:
                id, size, x, y, orientation = line.split(",", 4)
                cars.append(Car(int(id), int(size), int(x), int(y), orientation[:-1]))

    max_depht = int(input("Zadajte hĺku do akej chcete vyhladavat: "))
    # max_depht = 20

    # ak neni riesenie
    if not iterative_deepening_search(max_depht, cars):
        print("\nRiesenie sa nenaslo alebo neexistuje")
    pass

if __name__ == "__main__":
    print("PyCharm starting..")
    # sys.stdout = open("file.txt", "w")
    main()
    print("sum_of_state: ", sum_of_state)
    # end of program
