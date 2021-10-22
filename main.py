import sys
from collections import deque
from termcolor import colored, cprint
import copy

size_of_mapa = 0

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

# funkcia skontroluje ci je predane auto je mozne sa pohnut v pozadovanom smere
def can_go(car, smer, distance_to_go):

    if car.orientation == "hor":

        if smer == "go_right":
            if car.x + car.size + distance_to_go <= size_of_mapa:
                return True
        elif smer == "go_left":
            if car.x - distance_to_go >= 0:
                return True

    if car.orientation == "ver":

        if smer == "go_up":
            if car.y - distance_to_go >= 0:
                return True
        elif smer == "go_down":
            if car.y + car.size + distance_to_go <= size_of_mapa:
                return True

    return False

def can_go_in_map(state, car, distance_to_go, smer):

    for i in range(0, distance_to_go):

        if smer == "go_right":
            if state.my_map[car.y][car.x + car.size + i]:
                return False
        elif smer == "go_left":
            if state.my_map[car.y][car.x - i - 1]:
                return False
        elif smer == "go_up":
            if state.my_map[car.y - i - 1][car.x]:
                return False
        elif smer == "go_down":
            if state.my_map[car.y + car.size + i][car.x]:
                return False

    return True

'''
POHYBOVANIE AUTICOK
'''
#(VPRAVO stav vozidlo počet) - go_right je HOR pohyb na ose X
def go_right(stav, car, distance_to_go):

    if can_go(car, "go_right", distance_to_go):
        if can_go_in_map(stav, car, distance_to_go, "go_right"):
            car.x += distance_to_go
            # print(f"Posunulo sa auto {auticka_dict[car.id]} go_right o {distance_to_go}")
            return True
    # print(f"Nieje mozne posunut {auticka_dict[car_id]} go_right o {distance_to_go}")
    return False

#(VLAVO stav vozidlo počet)
def go_left(stav, car, distance_to_go):

    if can_go(car, "go_left", distance_to_go):
        if can_go_in_map(stav, car, distance_to_go, "go_left"):
            car.x -= distance_to_go
            # print(f"Posunulo sa auto {auticka_dict[car.id]} go_left o {distance_to_go}")
            return True
    # print(f"Nieje mozne posunut {auticka_dict[car_id]} go_left o {distance_to_go}")
    return False

#(DOLE stav vozidlo počet)
def go_down(stav, car, distance_to_go):

    if can_go(car, "go_down", distance_to_go):
        if can_go_in_map(stav, car, distance_to_go, "go_down"):
            car.y += distance_to_go
            # print(f"Posunulo sa auto {auticka_dict[car.id]} go_down o {distance_to_go}")
            return True
    # print(f"Nieje mozne posunut {auticka_dict[car_id]} go_down o {distance_to_go}")
    return False

#(HORE stav vozidlo počet)
def go_up(stav, car, distance_to_go):

    if can_go(car, "go_up", distance_to_go):
        if can_go_in_map(stav, car, distance_to_go, "go_up"):
            car.y -= distance_to_go
            # print(f"Posunulo sa auto {auticka_dict[car.id]} go_up o {distance_to_go}")
            return True
    # print(f"Nieje mozne posunut {auticka_dict[car_id]} go_up o {distance_to_go}")
    return False

'''
MAPA, STAV-uzol, Main()
'''

# funkcia urobi prazdnu mapu
# bud s False hodnotami alebo s 0
def creat_empty_map(prepinac):
        return [[prepinac for x in range(size_of_mapa)] for y in range(size_of_mapa)]

# funkcia urobi mapu pre aktualne auticka
def creat_map(cars):
    temp_map = creat_empty_map(False)
    for car in cars:
        for i in range(car.size):
            if car.orientation == "ver":
                temp_map[car.y + i][car.x] = True
            elif car.orientation == "hor":
                temp_map[car.y][car.x + i] = True
    return temp_map

def print_map(cars):
    temp_map = creat_empty_map(0)
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

class Node:
    # v podstate je to vytvorenie pociatocneho uzla
    def __init__(self, cars):
        # atribúty
        self.depth = 0
        self.cars = cars
        self.my_map = creat_map(cars)
        self.printed_map = None
        self.previous_state = None
        self.co_sa_udialo = "start"
        self.visited = False
        self.susedia = []
        pass

def creat_new_node(old_state, temp_car, depth, step, distance_to_go): # sem este pridat smer ak tak

    state = copy.deepcopy(old_state)

    state.depth = depth
    state.cars[temp_car.id - 1] = temp_car
    state.my_map = creat_map(state.cars)
    state.printed_map = print_map(state.cars)
    state.co_sa_udialo = f"auto {auticka_dict[temp_car.id]} islo {step} o {distance_to_go}"
    state.previous_state = old_state

    # tu sa ked tak moze vypisat mapka
    return state

def test_finish(state, temp_car):
    flag = False
    temp_state = copy.deepcopy(state)
    car = copy.deepcopy(temp_car)

    if car.x + car.size >= size_of_mapa:
        flag = True

    for distance_to_go in range(1, size_of_mapa - 2):
        if go_left(temp_state, car, distance_to_go):
            if car.x + car.size >= size_of_mapa:
                flag = True

    if flag:
        act = state
        while act != None:
            print(act.co_sa_udialo)
            act = act.previous_state
        return True

    return False

pouzite, nepouzite = [], []
def compare_pouzite_cars(cars):
    global pouzite
    if pouzite:
        for car in cars:
            for cars_pouzite in pouzite:
                for car_pouzite in cars_pouzite.cars:
                    if car.id == car_pouzite.id and car.x == car_pouzite.x and car.y == car_pouzite.y:
                        return True
    return False

def dfs(state, depth):
    global pouzite, nepouzite

    # kontrola ciela
    if test_finish(state, state.cars[3]):
        print("\nNaslo sa riesenie!")
        return True

    if depth <= 0:
        return False

    # tento loop vytvára stavy v jednej vrstve
    # Node(self, cars, temp_map, previous_state, step, depth)
    for temp_car in state.cars:
        car = copy.deepcopy(temp_car)

        # najskor posuniem kazde auticko o max krokov
        # pohyb(stav, car_id, distance_to_go)
        for distance_to_go in range(1, size_of_mapa - car.size):

            if car.orientation == "ver":

                if go_up(state, car, distance_to_go):
                    temp_state = creat_new_node(state, car, depth, "go_up", distance_to_go)
                    if not compare_pouzite_cars(temp_state.cars):
                        nepouzite.append(temp_state)

                if go_down(state, car, distance_to_go):
                    temp_state = creat_new_node(state, car, depth, "go_down", distance_to_go)
                    if not compare_pouzite_cars(temp_state.cars):
                        nepouzite.append(temp_state)
            # koniec ver pohybov

            elif car.orientation == "hor":

                if go_right(state, car, distance_to_go):
                    temp_state = creat_new_node(state, car, depth, "do_right", distance_to_go)
                    if not compare_pouzite_cars(temp_state.cars):
                        nepouzite.append(temp_state)

                if go_left(state, car, distance_to_go):
                    temp_state = creat_new_node(state, car, depth, "go_left", distance_to_go)
                    if not compare_pouzite_cars(temp_state.cars):
                        nepouzite.append(temp_state)
            # koniec hor pohybov

    pouzite.append(state)
    if len(nepouzite) > 0:
        state = nepouzite[len(nepouzite) - 1]
        nepouzite.pop()
        term_print(state.cars)
        dfs(state, depth - 1)

    # koniec testovanie vsetkych auticok
    return False

def iterative_deepening_search(max_depht, cars):
    global pouzite, nepouzite
    d = 1
    # vytvorenie prazdnej map
    while d != max_depht:
        print(f"***** Pokus c. {d}, taka je aj max hlbka ***** \n")
        if dfs(Node(cars), d):
            return True
        d += 1
    return False

# Defining main function
def main():

    cars = []
    global size_of_mapa
    with open("vstup.txt", "r") as input_file:

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

    # max_depht = int(input("Zadajte hĺku do akej chcete vyhladavat: "))
    max_depht = 6

    if not iterative_deepening_search(max_depht, cars):
        print("\nRiesenie sa nenaslo")
    pass

if __name__ == "__main__":
    print("PyCharm starting..")
    # sys.stdout = open("file.txt", "w")
    main()
    # end of program
