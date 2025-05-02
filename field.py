class Field:
    FALLING = 1
    LANDING = 2
    FREEZING = 3

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.faller_lst = []
        self.virus_lst = []
    
        for row in range(rows):
            row = []
            for column in range(columns):
                row.append('   ')
            self.grid.append(row)

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def create_faller(self, command_lst):
         #if number of columns is odd
        if self.columns % 2 == 1:
            middle_col = self.columns // 2
        #if number of columns is even 
        else:
            middle_col = (self.columns // 2) - 1
        fall = True 
        row_pos = 1
        a_faller = Vitamin(row_pos, middle_col, row_pos, middle_col+1, command_lst[1], command_lst[2], faller_state = self.FALLING)
        while (row_pos < self.rows-1) and fall:
            #check if there's something in the next position. If there is, set fall to false.
            if self.grid[row_pos+1][middle_col] != '   ' or self.grid[row_pos+1][middle_col+1] != '   ':
                fall = False
                break

            #put faller in current position
            self.grid[row_pos][middle_col] = f"[{command_lst[1]}"
            self.grid[row_pos][middle_col+1] = f"--{command_lst[2]}]"
            self.print_grid()

            #clear faller in current position
            self.grid[row_pos][middle_col] = '   '
            self.grid[row_pos][middle_col+1] = '   '
            row_pos += 1
        
        #faller lands 
        self.grid[row_pos][middle_col] = f"|{command_lst[1]}"
        self.grid[row_pos][middle_col+1] = f"--{command_lst[2]}|"
        self.print_grid()
        a_faller.set_faller_state(self.LANDING)

        if row_pos == self.rows - 1:
            #faller freezes
            self.grid[row_pos][middle_col] = f" {command_lst[1]}"
            self.grid[row_pos][middle_col+1] = f"--{command_lst[2]} "
            self.print_grid()
            a_faller.set_faller_state(self.FREEZING)
        
        self.faller_lst.append(a_faller)
        a_faller.set_faller_position(row_pos, middle_col, row_pos, middle_col+1) 

    def matches(self):
        num_of_matched_rows = 1
        num_of_matched_columns = 1
        for row in range(self.rows):
            for column in range (self.columns):
                if self.grid[row][column] != '   ':
                    print(f"CURRENT_ROW{row}")
                    print(f"CURRENT_COLUMN{column}")
                    color = self.grid[row][column].upper().strip()
                    print(f"CURRENT_COLOR{color}")
                    '''next_column = column + 1
                    while next_column < self.columns:
                        next_color = self.grid[row][next_column].upper()
                        if next_color == color:
                            next_column += 1
                            num_of_matched_columns += 1
                        else:
                            break
                    if num_of_matched_columns == 4:
                        pass'''
                    num_of_matched_rows = 1
                    next_row = row + 1
                    while next_row < self.rows:
                        next_color = self.grid[next_row][column].upper().strip()
                        if next_color == color:
                            next_row += 1
                            num_of_matched_rows += 1
                        else:
                            break
                    if num_of_matched_rows == 4:
                        for i in range(num_of_matched_rows):
                            self.grid[row-1+i][column] = f"*{self.grid[row-1+i][column]}*"
                        self.print_grid()
                        for i in range(num_of_matched_rows):
                            self.grid[row-1+i][column] = f"   "
                    break
        self.print_grid()
        
        
        '''for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING:
                break
        match_row, match_column = a_faller.get_faller_position
        for row in range(self.rows):
            column = 0
            while column < self.columns:
                #if'''


        #self.grid[][]
    
    def move_right(self):
        for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING or a_faller.get_faller_state() == self.FALLING:
                move_faller = a_faller
                break

        row, column, second_row, second_column= move_faller.get_faller_position()  
        if move_faller.get_direction() == 'vertical':
            shift_left_row = row
            shift_left_column = column + 1 
            shift_right_row = second_row
            shift_right_column = second_column + 1
            self.grid[shift_left_row][shift_left_column] = self.grid[row][column]
            self.grid[shift_right_row][shift_right_column] = self.grid[second_row][second_column]
            self.grid[row][column] = '   '
            self.grid[second_row][second_column] = '   '
        else:
            #add horizontal 
            pass
    
        a_faller.set_faller_position(shift_left_row, shift_left_column, shift_right_row, shift_right_column)
        self.print_grid()

    def rotate_faller_clockwise(self):
        rotate_faller  = None

        for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING or a_faller.get_faller_state() == self.FALLING:
                rotate_faller = a_faller
                break
                
        if not rotate_faller:
            return None
    
        #faller's colors switch and direction switches 
        rotate_row, rotate_column, second_row, second_column = rotate_faller.get_faller_position()  
        
        #self.grid[rotate_row][rotate_column] = LEFT CAPSULE
        #clear current cells before rotating 
        if rotate_faller.get_direction() == 'horizontal':
            old_left_capsule = self.grid[rotate_row][rotate_column]
            old_right_capsule = self.grid[second_row][second_column]
            new_left_row = rotate_row-1
            new_left_column = rotate_column
            new_right_row = rotate_row
            new_right_column = rotate_column
            #old left capsule position is equal to right capsule 
            self.grid[rotate_row][rotate_column] = f"|{old_right_capsule[2:]}"
            self.grid[rotate_row-1][rotate_column] = f"{old_left_capsule}|"
            #clear right capsule 
            self.grid[second_row][second_column] = '   '
            a_faller.set_direction('vertical')
            a_faller.set_faller_position(new_left_row, new_left_column, new_right_row, new_right_column)
            #may need right capsule's row and column

        elif rotate_faller.get_direction() == 'vertical': #TBD
            self.grid[rotate_row-1][rotate_column] = '   '
            self.grid[rotate_row][rotate_column] = '   '

        self.print_grid()



    def rotate_faller_counter_clockwise(self):
        rotate_faller  = None

        for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING or a_faller.get_faller_state() == self.FALLING:
                rotate_faller = a_faller
                break
                
        if not rotate_faller:
            return None
    
        #faller's colors switch and direction switches 
        rotate_row, rotate_column, second_row, second_column = rotate_faller.get_faller_position()  
        
        #self.grid[rotate_row][rotate_column] = LEFT CAPSULE
        #clear current cells before rotating 
        if rotate_faller.get_direction() == 'horizontal':
            '''left_capsule = self.grid[rotate_row][rotate_column]
            right_capsule = self.grid[second_row][second_column]
            new_right_capsule_row = rotate_row-1
            new_right_capsule_column = rotate_column
            new_left_capsule_row = rotate_row
            self.grid[new_right_capsule_row][new_right_capsule_column] = f"|{right_capsule[2:]}"
            self.grid[rotate_row][rotate_column] = f"{self.grid[rotate_row][rotate_column]}|"
            self.grid[second_row][second_column] = '   '
            a_faller.set_direction('vertical')
            a_faller.set_faller_position(rotate_row, rotate_column, rotate_row-1, rotate_column)
            #may need right capsule's row and column'''
            #only RIGHT capsule rotates 
            self.grid[rotate_row-1][rotate_column] = f"|{self.grid[rotate_row][rotate_column+1][2:]}"
            self.grid[rotate_row][rotate_column] = f"{self.grid[rotate_row][rotate_column]}|"
            self.grid[rotate_row][rotate_column+1] = '   '
            a_faller.set_direction('vertical')
            a_faller.set_faller_position(rotate_row, rotate_column, rotate_row-1, rotate_column)
            #may need right capsule's row and column

        elif rotate_faller.get_direction() == 'vertical': #TBD
            self.grid[rotate_row-1][rotate_column] = '   '
            self.grid[rotate_row][rotate_column] = '   '

        self.print_grid()

    def create_virus(self, command_lst):
        row = int(command_lst[1])
        column = int(command_lst[2])
        color = command_lst[3].lower()
        a_virus = Virus(row, column, color)
        self.virus_lst.append(a_virus)
        if self.grid[row][column] == '   ':
            self.grid[row][column] = f' {color} '
        self.print_grid()

        self.matches()
        
    def contains_virus(self):
        pass

    def print_grid(self):  
        for row in range(len(self.grid)):
            print('|', end='')
            columns = len(self.grid[0])
            for column in range(columns):
                print(f"{self.grid[row][column]}", end='')
            print('|')
        print(' '+ '-' * (columns * 3)  + ' ')
        if len(self.virus_lst) == 0:
            print("LEVEL CLEARED")


class Vitamin:
    def __init__(self, rows, columns, second_row, second_column, first_color, second_color, faller_state):
        self.rows = rows
        self.columns = columns
        self.second_row = second_row
        self.second_column = second_column
        self.first_color =  first_color
        self.second_color =  second_color
        self.faller_state = faller_state
        self.direction = 'horizontal'

    '''def rotate_clockwise(self):
        if self.direction == 'horizontal':
            self.direction = 'vertical'
            self.left_color, self.right_color = self.right_color, self.left_color

        else:
            self.direction = 'horizontal'
            self.left_color, self.right_color = self.right_color, self.left_color'''
    def get_direction(self):
        return self.direction
    
    def set_direction(self, direction):
        self.direction = direction

    def get_faller_state(self):
        return self.faller_state
    
    def set_faller_state(self, faller_state):
        self.faller_state = faller_state

    def get_first_color(self):
        return self.first_color
    
    def get_second_color(self):
        return self.second_color
    
    def get_faller_position(self):
        return self.rows, self.columns, self.second_row, self.second_column
    
    def set_faller_position(self, row, col, second_row, second_column):
        self.rows = row
        self.columns = col
        self.second_row = second_row
        self.second_column = second_column

class Virus:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color

    def get_virus_position(self):
        return self.row, self.column
    
    def set_virus_position(self, row, column):
        self.row = row
        self.column = column
    
    def get_virus_color(self):
        return self.color 

    
