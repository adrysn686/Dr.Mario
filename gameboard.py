class GameBoard:
    FALLING = 1
    LANDING = 2
    FREEZING = 3

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.virus_lst = []
        self.faller = None
        self.empty =  '   '
    
        for row in range(rows):
            row = []
            for column in range(columns):
                row.append('   ')
            self.grid.append(row)

    def create_faller(self, command_lst):
         #if number of columns is odd
        if self.columns % 2 == 1:
            middle_col = self.columns // 2
        #if number of columns is even 
        else:
            middle_col = (self.columns // 2) - 1
        fall = True 
        row_pos = 1
        self.faller = Vitamin(row_pos, middle_col, command_lst[1], command_lst[2], faller_state = self.FALLING)

        if self.grid[row_pos][middle_col] != '   ' or self.grid[row_pos][middle_col+1] != '   ':
            print("GAME OVER")
            return
        
        #put faller in current position
        self.grid[row_pos][middle_col] = f"[{command_lst[1]}"
        self.grid[row_pos][middle_col+1] = f"--{command_lst[2]}]"
        self.print_grid()
        
    def time(self):
        #if horizontal 
        if self.faller.direction == 'horizontal':
            curr_row = self.faller.row
            curr_col = self.faller.column

            left_capsule = self.grid[curr_row][curr_col]
            right_capsule = self.grid[curr_row][curr_col+1]

            if curr_row < self.rows-1:
                #place capsules in new positions 
                if self.grid[curr_row+1][curr_col] == '   ' and self.grid[curr_row+1][curr_col+1] == '   ' and self.faller.faller_state == self.FALLING:
                    self.grid[curr_row+1][curr_col] = left_capsule
                    self.grid[curr_row+1][curr_col+1] = right_capsule
                    self.faller.set_faller_position(curr_row+1, curr_col)

                    #clear old position
                    self.grid[curr_row][curr_col] = '   '
                    self.grid[curr_row][curr_col+1] = '   '
                
                #change faller state to landing if something is under 
                elif (self.grid[curr_row+1][curr_col] != '   ' or self.grid[curr_row+1][curr_col+1] != '   ') and self.faller.faller_state == self.FALLING:
                    self.grid[curr_row][curr_col] = f"|{left_capsule[1:]}"
                    self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]}|"

                    self.faller.faller_state = self.LANDING
                
                #faller changes from landing to freezing 
                elif (self.grid[curr_row+1][curr_col] != '   ' or self.grid[curr_row+1][curr_col+1] != '   ') and self.faller.faller_state == self.LANDING:
                    self.grid[curr_row][curr_col] = f" {left_capsule[1:]}"
                    self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]} "

                    self.faller.faller_state = self.FREEZING
            #this is when faller is in the last row 
            elif curr_row == self.rows-1:
                if self.faller.faller_state == self.FALLING:
                    self.grid[curr_row][curr_col] = f"|{left_capsule[1:]}"
                    self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]}|"

                    self.faller.faller_state = self.LANDING
                elif self.faller.faller_state == self.LANDING:
                    self.grid[curr_row][curr_col] = f" {left_capsule[1:]}"
                    self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]} "

                    self.faller.faller_state = self.FREEZING
            else:
                return
            self.print_grid()
        
        #curr_row = self.faller.row
        #curr_col = self.faller.column
        elif self.faller.direction == 'vertical':
            curr_row = self.faller.top_row
            curr_col = self.faller.column

            top_capsule = self.grid[curr_row][curr_col]
            bottom_capsule = self.grid[curr_row+1][curr_col]

            if curr_row < self.rows-2:
                #check if next capsule after bottom is empty 
                if self.grid[curr_row+2][curr_col] == '   ' and self.faller.faller_state == self.FALLING:
                    #clear old position
                    self.grid[curr_row][curr_col] = '   '
                    self.grid[curr_row+1][curr_col] = '   '

                     #place capsules in new positions 
                    self.grid[curr_row+1][curr_col] = top_capsule
                    self.grid[curr_row+2][curr_col] = bottom_capsule
                    self.faller.set_faller_position(curr_row+1, curr_col)
                
                #change faller state to landing if something is under 
                elif (self.grid[curr_row+2][curr_col] != '   ') and self.faller.faller_state == self.FALLING:
                    self.grid[curr_row][curr_col] = f"|{top_capsule[1]}|"
                    self.grid[curr_row+1][curr_col] = f"|{bottom_capsule[1]}|"

                    self.faller.faller_state = self.LANDING
                
                #faller changes from landing to freezing 
                elif (self.grid[curr_row+2][curr_col] != '   ') and self.faller.faller_state == self.LANDING:
                    self.grid[curr_row][curr_col] = f" {top_capsule[1]} "
                    self.grid[curr_row+1][curr_col] = f" {bottom_capsule[1]} "

                    self.faller.faller_state = self.FREEZING
            #this is when faller is in the last row 
            elif curr_row == self.rows-2:
                if self.faller.faller_state == self.FALLING:
                    self.grid[curr_row][curr_col] = f"|{top_capsule[1]}|"
                    self.grid[curr_row+1][curr_col] = f"|{bottom_capsule[1]}|"

                    self.faller.faller_state = self.LANDING
                elif self.faller.faller_state == self.LANDING:
                    self.grid[curr_row][curr_col] = f" {top_capsule[1]} "
                    self.grid[curr_row+1][curr_col] = f" {bottom_capsule[1]} "

                    self.faller.faller_state = self.FREEZING
            else:
                return
            self.print_grid()

    def gravity(self):
        #check for vitamin
        # if its empty, call time
        pass

    def rotate_gameboard_counter_clockwise(self):
        if self.faller.faller_state in [self.LANDING, self.FALLING]:
            self.faller.rotate_faller_counter_clockwise(self.grid)
        self.print_grid()

    def rotate_gameboard_clockwise(self):
        if self.faller.faller_state in [self.LANDING, self.FALLING]:
            self.faller.rotate_faller_clockwise(self.grid)
        self.print_grid()
    
    def move_right(self):
        if self.faller.faller_state in [self.LANDING, self.FALLING]:
            self.faller.move_right(self.grid)
        
        self.print_grid()

    def move_left(self):
        if self.faller.faller_state in [self.LANDING, self.FALLING]:
            self.faller.move_left(self.grid)
        self.print_grid()

    def matches(self):
        matches = set()

        #horizontal match
        for row in range(self.rows):
            for column in range (self.columns-3):
                if (self.grid[row][column] != '   ' and
                    self.grid[row][column] == self.grid[row][column+1]
                    == self.grid[row][column+2] == self.grid[row][column+3]): 
                    matches.update([(row, column), (row, column+1), (row, column+2), (row, column+3)])
       
        #vertical match
        for column in range(self.columns):
            for row in range (self.rows-3):
                if (self.grid[row][column] != '   ' and
                    self.grid[row][column] == self.grid[row+1][column] ==
                    self.grid[row+2][column] == self.grid[row+3][column]): 
                    matches.update([(row, column), (row+1, column), (row+2, column), (row+3, column)])
        #clear matches 
        for row, column in matches:
            self.grid[row][column] = '   '
            for virus in self.virus_lst:
                if virus.row == row and virus.column == column:
                    virus.is_remove = True
        #remove viruses from virus list 
        i = 0
        while i < len(self.virus_lst):
            if self.virus_lst[i].is_remove:
                del self.virus_lst[i]
            else:
                i += 1
        
        #self.gravity()

    def create_contents_board(self, input1, input2):
        pass

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
    def __init__(self, row, column, left_color, right_color, faller_state):
        self.row = row
        self.column = column
        self.top_row = row
        self.left_color =  left_color
        self.right_color =  right_color
        self.faller_state = faller_state
        self.direction = 'horizontal'

    def move_right(self, grid):
       
        if self.direction == 'vertical':
            new_column = self.column + 1
            
            #move right 
            grid[self.top_row][new_column] = grid[self.top_row][self.column]
            grid[self.top_row + 1][new_column] = grid[self.top_row + 1][self.column]
            grid[self.top_row][self.column] = '   '
            grid[self.top_row + 1][self.column] = '   '
            
            self.column = new_column
        
        elif self.direction == 'horizontal':
            new_left_column = self.column + 1
            new_right_column = self.column + 2

            left_capsule = grid[self.row][self.column]
            right_capsule = grid[self.row][self.column+1]

            grid[self.row][new_left_column] = left_capsule
            grid[self.row][new_right_column] = right_capsule
            grid[self.row][self.column] = '   '

            self.column = new_left_column
    
    def move_left(self, grid):

        if self.direction == 'vertical':
            new_column = self.column - 1
            
            #move right 
            grid[self.top_row][new_column] = grid[self.top_row][self.column]
            grid[self.top_row + 1][new_column] = grid[self.top_row + 1][self.column]
            grid[self.top_row][self.column] = '   '
            grid[self.top_row + 1][self.column] = '   '
            
            self.column = new_column
        
        elif self.direction == 'horizontal':
            new_left_column = self.column - 1
            new_right_column = self.column

            left_capsule = grid[self.row][self.column]
            right_capsule = grid[self.row][self.column+1]

            grid[self.row][new_left_column] = left_capsule
            grid[self.row][new_right_column] = right_capsule
    
            grid[self.row][self.column+1] = '   '

            self.column = new_left_column
    

    def get_direction(self):
        return self.direction
    
    def set_direction(self, direction):
        self.direction = direction
   
    def get_faller_position(self):
        return self.row, self.column
    
    # only use this method when using outside of class 
    def set_faller_position(self, row, col):
        self.row = row
        self.column = col       

    #wall kick only implemented in rotate faller clockwise so far
    def rotate_faller_clockwise(self, grid):
        
        if self.direction == 'horizontal':
            left_content = grid[self.row][self.column]
            right_content = grid[self.row][self.column + 1]
            
            #clear current position
            grid[self.row][self.column] = '   '
            grid[self.row][self.column+1] = '   '

            if self.faller_state == 1:
                new_top_row = self.row -1
                #left changes to top 
                grid[new_top_row][self.column] = f"[{left_content[1]}]"
                #left changes to bottom 
                grid[self.row][self.column] = f"[{right_content[2]}]"
            
            elif self.faller_state == 2:
                new_top_row = self.row -1
                #left changes to top 
                grid[new_top_row][self.column] = f"|{left_content[1]}|"
                #left changes to bottom 
                grid[self.row][self.column] = f"|{right_content[2]}|"

            self.direction = 'vertical'
            #self.row = new_top_row
            self.top_row = new_top_row
            
        elif self.direction == 'vertical':
            if grid[self.top_row + 1][self.column+1] != '   ':
                if grid[self.top_row + 1][self.column-1] == '   ':
                    self.move_left(grid)
                    top_content = grid[self.top_row][self.column]
                    bottom_content = grid[self.top_row + 1][self.column]
                    #clear position
                    grid[self.top_row][self.column] = '   '
                
                    new_right_column = self.column +1
                    if self.faller_state == 1:
                        grid[self.top_row+1][self.column] = f"[{bottom_content[1]}"
                        grid[self.top_row+1][new_right_column] = f"--{top_content[1]}]"
                    else: #it's landing
                        grid[self.top_row][self.column] = f"|{bottom_content[1]}"
                        grid[self.top_row][new_right_column] = f"--{top_content[1]}|"

                    self.direction = 'horizontal'

                    #self.row = self.row + 1
            else:
                top_content = grid[self.top_row][self.column]
                bottom_content = grid[self.top_row + 1][self.column]
                #clear position
                grid[self.top_row][self.column] = '   '
            
                new_right_column = self.column +1
                if self.faller_state == 1:
                    grid[self.top_row+1][self.column] = f"[{bottom_content[1]}"
                    grid[self.top_row+1][new_right_column] = f"--{top_content[1]}]"
                else: #it's landing
                    grid[self.top_row][self.column] = f"|{bottom_content[1]}"
                    grid[self.top_row][new_right_column] = f"--{top_content[1]}|"

                self.direction = 'horizontal'
                #self.row = self.row + 1


    def rotate_faller_counter_clockwise(self, grid):
        if self.direction == 'horizontal':
            left_content = grid[self.row][self.column]
            right_content = grid[self.row][self.column + 1]
            
            #clear current position
            grid[self.row][self.column+1] = '   '

            new_top_row = self.row -1
            self.top_row = new_top_row

            if self.faller_state == 1:
                #right changes to top 
                grid[new_top_row][self.column] = f"[{right_content[2]}]"
                #left changes to bottom 
                grid[self.row][self.column] = f"[{left_content[1]}]"
            
            elif self.faller_state == 2:
                #right changes to top 
                grid[new_top_row][self.column] = f"|{right_content[2]}|"
                #left changes to bottom 
                grid[self.row][self.column] = f"|{left_content[1]}|"

            self.direction = 'vertical'

        elif self.direction == 'vertical':
            top_content = grid[self.top_row][self.column]
            bottom_content = grid[self.top_row + 1][self.column]

            #clear position
            grid[self.top_row][self.column] = '   '
        
            new_right_column = self.column +1
            if self.faller_state == 1:
                grid[self.top_row + 1][new_right_column] = f"--{bottom_content[1]}]"
                grid[self.top_row + 1][self.column] = f"[{top_content[1]}"
            else: #it's landing
                grid[self.top_row + 1][new_right_column] = f"--{bottom_content[1]}|"
                grid[self.top_row + 1][self.column] = f"|{top_content[1]}"

            self.direction = 'horizontal'

class Virus:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.is_remove = False

    '''def get_virus_position(self):
        return self.row, self.column
    
    def set_virus_position(self, row, column):
        self.row = row
        self.column = column
    
    def get_virus_color(self):
        return self.color 

    def set_virus_state(self, is_remove):
        self.is_remove = is_remove
    
    def get_virus_state(self):
        return self.is_remove'''

