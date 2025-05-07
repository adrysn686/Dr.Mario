import shlex
from gameboard import GameBoard

def main():
    rows = int(input())
    columns = int(input())
    create_board_command = input()
    if create_board_command == 'EMPTY':
        gameboard = GameBoard(rows, columns)
        gameboard.print_grid()
    elif create_board_command == "CONTENTS":
        row_list = []
        for _ in range(rows):
            row = input()
            row_list.append(row)
        gameboard = GameBoard(rows, columns, row_list)
        if not gameboard.isMatch:
            gameboard.print_grid()

    while True:
        command = input()
        command_lst = shlex.split(command)
        if command == 'Q':
            break
        elif command == '':
            gameboard.time()
        elif command[0] == 'F':
            gameboard.create_faller(command_lst)
        elif command[0] == 'B':
            gameboard.rotate_gameboard_counter_clockwise()
        elif command[0] == 'A':
            gameboard.rotate_gameboard_clockwise()
        elif command[0] == 'V':
            gameboard.create_virus(command_lst)
        elif command[0] == '>':
            gameboard.move_right()
        elif command[0] == '<':
            gameboard.move_left()
        elif command[0] == 'V':
            gameboard.create_virus()
        



if __name__ == '__main__':
    main()







