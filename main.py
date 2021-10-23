import sys
from termcolor import colored, cprint
import copy
import time

size_of_mapa = 0
d_stack = []

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

def max_of_car_step(car, crossroad, smer):
    steps = 0

    if smer == "go_right":
        while car.x + car.size + steps < size_of_mapa:
            if crossroad[car.y][car.x + car.size + steps]:
                break
            steps += 1

    elif smer == "go_left":
        while car.x - steps - 1 >= 0:
            if crossroad[car.y][car.x - steps - 1]:
                break
            steps += 1

    elif smer == "go_down":
        while car.y + car.size + steps < size_of_mapa:
            if crossroad[car.y + car.size + steps][car.x]:
                break
            steps += 1

    elif smer == "go_up":
        while car.y - steps - 1 >= 0:
            if crossroad[car.y - steps - 1][car.x]:
                break
            steps += 1

    return steps

def test_finish(state):
    car_red = state.cars[3]
    if car_red.x + car_red.size >= size_of_mapa:
        act = state
        mess = []
        while act != None:
            mess.append(act.note)
            act = act.parent
        for i in range(len(mess) - 1, -1, -1):
            print(mess[i])
        return True
    return False

def move_objs(state, id, visited, depth, smer):
    global d_stack

    steps = max_of_car_step(state.cars[id - 1], state.crossroad, smer)
    temp_state = copy.deepcopy(state)
    temp_state.parent = state
    temp_state.depth += 1

    if temp_state.depth > depth:
        return 0

    for step in range(1, steps + 1):
        temp_state = copy.deepcopy(temp_state)

        if smer == "go_right":
            go_right(temp_state, id)

        elif smer == "go_left":
            go_left(temp_state, id)

        elif smer == "go_down":
            go_down(temp_state, id)

        elif smer == "go_up":
            go_up(temp_state, id)

        temp_state.note = f"auticko({auticka_dict[id]} {id}) {smer} o {step}"

        if temp_state in visited:
            index = visited.index(temp_state)
            if temp_state == visited[index] and temp_state.depth < visited[index].depth:
                d_stack.append(temp_state)
                visited.remove(visited[index])
                visited.append(temp_state)
                break
        else:
            d_stack.append(temp_state)

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

        for car in state.cars:

            if car.orientation == "hor":
                if move_objs(state, car.id, visited, depth, "go_right"):
                    term_print(state.cars)
                    return True
                move_objs(state, car.id, visited, depth, "go_left")

            elif car.orientation == "ver":
                move_objs(state, car.id, visited, depth, "go_down")
                move_objs(state, car.id, visited, depth, "go_up")

    return False

def root_state(max_depht, cars):
    crossroad = [[False for x in range(size_of_mapa)] for y in range(size_of_mapa)]

    for car in cars:

        for i in range(car.size):

            if car.orientation == "ver":
                crossroad[car.y + i][car.x] = True

            elif car.orientation == "hor":
                crossroad[car.y][car.x + i] = True

    root_state = State(crossroad, cars, 0, None)
    return root_state

def iterative_deepening_search(max_depht, cars):
    t0 = time.time()
    global d_stack
    flag = False
    d = 0

    term_print(cars)
    while d != max_depht:
        print(f"***** Pokus c. {d} *****")
        state = root_state(max_depht, cars)
        d_stack.append(state)
        if dfs(state, d):
            flag = True
            break
        d += 1
    t1 = time.time()
    print("Cas: ", t1-t0)
    return flag

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
    max_depht = 20

    if not iterative_deepening_search(max_depht, cars):
        print("\nRiesenie sa nenaslo")
    pass

if __name__ == "__main__":
    print("PyCharm starting..")
    # sys.stdout = open("file.txt", "w")
    main()
    # end of program
