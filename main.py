from classes import *


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
        ship_len2_user = [Ship(2) for _ in range(2)]
        ship_len1_user = [Ship(1) for _ in range(4)]
        ships_user = []
        ships_user.extend(ship_len1_user)
        ships_user.extend(ship_len2_user)
        ships_user.extend(ship_len3_user)
        ship_len3_computer = [Ship(3)]
        ship_len2_computer = [Ship(2) for _ in range(2)]
        ship_len1_computer = [Ship(1) for _ in range(4)]
        ships_computer = []
        ships_computer.extend(ship_len3_computer)
        ships_computer.extend(ship_len2_computer)
        ships_computer.extend(ship_len1_computer)
        print(board_1_user)
        while True:
            for num in ships_user:
                print(f'Корабль длинной в {num.get_len} ')
                user.set_ship_user(num, board_1_user)
                if user.get_reset:
                    break
                print(board_1_user)
            if not user.get_reset:
                break
            user.get_reset = False

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
