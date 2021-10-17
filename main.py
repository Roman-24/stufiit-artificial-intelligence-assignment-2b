
import collections

size_of_mapa = None

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
        self.x = x
        self.y = y
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



# class map: ???

# class stav ???



def iterative_deepening_search(max_depht, cars):

    pass


# Defining main function
def main():

    cars = []
    global size_of_mapa
    with open("vstup.txt", "r") as input_file:

        # nacitanie a vytvorenie objektov auticka v liste cars podla vstupneho suboru
        while True:
            line = input_file.readline()

            if line.startswith("*"):
                size_of_mapa = line.split(" ", 1)
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
    iterative_deepening_search(max_depht, cars)
    pass


if __name__ == "__main__":
    print("PyCharm starting..")
    main()
    # end of program
