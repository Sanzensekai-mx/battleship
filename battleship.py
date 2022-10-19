class BoardOutException(Exception):
    pass

# RecursionError: maximum recursion depth exceeded in comparison. You are using the same name for the getter, setter and attribute. 
# When setting up a property, you must rename the attribute locally; the convention is to prefix it with an underscore.

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Сравнение == Dot объектов
    def __eq__(self, other):
        if not isinstance(other, Dot):
            raise TypeError("Один из операндов не относится к типу Dot")
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"{self.__class__}{self.x, self.y}"

class Ship:
    def __init__(self, length, ship_bow: Dot, ship_direction):
        self.length = length
        self.ship_bow = ship_bow
        self.ship_direction = ship_direction
        self.lives = length
    
    def __dots(self):
        ship_dots = []
        ship_dots.append(self.ship_bow)
        if self.length > 1:
            cur_dot_x, cur_dot_y = self.ship_bow.x, self.ship_bow.y
            for i in range(self.length - 1):
                if self.ship_direction == 'vertically':
                    cur_dot_x += 1
                elif self.ship_direction == 'horizontally':
                    cur_dot_y += 1
                ship_dots.append(Dot(cur_dot_x, cur_dot_y))
        return ship_dots

class Board:
    def __init__(self, hid=False, board_size=6):
        self._board_dots = [[Dot(i, j) for j in range(1, board_size + 1)] for i in range(1, board_size + 1)]
        self.ship_list = [] # объкты Ships
        self.hid = hid
        # self.hid = hid # Тру или фалсе нужно ли скрывать корабли на доске
        self.alive_ships = 0 # Количество живых кораблей на доске

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
        # board = Board
        pass


class User(Player):
    pass


class AI(Player):
    pass

dot1 = Dot(1, 5)
dot2 = Dot(2, 3)

list_dots = [dot2, Dot(1, 5), Dot(5, 3)]

# print(dot1 == dot2)
# print(dot1 in list_dots)

board = Board()

print(board._board_dots)

ship = Ship(length=3, ship_bow=dot1, ship_direction='vertically')

print(ship._Ship__dots())