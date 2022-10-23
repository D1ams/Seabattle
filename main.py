class Board:
    def __init__(self):
        self.width = 6
        self.height = 6
        self.list = [['O' for i in range(self.width)] for j in range(self.height)]

    def __str__(self):
        end = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for num in enumerate(self.list):
            end += f"\n {num[0] + 1} | "
            end += " | ".join(num[1])
            end += ' |'
        end += "\n"
        return end

    def get_value(self, x, y):
        return self.list[x - 1][y - 1]

    def set_value(self, x, y):
        self.list[x - 1][y - 1] = 'T'


class User:
    def move(self, other):
        try:
            x, y = map(int, input("Введите координаты выстрела (гор, верт) ").split())
            if not (0 < x < 7) or not (0 < y < 7) or other.get_value(x, y) == "T":
                raise ValueError
        except ValueError:
            print("Невозможные кооридинаты, попробуйте снова!")
            self.move(other)
        else:
            other.set_value(x, y)


class Ship:
    def __init__(self, len, x, y, direct):
        self.len = len
        self.x = x
        self.y = y
        self.direct = direct




def main():
    board_1 = Board()
    user = User()
    print(board_1)
    user.move(board_1)
    print(board_1)


if __name__ == '__main__':
    main()
