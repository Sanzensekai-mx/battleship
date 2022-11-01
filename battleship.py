import random
from time import sleep


class BoardShipException(Exception):
    pass


class BoardDotOutException(Exception):
    pass

class BoardShotException(Exception):
    pass


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
        return f"{self.x + 1, self.y + 1}"


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
        self._board_dots = [["O"] * board_size for i in range(board_size)]
        self.ship_list = [] # объекты Ships
        self.hid = hid
        self.board_size = board_size
        self.alive_ships = 0 # Количество живых кораблей на доске
        self.not_empty_dots = []
        self.last_board_event = []
        self.last_dot_event = None

    def out(self, dot):
        return not((self.board_size > dot.x >= 0) and (self.board_size > dot.y >= 0))

    def add_ship(self, ship: Ship):
        # print(ship.dots())
        for dot in ship.dots():
            if self.out(dot):
                raise BoardShipException(f"Невозможно разместить корабль в точке: {dot.x} {dot.y + 1}" if ship.ship_direction == 'horizontally' 
                                            else f"Невозможно разместить корабль в точке: {dot.x + 1} {dot.y}")
            for a_dot in self.not_empty_dots:
                if dot == a_dot and self._board_dots[dot.x][dot.y] == '■':
                    raise BoardShipException(f"В этой точке уже стоит другой корабль: {dot.x} {dot.y + 1}" if ship.ship_direction == 'horizontally' 
                                            else f"В этой точке уже стоит другой корабль: {dot.x + 1} {dot.y}")
                elif dot == a_dot:
                    raise BoardShipException(f"В этой точке по правилам нельзя ставить корабль: {dot.x} {dot.y + 1}" if ship.ship_direction == 'horizontally' 
                                            else f"В этой точке по правилам нельзя ставить корабль: {dot.x + 1} {dot.y}")

        for dot in ship.dots():
            self.not_empty_dots.append(dot)
            self._board_dots[dot.x][dot.y] = "■"
        self.ship_list.append(ship)
        self.alive_ships += 1
                

    def contour(self, ship: Ship, change_board_layout=False):
        # Использовать out, not_empty_dots
        for dot in ship.dots():
            near_dots = [Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y), Dot(dot.x, dot.y + 1),
                    Dot(dot.x, dot.y - 1), Dot(dot.x + 1, dot.y + 1), Dot(dot.x - 1, dot.y - 1),
                    Dot(dot.x + 1, dot.y - 1), Dot(dot.x - 1 , dot.y + 1)]
            for n_dot in near_dots:
                if self.out(n_dot) or n_dot in ship.dots():
                    continue
                self.not_empty_dots.append(n_dot)
                if change_board_layout:
                    self._board_dots[n_dot.x][n_dot.y] = 'T'

    def shot(self, dot):
        if self.out(dot):
            raise BoardDotOutException()
        if self._board_dots[dot.x][dot.y] in ('T', 'X'):
            raise BoardShotException()
        self.not_empty_dots.append(dot)
        for ship in self.ship_list:
            if dot in ship.dots():
                self.last_dot_event = dot
                ship.lives -= 1
                self._board_dots[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    # Корабль уничтожен
                    self.contour(ship, change_board_layout=True)
                    self.alive_ships -= 1
                    # self.last_board_event = 'Корабль уничтожен!!!'
                    self.last_board_event.append(('Корабль уничтожен!!!', dot))
                    return True
                elif ship.lives > 0:
                    # ранен
                    self.last_board_event.append(('Ранен корабль!', dot))
                    # self.last_board_event = 'Ранен корабль!'
                    return True
        # промах
        self._board_dots[dot.x][dot.y] = 'T'
        # self.last_dot_event = dot
        self.last_board_event.append(('Промах!', dot))
        # self.last_board_event = 'Промах!'
        return False

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
    def __init__(self, player_board, enemy_board):
        self.player_board = player_board
        self.enemy_board = enemy_board

    def ask(self):
        pass # Вернуть Dot объект

    def move(self):
        # asked_dot_to_shot = self.ask()
        shot_result = None
        shot_not_valid = True
        while shot_not_valid:
            asked_dot_to_shot = self.ask()
            try:
                shot_result = self.enemy_board.shot(asked_dot_to_shot)
                shot_not_valid = False
            except BoardShotException:
                print('\n!!! Нельзя стрелять в уже подбитую клетку')
                continue
        while shot_result:
            # asked_dot_to_shot = self.ask()
            shot_not_valid = True
            while shot_not_valid:
                asked_dot_to_shot = self.ask()
                try:
                    shot_result = self.enemy_board.shot(asked_dot_to_shot)
                    shot_not_valid = False
                except BoardShotException:
                    print('\n!!! Нельзя стрелять в уже подбитую клетку')
                    continue


class User(Player):
    def ask(self):
        print(f"""
Моя доска
{self.player_board}

Доска врага
{self.enemy_board}
\n""")
        while True:
            # try:
                # if self.enemy_board.last_board_event[-1][0] == 'Промах!':
                #     self.enemy_board.last_board_event = [('Промах!', self.enemy_board.last_dot_event)]
                # if self.player_board.last_board_event[-1][0] == 'Промах!':
                    # self.player_board.last_board_event = [('Промах!', self.player_board.last_dot_event)]
            # except IndexError:
                # pass
            try:
                print(f"Результаты моего выстрела: {self.enemy_board.last_board_event}")
                print(f"Результаты выстрела врага: {self.player_board.last_board_event}")
                # print(f"Результаты моего выстрела: {self.enemy_board.last_board_event[-1]}")
                # print(f"Результаты выстрела врага: {self.player_board.last_board_event[-1]}")
            except IndexError:
                pass
            print("Введите координаты точки для выстрела через пробел")
            print('Например: --> 1 2 ')
            user_input = input("--> ").split()
            try:
                return Dot(int(user_input[0]) - 1, int(user_input[1]) - 1)
            except IndexError:
                print("Неправильный ввод")
                continue


class AI(Player):
    def ask(self):
        print('Ход врага')
        for i in ['.' for _ in range(3)]:
            sleep(0.5)
            print(i)
        # !!! Дополнить алгоритм 
        dot = self.player_board.last_board_event[-1][1]
        if self.player_board.last_board_event[-1][0] == 'Ранен корабль!':
            near_dots = [Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y), Dot(dot.x, dot.y + 1),
                    Dot(dot.x, dot.y - 1), Dot(dot.x + 1, dot.y + 1), Dot(dot.x - 1, dot.y - 1),
                    Dot(dot.x + 1, dot.y - 1), Dot(dot.x - 1 , dot.y + 1)]
            return random.choice(near_dots)
        return Dot(random.randint(0, 5), random.randint(0, 5))


class Game:
    def __init__(self):
        self.user_board = self.random_board()
        self.ai_board = self.random_board(hid_board=True)
        self.user_player = User(self.user_board, self.ai_board)
        self.ai_player = AI(self.ai_board, self.user_board)
    
    def random_board(self, hid_board=False):
        ship_to_place = [3, 2, 2, 1, 1, 1, 1]
        while True:
            board = Board(hid=hid_board)
            is_valid_board = True
            for i in ship_to_place:
                count_try = 0
                while count_try < 1000:
                    direction = 'vertically' if random.randint(0, 1) == 1 else 'horizontally'
                    cur_ship = Ship(length=i, ship_bow=Dot(random.randint(0, board.board_size - 1), random.randint(0, board.board_size - 1)),
                                ship_direction=direction)
                    try:
                        board.add_ship(cur_ship)
                        board.contour(cur_ship)
                        break
                    except BoardShipException as e:
                        # print(e)
                        count_try += 1
                        continue
                    
                if count_try >= 1000:
                    is_valid_board = False
                    break
            if not is_valid_board:
                continue
            return board


    def greet(self):
        print("""
╔══╗─╔═══╗╔════╗╔════╗╔╗───╔═══╗╔═══╗╔╗─╔╗╔══╗╔═══╗
║╔╗║─║╔═╗║║╔╗╔╗║║╔╗╔╗║║║───║╔══╝║╔═╗║║║─║║╚╣─╝║╔═╗║
║╚╝╚╗║║─║║╚╝║║╚╝╚╝║║╚╝║║───║╚══╗║╚══╗║╚═╝║─║║─║╚═╝║
║╔═╗║║╚═╝║──║║────║║──║║─╔╗║╔══╝╚══╗║║╔═╗║─║║─║╔══╝
║╚═╝║║╔═╗║──║║────║║──║╚═╝║║╚══╗║╚═╝║║║─║║╔╣─╗║║───
╚═══╝╚╝─╚╝──╚╝────╚╝──╚═══╝╚═══╝╚═══╝╚╝─╚╝╚══╝╚╝───
        """)
        print("")

    def loop(self):
        who_move = 0
        while self.user_board.alive_ships > 0 or self.ai_board.alive_ships > 0:
            if who_move == 0:
                self.user_player.move()
                who_move = 1
            elif who_move == 1:
                self.ai_player.move()
                who_move = 0
        print("Игрок победил" if self.user_board.alive_ships > 0 and self.ai_board.alive_ships == 0 else "AI победил")
    
    def start(self):
        self.greet()
        self.loop()

        

if __name__ == '__main__':
    game = Game()
    game.start()