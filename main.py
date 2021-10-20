
from collections import deque
import copy

size_of_mapa = 0

auticka_dict = {
    1: "orange",
    2: "yellow",
    3: "purple",
    4: "red",
    5: "turquoise",
    6: "green",
    7: "gray",
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
            if car.x + car.size + distance_to_go < size_of_mapa:
                return True
        elif smer == "go_left":
            if car.x - distance_to_go >= 0:
                return True
        else:
            return False

    if car.orientation == "ver":

        if smer == "go_up":
            if car.y - distance_to_go >= 0:
                return True
        elif smer == "go_down":
            if car.y + car.size + distance_to_go < size_of_mapa:
                return True
        else:
            return False

    pass

def can_go_in_map(map, x, y, distance_to_go, smer):

    for i in range(1, distance_to_go):

        if smer == "go_right":
            if map[y][x + i]:
                return False
        elif smer == "go_left":
            if map[y][x - i]:
                return False
        elif smer == "go_up":
            if map[y + i][x]:
                return False
        elif smer == "go_down":
            if map[y - i][x]:
                return False

    return True

'''
POHYBOVANIE AUTICOK
'''
#(VPRAVO stav vozidlo počet) - go_right je HOR pohyb na ose X
def go_right(stav, car_id, distance_to_go):
    car = stav.cars[car_id - 1]

    if can_go(car, "go_right", distance_to_go):
        if can_go_in_map(stav.my_map, car.x + distance_to_go, car.y, distance_to_go, "go_right"):
            car.x += distance_to_go
            print(f"Posunulo sa auto {auticka_dict[car_id]} go_right o {distance_to_go}")
            return True

    print(f"Nieje mozne posunut {auticka_dict[car_id]} go_right o {distance_to_go}")
    return False

#(VLAVO stav vozidlo počet)
def go_left(stav, car_id, distance_to_go):
    car = stav.cars[car_id - 1]

    if can_go(car, "go_left", distance_to_go):
        if can_go_in_map(stav.my_map, car.x - distance_to_go, car.y, distance_to_go, "go_left"):
            car.x -= distance_to_go
            print(f"Posunulo sa auto {auticka_dict[car_id]} go_left o {distance_to_go}")
            return True

    print(f"Nieje mozne posunut {auticka_dict[car_id]} go_left o {distance_to_go}")
    return False

#(DOLE stav vozidlo počet)
def go_down(stav, car_id, distance_to_go):
    car = stav.cars[car_id - 1]

    if can_go(car, "go_down", distance_to_go):
        if can_go_in_map(stav.my_map, car.x, car.y + distance_to_go, distance_to_go, "go_down"):
            car.y += distance_to_go
            print(f"Posunulo sa auto {auticka_dict[car_id]} go_down o {distance_to_go}")
            return True

    print(f"Nieje mozne posunut {auticka_dict[car_id]} go_down o {distance_to_go}")
    return False

#(HORE stav vozidlo počet)
def go_up(stav, car_id, distance_to_go):
    car = stav.cars[car_id - 1]

    if can_go(car, "go_up", distance_to_go):
        if can_go_in_map(stav.my_map, car.x, car.y - distance_to_go, distance_to_go, go_up):
            car.y -= distance_to_go
            print(f"Posunulo sa auto {auticka_dict[car_id]} go_up o {distance_to_go}")
            return True

    print(f"Nieje mozne posunut {auticka_dict[car_id]} go_up o {distance_to_go}")
    return False

'''
MAPA, STAV-uzol, Main()
'''

# funkcia urobi prazdnu mapu
def creat_empty_map():
    return [[False for x in range(size_of_mapa)] for y in range(size_of_mapa)]

# funkcia urobi mapu pre aktualne auticka
def creat_map(cars):
    temp_map = creat_empty_map()
    for car in cars:

        for i in range(car.size):
            if car.orientation == "ver":
                temp_map[car.y + i][car.x] = True
            elif car.orientation == "hor":
                temp_map[car.y][car.x + i] = True

    return temp_map

class Node:
    # v podstate je to vytvorenie pociatocneho uzla
    global size_of_mapa

    def __init__(self, cars, temp_map, previous_state, step, depth):
        temp_map = creat_map(cars)
        # atribúty
        self.cars = cars
        self.my_map = temp_map
        self.previous_state = previous_state
        self.step_from_previous_state = step
        self.distance_of_previous_step = None
        self.depth = depth
        pass

def creat_new_node(old_state, temp_car, d_stack, depth, co_ma_dostalo_do_tohto_stavu, distance_to_go):

    state = copy.deepcopy(old_state)

    state.cars[temp_car.id - 1] = temp_car
    state.my_map = creat_map(state.cars)
    state.step_from_previous_state = co_ma_dostalo_do_tohto_stavu
    state.distance_of_previous_step = distance_to_go
    state.depth = depth

    d_stack.append(state)


def test_finish(car):
    if car.x == size_of_mapa - 1:
        return True
    else:
        return False

def dfs(cars, max_depth):

    root = Node(cars, creat_empty_map(), None, None, 0)
    d_stack = deque()
    d_stack.append(root)

    while len(d_stack) != 0:

        state = d_stack.pop()

        state.depth += 1
        depth = state.depth
        if state.depth > max_depth:
            return False

        # tento loop vytvára stavy v jednej vrstve
        # Node(self, cars, temp_map, previous_state, step, depth)
        for car in state.cars:

            # najskor posuniem kazde auticko o max krokov
            # pohyb(stav, car_id, distance_to_go)
            for distance_to_go in range(size_of_mapa - car.size, 1, -1):

                if car.orientation == "ver":

                    if can_go(car, "go_up", distance_to_go):
                        if go_up(state, car.id, distance_to_go) and state.step_from_previous_state != "go_down":
                            co_ma_dostalo_do_tohto_stavu = "go_up"
                            creat_new_node(state, car, d_stack, depth, co_ma_dostalo_do_tohto_stavu, distance_to_go)
                            break

                    elif can_go(car, "go_down", distance_to_go):
                        if go_down(state, car.id, distance_to_go) and state.step_from_previous_state != "go_up":
                            co_ma_dostalo_do_tohto_stavu = "go_down"
                            creat_new_node(state, car, d_stack, depth, co_ma_dostalo_do_tohto_stavu, distance_to_go)
                            break
                    pass # koniec ver pohybov

                elif car.orientation == "hor":

                    if can_go(car, "go_left", distance_to_go):
                        if go_left(state, car.id, distance_to_go) and state.step_from_previous_state != "go_right":
                            co_ma_dostalo_do_tohto_stavu = "go_left"
                            creat_new_node(state, car, d_stack, depth, co_ma_dostalo_do_tohto_stavu, distance_to_go)
                            break

                    elif can_go(car, "go_right", distance_to_go):
                        if go_right(state, car.id, distance_to_go) and state.step_from_previous_state != "go_left":
                            co_ma_dostalo_do_tohto_stavu = "go_right"
                            creat_new_node(state, car, d_stack, depth, co_ma_dostalo_do_tohto_stavu, distance_to_go)
                            break
                    pass # koniec hor pohybov

                pass  # ukoncenie loopu na posuvanie auticka

            # kontrola ciela
            if auticka_dict[car.id] == "red":
                if test_finish(car):
                    print("\nNaslo sa riesenie!")
                    return True

            pass  # testovanie vsetkych auticok

def iterative_deepening_search(max_depht, cars):
    d = 1
    # vytvorenie prazdnej map
    while d != max_depht:
        print(f"\n***** Pokus c. {d} ***** \n")
        if dfs(copy.deepcopy(cars), d):
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

    # print(cars)
    # max_depht = int(input("Zadajte hĺku do akej chcete vyhladavat: "))
    max_depht = 5

    if not iterative_deepening_search(max_depht, cars):
        print("\nRiesenie sa nenaslo")
    pass

if __name__ == "__main__":
    print("PyCharm starting..")
    main()
    # end of program
