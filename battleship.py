class BoardShipException(Exception):
    pass

class BoardDotOutException(Exception):
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
    
    def dots(self):
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
        # self._board_dots = [[Dot(i, j) for j in range(1, board_size + 1)] for i in range(1, board_size + 1)]
        self._board_dots = [["O"] * board_size for i in range(board_size)]
        self.ship_list = [] # объекты Ships
        self.hid = hid
        self.board_size = board_size
        self.alive_ships = 0 # Количество живых кораблей на доске
        self.not_empty_dots = []

    def out(self, dot):
        return not((self.board_size > dot.x >= 0) and (self.board_size > dot.y >= 0))

    def add_ship(self, ship: Ship):
        for dot in ship.dots():
            if self.out(dot):
                raise BoardShipException(f"Невозможно разместить корабль в точке: {dot.x} {dot.y + 1}" if ship.ship_direction == 'horizontally' 
                                            else f"Невозможно разместить корабль в точке: {dot.x + 1} {dot.y}")
            for another_ship in self.ship_list:
                # print(another_ship.dots())
                for a_dot in another_ship.dots():
                    if dot == a_dot:
                        # print(f'{dot} == {a_dot}')
                        raise BoardShipException(f"В этой точке уже стоит другой корабль: {dot.x} {dot.y + 1}" if ship.ship_direction == 'horizontally' 
                                            else f"В этой точке уже стоит другой корабль: {dot.x + 1} {dot.y}")
        for dot in ship.dots():
            self._board_dots[dot.x][dot.y] = "■"
            # self.not_empty_dots.append(dot) # BoardShipException при shoot
        self.ship_list.append(ship)
                

    def contour(self, ship: Ship, change_board_layout=False):
        # ship_contour = []
        # Использовать out, not_empty_dots
        for dot in ship.dots():
            near_dots = [Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y), Dot(dot.x, dot.y + 1),
                    Dot(dot.x, dot.y - 1), Dot(dot.x + 1, dot.y + 1), Dot(dot.x - 1, dot.y - 1),
                    Dot(dot.x + 1, dot.y - 1), Dot(dot.x - 1 , dot.y + 1)]
            for n_dot in near_dots:
                if self.out(n_dot):
                    continue
                if n_dot not in self.not_empty_dots:
                    self.not_empty_dots.append(n_dot)
                    if change_board_layout:
                        self._board_dots[n_dot.x][n_dot.y] = 'T'

    def shot(self, dot):
        if self.out(dot):
            raise BoardDotOutException()
        if dot in self.not_empty_dots:
            raise BoardShipException()
        
        self.not_empty_dots.append(dot)
        for ship in board.ship_list:
            if dot in ship.dots():
                ship.lives -= 1
                self._board_dots[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    # Корабль уничтожен
                    self.contour(ship, change_board_layout=True)
                    return
                elif ship.lives > 0:
                    # ранен
                    return
        # промах
        self._board_dots[dot.x][dot.y] = 'T'


    def __str__(self):
        result = '  |1|2|3|4|5|6|'
        for idx, line in enumerate(self._board_dots, 1):
            line_copy = line.copy()
            if self.hid:
                for i, c in enumerate(line_copy):
                    if c == '■':
                        line_copy[i] = 'O'
            result += f"\n{idx} |{'|'.join(line_copy)}|"
        return result

class Player:
    def __init__(self):
        # board = Board
        pass


class User(Player):
    pass


class AI(Player):
    pass

dot1 = Dot(0, 2)
dot2 = Dot(2, 3)

list_dots = [dot2, Dot(0, 5), Dot(5, 3)]

# print(dot1 == dot2)
# print(dot1 in list_dots)

board = Board(hid=True)

# print(board._board_dots)

ship1 = Ship(length=3, ship_bow=dot1, ship_direction='horizontally')
ship2 = Ship(length=2, ship_bow=dot2, ship_direction='vertically')

# print(ship1.dots())

# board.add_ship(ship1)
# board.add_ship(ship2)



dot3 = Dot(2, 3)

ship3 = Ship(length=3, ship_bow=dot3, ship_direction='vertically')
print(ship3.dots())
board.add_ship(ship3)
# board.contour(ship3)
print(board.not_empty_dots)

# for row in board._board_dots:
    # print(row)
# print(board.out(dot3))
board.shot(Dot(1, 3))
board.shot(Dot(2, 3))
# print(board.not_empty_dots)
board.shot(Dot(3, 3))
board.shot(Dot(4, 3))
print(board)