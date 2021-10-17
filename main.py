
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
def can_go(car, smer):

    if car.orientation == "hor":
        if smer == "go_right" or smer == "go_left":
            return True
        else:
            return False

    if car.orientation == "ver":
        if smer == "go_up" or smer == "go_down":
            return True
        else:
            return False

    pass

'''
POHYBOVANIE AUTICOK
'''
#(VPRAVO stav vozidlo počet) - go_right je HOR pohyb na ose X
def go_right(stav, car_id, distance_to_go):
    car = stav.this_car(car_id)

    if can_go(car, "hor"):
        if car.x + distance_to_go < size_of_mapa:
            car.x += distance_to_go
            return True

    print(f"Nieje mozne posunut {car_id} go_right o {distance_to_go}")
    return False

#(VLAVO stav vozidlo počet)
def go_left(stav, car_id, distance_to_go):
    car = stav.this_car(car_id)

    if can_go(car, "hor"):
        if car.x - distance_to_go >= 0:
            car.x -= distance_to_go
            return True

    print(f"Nieje mozne posunut {car_id} go_left o {distance_to_go}")
    return False

#(DOLE stav vozidlo počet)
def go_down(stav, car_id, distance_to_go):
    car = stav.this_car(car_id)

    if can_go(car, "ver"):
        if car.x + distance_to_go < size_of_mapa:
            car.x += distance_to_go
            return True

    print(f"Nieje mozne posunut {car_id} go_down o {distance_to_go}")
    return False

#(HORE stav vozidlo počet)
def go_up(stav, car_id, distance_to_go):
    car = stav.this_car(car_id)

    if can_go(car, "hor"):
        if car.x - distance_to_go >= 0:
            car.x -= distance_to_go
            return True

    print(f"Nieje mozne posunut {car_id} go_up o {distance_to_go}")
    return False

'''
MAPA, STAV-uzol, Main()
'''
# funkcia urobi mapu pre aktualne auticka
def creat_map(cars, temp_map):
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

    def __init__(self, cars, temp_map, previous_state, step):
        temp_map = creat_map(cars, temp_map)
        # atribúty
        self.cars = cars
        self.my_map = temp_map
        self.previous_state = previous_state
        self.step_from_previous_state = step
        pass

def iterative_deepening_search(max_depht, cars):

    d = 0

    # vytvorenie prazdnej map
    my_map = [[False for x in range(size_of_mapa)] for y in range(size_of_mapa)]

    root = Node(cars, my_map)
    d_stack = deque()
    d_stack.appendleft(root)
    temp_state = root
    while d != max_depht:

        if len(d_stack) == 0:
            return False

        new_temp_state = copy.deepcopy(temp_state)

        for car in temp_state.cars:

            # najskor posuniem kazde auticko o max krokov
            # pohyb(stav, car_id, distance_to_go)
            for distance_to_go in range(size_of_mapa - car.size):

                if car.orientation == "ver":
                    if can_go(car, "go_up"):
                        temp_car = copy.deepcopy(car)
                        if go_up(new_temp_state, temp_car.id, distance_to_go):
                            new_temp_state.car = temp_car
                            d_stack.appendleft(copy.deepcopy(new_temp_state))
                        else:
                            del(temp_car)
                    elif can_go(car, "go_down"):
                        temp_car = copy.deepcopy(car)

                        if go_down(new_temp_state, temp_car.id, distance_to_go):
                            new_temp_state.car = temp_car
                            d_stack.appendleft(copy.deepcopy(new_temp_state))
                        else:
                            del(temp_car)
                    pass

                elif car.orientation == "hor":
                    if can_go(car, "go_left"):
                        temp_car = copy.deepcopy(car)
                        if go_up(new_temp_state, temp_car.id, distance_to_go):
                            new_temp_state.car = temp_car
                            d_stack.appendleft(copy.deepcopy(new_temp_state))
                        else:
                            del (temp_car)
                    elif can_go(car, "go_right"):
                        temp_car = copy.deepcopy(car)
                        if go_down(new_temp_state, temp_car.id, distance_to_go):
                            new_temp_state.car = temp_car
                            d_stack.appendleft(copy.deepcopy(new_temp_state))
                        else:
                            del (temp_car)
                    pass

                pass
            pass
        d += 1
        pass

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
    max_depht = int(input("Zadajte hĺku do akej chcete vyhladavat: "))

    if not iterative_deepening_search(max_depht, cars):
        print("Riesenie sa nenaslo")
    pass

if __name__ == "__main__":
    print("PyCharm starting..")
    main()
    # end of program
