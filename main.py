import random


class Board:
    def __init__(self, width=6, height=6):
        self.width = width
        self.height = height
        self.list = [['O' for _ in range(self.width)] for _ in range(self.height)]
        self.alive = None

    def create_list(self):
        self.list = [['O' for _ in range(self.width)] for _ in range(self.height)]

    def __str__(self):
        end = "   | 1 | "
        str_ = []
        for num in range(2, self.width + 1):
            str_.append(str(num))
        end += ' | '.join(str_)
        end += ' |'
        for num in enumerate(self.list):
            end += f"\n {num[0] + 1} | "
            end += " | ".join(num[1])
            end += ' |'
        end += "\n"
        return end

    def check_alive(self):
        self.alive = False
        for num in self.list:
            for j in num:
                if j == '█':
                    self.alive = True
                    break
            if self.alive:
                break
        return self.alive

    def set_ship(self, ship):
        if ship.direct_get == 'U' or ship.direct_get == 'D':
            for num in ship.coord_get:
                self.list[num - 1][ship.x_get - 1] = '█'
        else:
            for num in ship.coord_get:
                self.list[ship.y_get - 1][num - 1] = '█'

    def copy_value(self, board, user):
        self.list[user.get_y_user - 1][user.get_x_user - 1] = board.get_value(user.get_x_user, user.get_y_user)

    def set_value(self, x, y):
        if self.get_value(x, y) == 'O' or self.get_value(x, y) == '□':
            self.list[y - 1][x - 1] = 'T'
        else:
            self.list[y - 1][x - 1] = 'X'

    def set_blank(self, x, y):
        self.list[y - 1][x - 1] = '□'

    def copy_blanks(self, board):
        for i, v in enumerate(board.list):
            for j, k in enumerate(v):
                if k == '□':
                    self.set_blank(j + 1, i + 1)

    def ship_check_alive(self, ship):
        ship_alive = False
        if ship.ship_alive_get:
            if ship.direct_get == 'U' or ship.direct_get == 'D':
                for num in ship.coord_get:
                    if self.list[num - 1][ship.x_get - 1] == '█':
                        ship_alive = True
                        break
            else:
                for num in ship.coord_get:
                    if self.list[ship.y_get - 1][num - 1] == '█':
                        ship_alive = True
                        break

        if (not ship_alive) and ship.ship_alive_get:
            ship.ship_alive_get = ship_alive
            if ship.direct_get == 'U' or ship.direct_get == 'D':
                for num in ship.coord_check_get:
                    if num == ship.coord_check_get[0] and ship.coord_check_get[0] != ship.coord_get[0]:
                        self.set_blank(ship.x_get, num)
                    if num == ship.coord_check_get[-1] and ship.coord_check_get[-1] != ship.coord_get[-1]:
                        self.set_blank(ship.x_get, num)
                    if ship.x_get == 1:
                        self.set_blank(ship.x_get + 1, num)
                    elif ship.x_get == self.get_width:
                        self.set_blank(ship.x_get - 1, num)
                    else:
                        self.set_blank(ship.x_get - 1, num)
                        self.set_blank(ship.x_get + 1, num)
            else:
                for num in ship.coord_check_get:
                    if num == ship.coord_check_get[0] and ship.coord_check_get[0] != ship.coord_get[0]:
                        self.set_blank(num, ship.y_get)
                    if num == ship.coord_check_get[-1] and ship.coord_check_get[-1] != ship.coord_get[-1]:
                        self.set_blank(num, ship.y_get)
                    if ship.y_get == 1:
                        self.set_blank(num, ship.y_get + 1)
                    elif ship.y_get == self.get_height:
                        self.set_blank(num, ship.y_get - 1)
                    else:
                        self.set_blank(num, ship.y_get - 1)
                        self.set_blank(num, ship.y_get + 1)

    def get_value(self, x, y):
        return self.list[y - 1][x - 1]

    @property
    def get_alive(self):
        return self.alive

    @property
    def get_width(self):
        return self.width

    @get_width.setter
    def get_width(self, value):
        if 5 < value < 10:
            self.width = value
        else:
            print("Такой ширины не может быть! Ширина будет равна 6")

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def get_height(self, value):
        if 5 < value < 10:
            self.height = value
        else:
            print("Такой высоты не может быть! Высота будет равна 6")


class User:
    def __init__(self):
        self.x_user = None
        self.y_user = None
        self.direct_user = None

    def move(self, board):
        try:
            x, y = map(int, input("Введите координаты выстрела (гор, верт) ").split())
            if not (0 < x < board.get_width + 1) or not (0 < y < board.get_height + 1) or board.get_value(x,
                                                                                                             y) == "T" or board.get_value(
                    x, y) == "X" or board.get_value(x, y) == '□':
                raise ValueError
        except ValueError:
            print("Невозможные кооридинаты, попробуйте снова!")
            self.move(board)
        else:
            self.x_user = x
            self.y_user = y
            board.set_value(self.x_user, self.y_user)

    def set_ship_user(self, ship, board):
        try:
            x, y = map(int, input("Введите начало координат коробля (гор, верт) ").split())
            direct = 'U'
            if not (0 < x < board.get_width + 1) or not (0 < y < board.get_height + 1):
                raise ValueError
            if ship.get_len != 1:
                direct = input("Куда смотрит ваш корабль? (U=UP, R=RIGHT, L=LEFT, D=DOWN) ")
            if not (direct == 'U' or direct == 'R' or direct == 'L' or direct == 'D'):
                raise ValueError
        except ValueError:
            print("Невозможные кооридинаты, попробуйте снова!")
            self.set_ship_user(ship, board)
        else:
            self.x_user = x
            self.y_user = y
            self.direct_user = direct
            ship.set_ship(self, board)

    @property
    def get_x_user(self):
        return self.x_user

    @property
    def get_y_user(self):
        return self.y_user

    @property
    def get_direct_user(self):
        return self.direct_user


class AI(User):
    board_filled = None

    def move(self, board):
        try:
            x, y = random.randint(1, board.get_width), random.randint(1, board.get_height)
            if board.get_value(x, y) == "T" or board.get_value(x, y) == "X" or board.get_value(x, y) == "□":
                raise ValueError
        except ValueError:
            self.move(board)
        else:
            board.set_value(x, y)

    def set_ship_user(self, ship, board):
        x, y = random.randint(1, board.get_width), random.randint(1, board.get_height)
        directs = ['U', 'D', 'R', 'L']
        c = random.randint(0, 3)
        direct = directs[c]
        self.x_user = x
        self.y_user = y
        self.direct_user = direct
        try:
            ship.set_ship(self, board)
        except RecursionError:
            board.create_list()
            self.board_filled = False

    @property
    def get_board_filled(self):
        return self.board_filled

    @get_board_filled.setter
    def get_board_filled(self, value):
        self.board_filled = value


class Ship:
    def __init__(self, len):
        self.x = None
        self.y = None
        self.direct = None
        self.len = len
        self.coord = None
        self.coord_check = None
        self.ship_alive = True

    def set_ship(self, user, board):
        try:
            x, y = user.get_x_user, user.get_y_user
            direct = user.get_direct_user
            if self.len != 1:
                if direct == 'U' and not (0 < y - (self.len - 1) < board.get_height + 1):
                    raise ValueError
                if direct == 'D' and not (0 < y + (self.len - 1) < board.get_height + 1):
                    raise ValueError
                if direct == 'R' and not (0 < x + (self.len - 1) < board.get_width + 1):
                    raise ValueError
                if direct == 'L' and not (0 < x - (self.len - 1) < board.get_width + 1):
                    raise ValueError
            if direct == 'U' or direct == 'D':
                if direct == 'U':
                    y_list = [i for i in range(y - (self.get_len - 1), y + 1)]
                else:
                    y_list = [i for i in range(y, y + self.get_len)]
                y_list_check = y_list.copy()
                if y_list[0] != 1:
                    y_list_check.insert(0, y_list[0] - 1)
                if y_list[-1] != board.get_height:
                    y_list_check.append(y_list[-1] + 1)
                for num in y_list_check:
                    if board.get_value(x, num) == '█':
                        raise ValueError
                    if x == 1:
                        if board.get_value(x + 1, num) == '█':
                            raise ValueError
                    elif x == board.get_width:
                        if board.get_value(x - 1, num) == '█':
                            raise ValueError
                    else:
                        if board.get_value(x - 1, num) == '█' or board.get_value(x + 1, num) == '█':
                            raise ValueError
            else:
                if direct == 'L':
                    x_list = [i for i in range(x - (self.get_len - 1), x + 1)]
                else:
                    x_list = [i for i in range(x, x + self.get_len)]
                x_list_check = x_list.copy()
                if x_list[0] != 1:
                    x_list_check.insert(0, x_list[0] - 1)
                if x_list[-1] != board.get_width:
                    x_list_check.append(x_list[-1] + 1)
                for num in x_list_check:
                    if board.get_value(num, y) == '█':
                        raise ValueError
                    if y == 1:
                        if board.get_value(num, y + 1) == '█':
                            raise ValueError
                    elif y == board.get_height:
                        if board.get_value(num, y - 1) == '█':
                            raise ValueError
                    else:
                        if board.get_value(num, y - 1) == '█' or board.get_value(num, y + 1) == '█':
                            raise ValueError
        except ValueError:
            if not isinstance(user, AI):
                print("Невозможные кооридинаты, попробуйте снова!")
            user.set_ship_user(self, board)

        else:
            self.x = x
            self.y = y
            self.direct = direct
            if self.direct == 'U' or self.direct == 'D':
                self.coord = y_list
                self.coord_check = y_list_check
            else:
                self.coord = x_list
                self.coord_check = x_list_check
            board.set_ship(self)

    @property
    def get_len(self):
        return self.len

    @property
    def x_get(self):
        return self.x

    @property
    def ship_alive_get(self):
        return self.ship_alive

    @ship_alive_get.setter
    def ship_alive_get(self, value):
        self.ship_alive = value

    @property
    def y_get(self):
        return self.y

    @property
    def direct_get(self):
        return self.direct

    @property
    def coord_get(self):
        return self.coord

    @property
    def coord_check_get(self):
        return self.coord_check


def main():
    try:
        x, y = map(int, input("Введите размер доски (гор, верт) от 6 до 9 ").split())
    except ValueError:
        print('Такой доски не может быть!')
    else:
        user = User()
        computer = AI()
        board_1_user = Board()
        board_1_user.get_width = x
        board_1_user.get_height = y
        board_1_user.create_list()
        board_2_user = Board(board_1_user.get_width, board_1_user.get_height)
        board_3_AI = Board(board_1_user.get_width, board_1_user.get_height)
        ship_len3_user = [Ship(3)]
        # ship_len2_user = [Ship(2) for _ in range(2)]
        # ship_len1_user = [Ship(1) for _ in range(4)]
        ships_user = []
        # ships_user.extend(ship_len1_user)
        # ships_user.extend(ship_len2_user)
        ships_user.extend(ship_len3_user)
        ship_len3_computer = [Ship(3)]
        ship_len2_computer = [Ship(2) for _ in range(2)]
        ship_len1_computer = [Ship(1) for _ in range(4)]
        ships_computer = []
        ships_computer.extend(ship_len3_computer)
        ships_computer.extend(ship_len2_computer)
        ships_computer.extend(ship_len1_computer)
        print(board_1_user)
        for num in ships_user:
            print(f'Корабль длинной в {num.get_len} ')
            user.set_ship_user(num, board_1_user)
            print(board_1_user)
        while True:
            computer.get_board_filled = None
            for num in ships_computer:
                computer.set_ship_user(num, board_3_AI)
                if computer.get_board_filled is False:
                    break
            if computer.get_board_filled is None:
                break
        print("Ваша доска ( T - промахи, X - попадания, █ - корабль) и Доска ваших выстрелов ")
        print(board_1_user)
        print(board_2_user)
        while True:
            user.move(board_3_AI)
            board_2_user.copy_value(board_3_AI, user)
            computer.move(board_1_user)
            for num in ships_user:
                board_1_user.ship_check_alive(num)
            for num in ships_computer:
                board_3_AI.ship_check_alive(num)
            board_2_user.copy_blanks(board_3_AI)
            print("Ваша доска ( T - промахи, X - попадания, █ - корабль) и Доска ваших выстрелов ")
            print(board_1_user)
            print(board_2_user)
            print(board_3_AI)
            if not (board_1_user.check_alive() and board_3_AI.check_alive()):
                if board_1_user.check_alive():
                    print("Пользователь победил!")
                elif board_3_AI.check_alive():
                    print("Доска комьютера ")
                    print(board_3_AI)
                    print("Компьютер победил!")
                else:
                    print("Ничья!")
                break


if __name__ == '__main__':
    main()
