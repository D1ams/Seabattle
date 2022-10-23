
class Board:
    def __init__(self):
        self.width = 6
        self.height = 6
        self.list = [['O' for i in range(self.width)] for j in range(self.height)]

    def __str__(self):
        end = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for num in self.list:
            end += "\n   | "
            end += " | ".join(num)
            end += ' |'
        return end




def main():
    board_1 = Board()
    print(board_1)


if __name__ == '__main__':
    main()
