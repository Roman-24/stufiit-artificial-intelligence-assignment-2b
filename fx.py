
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
    # Car constructor
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

class Node:
    # Node constructor
    def __init__(self, cars, depth, parent, note):
        # vytvorenie uzla zo zaznamom na predchodcu,jeho hlbku,posun, a nove rozlozenie aut, dvoj dimenzionalne pole
        self.depth = depth
        self.cars = cars
        self.parent = parent
        self.note = note

class GoDown:

    def __init__(self):
        pass

    def go_down(self, cars, distance_to_go, id, node, depth):
        new_state = State()
        note = f"auto {auticka_dict[cars[id - 1].id]} islo go_down o {distance_to_go}"
        cars[id - 1].y += distance_to_go
        return new_state.creat_child(cars, depth, node, note)

class GoLeft:

    def __init__(self):
        pass

    def go_left(self, cars, distance_to_go, id, node, depth):
        new_state = State()
        note = f"auto {auticka_dict[cars[id - 1].id]} islo go_left o {distance_to_go}"
        cars[id - 1].x -= distance_to_go
        return new_state.creat_child(cars, depth, node, note)

class GoRight:

    def __init__(self):
        pass

    def go_right(self, cars, distance_to_go, id, node, depth):
        new_state = State()
        note = f"auto {auticka_dict[cars[id - 1].id]} islo go_right o {distance_to_go}"
        cars[id - 1].x += distance_to_go
        return new_state.creat_child(cars, depth, node, note)

class GoUp:

    def __init__(self):
        pass

    def go_up(self, cars, distance_to_go, id, node, depth):
        new_state = State()
        note = f"auto {auticka_dict[cars[id - 1].id]} islo go_up o {distance_to_go}"
        cars[id - 1].y -= distance_to_go
        return new_state.creat_child(cars, depth, node, note)

class State:

    def __init__(self):
        pass

    root = Main()    
    def generovanie(self, node, d):

        # potrebujem tu cars
        cars = node.cars

        my_map = [[0 for x in range(size_of_mapa)] for y in range(size_of_mapa)]

        for i in range(len(cars)):
            pom_x = cars[i][2] - 1
            pom_y = cars[i][3] - 1

            # vykreslovanie aut do mapky
            if cars[i].orientation == "ver":
                if cars[i].size == 2:
                    my_map[pom_x][pom_y] = cars[i].id
                    my_map[pom_x + 1][pom_y] = cars[i].id
                else:
                    my_map[pom_x][pom_y] = cars[i].id
                    my_map[pom_x + 1][pom_y] = cars[i].id
                    my_map[pom_x + 2][pom_y] = cars[i].id

            if cars[i].orientation == "hor":
                if cars[i].size == 2:
                    my_map[pom_x][pom_y] = cars[i].id
                    my_map[pom_x][pom_y + 1] = cars[i].id

                else:
                    my_map[pom_x][pom_y] = cars[i].id
                    my_map[pom_x][pom_y + 1] = cars[i].id
                    my_map[pom_x][pom_y + 2] = cars[i].id
        # koniec vykreslenia mapy

        for car in cars:

            poc_L = 0
            poc_R = 0
            poc_U = 0
            poc_D = 0

            stav_p = False

            if car.orientation == "hor":

                # posun vlavo
                if 1 < car.x:
                    for l in range(car.x - 1, 0, -1):
                        if l - 1 < 0:
                            stav_p = True
                        if not stav_p:
                            if my_map[car.y - 1][l - 1] == 0:
                                poc_L += 1
                            else:
                                stav_p = True

                # posun vpravo
                posun_v_pravo = car.x + car.size
                stav_p = False
                if posun_v_pravo < 7:
                    for l in range(posun_v_pravo - 1, 6):
                        if posun_v_pravo < 6:
                            stav_p = True
                        if not stav_p:
                            if my_map[car.y - 1][l]:
                                poc_R += 1
                            else:
                                stav_p = True

            if car.orientation == "ver":

                # posun hore
                if 1 < car.x:
                    for l in range(car.x - 1, 0, -1):
                        if l - 1 < 0:
                            stav_p = True
                        if not stav_p:
                            if my_map[l - 1][car.x - 1] == 0:
                                poc_U += 1
                            else:
                                stav_p = True

                # posun dole
                posun_dole = car.x + car.size
                stav_p = False
                if posun_dole < 7:
                    for l in range(posun_dole - 1, 6):
                        if posun_dole > 6:
                            stav_p = True
                        if not stav_p:
                            if my_map[l][car.x - 1]:
                                poc_D += 1
                            else:
                                stav_p = True

            go_left_obj = GoLeft()
            for i in range(poc_L):
                root.lifo.append(go_left_obj.go_left(self.prepispola(node.cars), i, car, node, d))

            go_right_obj = GoRight()
            for i in range(poc_R):
                root.lifo.append(go_right_obj.go_right(self.prepispola(node.cars), i, car, node, d))

            go_up_obj = GoLeft()
            for i in range(poc_U):
                root.lifo.append(go_up_obj.go_left(self.prepispola(node.cars), i, car, node, d))

            go_down_onj = GoDown()
            for i in range(poc_D):
                root.lifo.append(go_down_onj.go_down(self.prepispola(node.cars), i, car, node, d))

    def prepispola(self, old_cars):
        new_cars = []
        for old_car in old_cars:
            new_cars.append(Car(int(old_car.id), int(old_car.size), int(old_car.x), int(old_car.y), old_car.orientation))
        return new_cars

    def kontrola_uzla(self, node):
        temp_node = Node()




def iterative_deepening_search(cars, max_depth):

    pass

class Main:
    
    lifo = []
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
                del (input_file, line, id, size, x, y, orientation)
                break
            else:
                id, size, x, y, orientation = line.split(",", 4)
                cars.append(Car(int(id), int(size), int(x), int(y), orientation[:-1]))

    if __name__ == "__main__":
        print("PyCharm starting..")
        # sys.stdout = open("file.txt", "w")
        # Node(cars, depth, parent, note)
        root = Node(cars, 0, None, "Start")
        state = State()
        lifo.append(root)
        state.algoritmus(lifo)
        # end of program