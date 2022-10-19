class BoardOutException(Exception):
    pass

BOARD_SIZE = 6

# RecursionError: maximum recursion depth exceeded in comparison. You are using the same name for the getter, setter and attribute. 
# When setting up a property, you must rename the attribute locally; the convention is to prefix it with an underscore.

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        if value <= BOARD_SIZE and value > 0:
            self._x = value
        else:
            raise ValueError("Координата X не может быть больше размера доски или меньше 0")
    
    @y.setter
    def y(self, value):
        if value <= BOARD_SIZE and value > 0:
            self._y = value
        else:
            raise ValueError("Координата Y не может быть больше размера доски или меньше 0")

    # Сравнение == Dot объектов
    def __eq__(self, other):
        if not isinstance(other, Dot):
            raise TypeError("Один из операндов не относится к типу Dot")
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, length, ship_bow, ship_direction, lives):
        self.length = length
        self.ship_bow = ship_bow
        self.ship_direction = ship_direction
        self.lives = lives
    
    def dots(self):
        ship_dots = []


        return

class Board:
    def __init__(self, board_dots, ship_list, hid, alive_ships):
        self.board_dots = None # !!!!!
        self.ship_list = ship_list
        self.hid = hid
        self.alive_ships = alive_ships

    def add_ship(self):
        pass

    def cotour(self):
        pass

    def show_board(self):
        pass

    def out(self):
        pass

    def shot(self):
        pass


class Player:
    def __init__(self):
        pass


class User(Player):
    pass


class AI(Player):
    pass

dot1 = Dot(1, 5)
dot2 = Dot(2, 3)

list_dots = [dot2, Dot(1, 5), Dot(5, 3)]

print(dot1 == dot2)
print(dot1 in list_dots)