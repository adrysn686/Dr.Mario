class Field:
    FALLING = 1
    LANDING = 2
    FREEZING = 3

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.faller_lst = []
    
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
        a_faller = Faller(row_pos, middle_col, row_pos, middle_col+1, command_lst[1], command_lst[2], faller_state = self.FALLING)
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
        a_faller.set_faller_position(row_pos, middle_col) 

    def matches(self):
        pass
    
    def move_right(self):
        for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING or a_faller.get_faller_state() == self.FALLING:
                move_faller = a_faller
                break

        row, column = move_faller.get_faller_position()  
        if move_faller.get_direction() == 'vertical':
            shift_row = row
            shift_column = column + 1 
            self.grid[shift_row][shift_column] = self.grid[row][column]
            self.grid[shift_row-1][shift_column] = self.grid[row-1][column]
            self.grid[row][column] = '   '
            self.grid[row-1][column] = '   '
        else:
            #add horizontal 
            pass
    
        a_faller.set_faller_position(shift_row, shift_column)
        self.print_grid()
    
    def rotate_faller(self):
        rotate_faller  = None

        for a_faller in self.faller_lst:
            if a_faller.get_faller_state() == self.LANDING or a_faller.get_faller_state() == self.FALLING:
                rotate_faller = a_faller
                break
                
        if not rotate_faller:
            return None
    
        #faller's colors switch and direction switches 
        rotate_row, rotate_column = rotate_faller.get_faller_position()  
        
        '''for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                 # If the cell contains part of a faller, clear it
                if cell.startswith('|') or cell.startswith('['):
                    self.grid[row][column] = '   '
        rotate_faller.rotate_clockwise()'''
        #self.grid[rotate_row][rotate_column] = LEFT CAPSULE
        #clear current cells before rotating 
        if rotate_faller.get_direction() == 'horizontal':
            #only RIGHT capsule rotates 
            self.grid[rotate_row-1][rotate_column] = f"|{self.grid[rotate_row][rotate_column+1][2:]}"
            self.grid[rotate_row][rotate_column] = f"{self.grid[rotate_row][rotate_column]}|"
            self.grid[rotate_row][rotate_column+1] = '   '
            a_faller.set_direction('vertical')
            a_faller.set_faller_position(rotate_row, rotate_column)
            #may need right capsule's row and column

        elif rotate_faller.get_direction() == 'vertical': #TBD
            self.grid[rotate_row-1][rotate_column] = '   '
            self.grid[rotate_row][rotate_column] = '   '

        self.print_grid()

        '''#row and column after rotation
        after_row, after_col = rotate_faller.get_faller_position()

        if rotate_faller.direction == 'horizontal':
            if after_col + 1 < self.columns:
                self.grid[after_row][after_col] = f"|{rotate_faller.left_color}--"
                self.grid[after_row][after_col+1] = f"{rotate_faller.right_color}|"
        
        elif rotate_faller.direction == 'vertical':
            self.grid[after_row-1][after_col] = f"|{rotate_faller.right_color}|"
            self.grid[after_row][after_col] = f"|{rotate_faller.left_color}|"
        
        self.print_grid()
        #if 2 columns are equivalent then they are vertical --> change to horizontal
        #else: they are horizontal --> change to vertical '''
        '''for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]'''

        '''faller_cell = {}
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if "|" in cell:
                    faller_cell[cell] = [row, column]
        #if 2 columns are equivalent then they are vertical --> change to horizontal
        #else: they are horizontal --> change to vertical 
        
        #rotate clockwise
        self.grid[row_pos-1][middle] = self.grid[row_pos][middle+1]'''

    def contains_virus(self):
        pass

    def print_grid(self):  
        for row in range(len(self.grid)):
            print('|', end='')
            columns = len(self.grid[0])
            for column in range(columns):
                print(f"{self.grid[row][column]}", end='')
            print('|')
        print(' '+ '-' * (columns * 3))


class Faller:
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
        return self.rows, self.columns
    
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
        self.color = color 

    
