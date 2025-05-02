import shlex
import field

def main():
    rows = int(input())
    columns = int(input())
    command = input()
    a_field = field.Field(rows, columns)
    a_field.print_grid()

    while True:
        command = input()
        command_lst = shlex.split(command)
        if command == 'Q':
            break
        elif command[0] == 'F':
            a_field.create_faller(command_lst)
        elif command[0] == 'B':
            a_field.rotate_faller_counter_clockwise()
        elif command[0] == 'A':
             a_field.rotate_faller_clockwise()
        elif command[0] == 'V':
            a_field.create_virus(command_lst)
        elif command[0] == '>':
            a_field.move_right()
        elif command[0] == '<':
            pass
        elif command[0] == 'V':
            pass
        elif command[0] == '':
            pass
        



if __name__ == '__main__':
    main()







