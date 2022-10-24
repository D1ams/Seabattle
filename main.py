import random


class Board:
    def __init__(self):
        self.width = 6
        self.height = 6
        self.list = [['O' for i in range(self.width)] for j in range(self.height)]
        self.alive = None

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

    def set_ship(self, ship):
        if ship.direct_get == 'U' or ship.direct_get == 'D':
            for num in ship.coord_get:
                self.list[num - 1][ship.x_get - 1] = '█'
        else:
            for num in ship.coord_get:
                self.list[ship.y_get - 1][num - 1] = '█'

    def set_value(self, x, y):
        if self.get_value(x, y) == 'O':
            self.list[y - 1][x - 1] = 'T'
        else:
            self.list[y - 1][x - 1] = 'X'

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
        self.get_width = value

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def get_height(self, value):
        self.get_height = value


class User:
    def __init__(self):
        self.x_user = None
        self.y_user = None
        self.direct_user = None

    def move(self, board):
        try:
            x, y = map(int, input("Введите координаты выстрела (гор, верт) ").split())
            if not (0 < x < board.get_width + 1) or not (0 < y < board.get_height + 1) or board.get_value(x, y) == "T":
                raise ValueError
        except ValueError:
            print("Невозможные кооридинаты, попробуйте снова!")
            self.move(board)
        else:
            board.set_value(x, y)

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
    def move(self, board):
        try:
            x, y = random.randint(1, board.get_width), random.randint(1, board.get_height)
            if board.get_value(x, y) == "T":
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
        ship.set_ship(self, board)


class Ship:
    def __init__(self, len):
        self.x = None
        self.y = None
        self.direct = None
        self.len = len
        self.coord = None

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
            else:
                self.coord = x_list
            board.set_ship(self)

    @property
    def get_len(self):
        return self.len

    @property
    def x_get(self):
        return self.x

    @property
    def y_get(self):
        return self.y

    @property
    def direct_get(self):
        return self.direct

    @property
    def coord_get(self):
        return self.coord


def main():
    pass


if __name__ == '__main__':
    main()
