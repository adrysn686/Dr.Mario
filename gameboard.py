class GameBoard:
    FALLING = 1
    LANDING = 2
    FREEZING = 3

    def __init__(self, rows, columns, row_list=None):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.virus_lst = []
        self.faller = None
        self.empty =  '   '
        self.gameover = False
        self.row_list = row_list
        self.board_matches = False
        self.connected_capsule_in_match = False
        self.gravity_happening = False

        #for empty
        if row_list is None:
            for _ in range(rows):
                row = []
                for column in range(columns):
                    row.append('   ')
                self.grid.append(row)
            self.print_grid()
        #for CONTENTS 
        else:
            for i in range(rows):
                row_lst = []
                for j in range(len(row_list[i])):
                    char = row_list[i][j]
                    if char in ['r','b','y']:
                        row = int(i)
                        column = int(j)
                        color = char
                        a_virus = Virus(row, column, color)
                        self.virus_lst.append(a_virus)
                    formatted = f" {char} "
                    row_lst.append(formatted)
                self.grid.append(row_lst)
            self.matches()
            if not self.board_matches:
                self.print_grid()

    
    def create_faller(self, command_lst):
        '''if self.gravity_happening:
            self.print_grid()
            return'''

        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if any(char in cell for char in['[', ']', '|']):
                    self.print_grid()
                    return
    
        #if number of columns is odd
        if self.columns % 2 == 1:
            middle_col = self.columns // 2
        #if number of columns is even 
        else:
            middle_col = (self.columns // 2) - 1
        fall = True 
        row_pos = 1
        self.faller = Vitamin(row_pos, middle_col, command_lst[1], command_lst[2], faller_state = self.FALLING)

        #game over scenario 
        if self.grid[row_pos][middle_col] != '   ' or self.grid[row_pos][middle_col+1] != '   ':
            #check if there is something under, if so, set it to landing 
            if self.grid[row_pos+1][middle_col] != '   ' or self.grid[row_pos+1][middle_col+1] != '   ':
                self.grid[row_pos][middle_col] = f"|{command_lst[1]}-"
                self.grid[row_pos][middle_col+1] = f"-{command_lst[2]}|"
                self.faller.faller_state = self.LANDING
            #there isn't something under, so falling state
            else:
                self.grid[row_pos][middle_col] = f"[{command_lst[1]}-"
                self.grid[row_pos][middle_col+1] = f"-{command_lst[2]}]"
            self.gameover = True
            self.print_grid()
            print("GAME OVER")
            return
        
        #landing since there's something under 
        elif self.grid[row_pos+1][middle_col] != '   ' or self.grid[row_pos+1][middle_col+1] != '   ':
            self.grid[row_pos][middle_col] = f"|{command_lst[1]}-"
            self.grid[row_pos][middle_col+1] = f"-{command_lst[2]}|"
            self.faller.faller_state = self.LANDING
            self.print_grid()

        #create regular faller that is falling 
        else:
            #put faller in current position
            self.grid[row_pos][middle_col] = f"[{command_lst[1]}-"
            self.grid[row_pos][middle_col+1] = f"-{command_lst[2]}]"
            self.print_grid()


    def time(self):
        #when faller is frozen
        if self.faller is None:
            #check matches first
            if (self.board_matches is True) or (not self.is_board_frozen()):
                if self.connected_capsule_in_match is True:
                    #if there's a connected capsule, print the grid first
                    self.print_grid()
                    self.connected_capsule_in_match = False
                else:
                    #apply gravity if matches is true 
                    #self.board_matches stays true until everything everything is frozen. 
                    self.gravity()
            else:
                #if there's no match and no faller, just print the grid again
                self.print_grid()
    
            if self.is_board_empty():
                #if there's nothing on the board just print it 
                self.print_grid()
            elif self.is_board_frozen():
                #if everything on the board is frozen, then apply matching again. This is when self.board_matches can be changed. (gravity will be called again in the next time interval)
                self.matches()
        
        #when faller is falling/landing (no matching occurs)
        else:    
            #if horizontal 
            if self.faller.direction == 'horizontal':
                curr_row = self.faller.row
                curr_col = self.faller.column

                left_capsule = self.grid[curr_row][curr_col]
                right_capsule = self.grid[curr_row][curr_col+1]

                if curr_row < self.rows-1:
                    #checking if during falling it's going to land on the last row OR if there's something under. If so, change state to landing 
                    if self.grid[curr_row+1][curr_col] == '   ' and self.grid[curr_row+1][curr_col+1] == '   ' and self.faller.faller_state == self.FALLING and (curr_row+1 == self.rows-1 or (self.grid[curr_row+2][curr_col] != '   ' or self.grid[curr_row+2][curr_col+1] != '   ')):
                        #print('g00')
                        self.grid[curr_row+1][curr_col] = f"|{left_capsule[1:]}"
                        self.grid[curr_row+1][curr_col+1] = f"{right_capsule[:-1]}|"
                        self.faller.set_faller_position(curr_row+1, curr_col)
                        self.faller.faller_state = self.LANDING

                        #clear old position
                        self.grid[curr_row][curr_col] = '   '
                        self.grid[curr_row][curr_col+1] = '   '

                    #place capsules in new positions 
                    elif self.grid[curr_row+1][curr_col] == '   ' and self.grid[curr_row+1][curr_col+1] == '   ' and self.faller.faller_state == self.FALLING:
                        #print('g100')
                        self.grid[curr_row+1][curr_col] = left_capsule
                        self.grid[curr_row+1][curr_col+1] = right_capsule
                        self.faller.set_faller_position(curr_row+1, curr_col)

                        #clear old position
                        self.grid[curr_row][curr_col] = '   '
                        self.grid[curr_row][curr_col+1] = '   '
                    
                    
                    #change faller state to landing if something is under 
                    elif (self.grid[curr_row+1][curr_col] != '   ' or self.grid[curr_row+1][curr_col+1] != '   ') and self.faller.faller_state == self.FALLING:
                        #print('g200')
                        self.grid[curr_row][curr_col] = f"|{left_capsule[1:]}"
                        self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]}|"

                        self.faller.faller_state = self.LANDING
                    
                    #faller changes from landing to freezing 
                    elif (self.grid[curr_row+1][curr_col] != '   ' or self.grid[curr_row+1][curr_col+1] != '   ') and self.faller.faller_state == self.LANDING:
                        #print('g300')
                        self.grid[curr_row][curr_col] = f" {left_capsule[1:]}"
                        self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]} "

                        self.faller.faller_state = self.FREEZING
                        self.faller = None
                        self.matches()
                #this is when faller is in the last row 
                elif curr_row == self.rows-1:
                    if self.faller.faller_state == self.FALLING:
                        #print('g400')
                        self.grid[curr_row][curr_col] = f"|{left_capsule[1:]}"
                        self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]}|"

                        self.faller.faller_state = self.LANDING
                    elif self.faller.faller_state == self.LANDING:
                        #print('g500')
                        self.grid[curr_row][curr_col] = f" {left_capsule[1:]}"
                        self.grid[curr_row][curr_col+1] = f"{right_capsule[:-1]} "

                        self.faller.faller_state = self.FREEZING
                        self.faller = None
                        self.matches()
                else:
                    return
                
            
            #curr_row = self.faller.row
            #curr_col = self.faller.column
            elif self.faller.direction == 'vertical':
                curr_row = self.faller.top_row
                curr_col = self.faller.column

                top_capsule = self.grid[curr_row][curr_col]
                bottom_capsule = self.grid[curr_row+1][curr_col]

                if curr_row < self.rows-2:
                    #check if next capsule after bottom is empty to move it DOWN
                    if self.grid[curr_row+2][curr_col] == '   ' and self.faller.faller_state == self.FALLING:
                        #clear old position
                        self.grid[curr_row][curr_col] = '   '
                        self.grid[curr_row+1][curr_col] = '   '

                        if curr_row < self.rows-3:
                            if self.grid[curr_row+3][curr_col] == '   ':
                                #place capsules in new positions (STAYS FALLING STATE)
                                self.grid[curr_row+1][curr_col] = top_capsule
                                self.grid[curr_row+2][curr_col] = bottom_capsule
                                self.faller.set_faller_vertical_position(curr_row+1, curr_col)
                    
                            else:
                                #place capsules in new positions (CHANGES TO LANDING)
                                self.grid[curr_row+1][curr_col] = f"|{top_capsule[1]}|"
                                self.grid[curr_row+2][curr_col] = f"|{bottom_capsule[1]}|"
                                self.faller.set_faller_vertical_position(curr_row+1, curr_col)
                                self.faller.faller_state = self.LANDING
                    
                    #change faller state to landing if something is under 
                    elif (self.grid[curr_row+2][curr_col] != '   ') and self.faller.faller_state == self.FALLING:
                        self.grid[curr_row][curr_col] = f"|{top_capsule[1]}|"
                        self.grid[curr_row+1][curr_col] = f"|{bottom_capsule[1]}|"
                        #self.faller.set_faller_position(curr_row, curr_col)
                        self.faller.faller_state = self.LANDING
                    
                    #faller changes from landing to freezing 
                    elif (self.grid[curr_row+2][curr_col] != '   ') and self.faller.faller_state == self.LANDING:
                        print(f"TOP: {top_capsule[1]}")
                        print(f"BOTTOM: {bottom_capsule[1]}")
                        self.grid[curr_row][curr_col] = f" {top_capsule[1]} "
                        self.grid[curr_row+1][curr_col] = f" {bottom_capsule[1]} "

                        self.faller.faller_state = self.FREEZING
                        self.faller = None
                        self.matches()
        
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
                        self.faller = None
                        self.matches()
                else:
                    return
            if not self.board_matches:
                self.print_grid()
                
 
    def gravity(self):
        isGravity = False
        for row in range(self.rows-2, -1, -1):
            for column in range(self.columns):
                current_cell = self.grid[row][column].strip()
                if current_cell == '   ':
                    continue
                elif '-' in current_cell:
                    current_row = row
                    if (current_row < self.rows - 1 and
                        column + 1 < self.columns and
                        self.grid[current_row + 1][column] == '   ' and
                        self.grid[current_row + 1][column + 1] == '   '):
                        self.grid[current_row + 1][column] = f" {current_cell} "
                        self.grid[current_row + 1][column + 1] = f" {self.grid[row][column + 1]} "
                        self.grid[current_row][column] = '   '
                        self.grid[current_row][column + 1] = '   '
                        isGravity = True

                elif current_cell in ['R', 'B', 'Y']:
                    current_row = row
                    if self.grid[current_row + 1][column] == '   ':
                        self.grid[current_row + 1][column] = f" {current_cell} "
                        self.grid[current_row][column] = '   '
                        isGravity = True
        if isGravity:
            self.print_grid()
        self.gravity_happening = isGravity

    def is_board_empty(self):
        isEmpty = False
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if cell.strip() != '':
                    isEmpty = False
                    return isEmpty
                else:
                    isEmpty = True
        return isEmpty

    
    def is_board_frozen(self):
        all_frozen = False
        copy_grid = [row[:] for row in self.grid]
        isGravity = False
        for row in range(self.rows-2, -1, -1):
            for column in range(self.columns):
                current_cell = self.grid[row][column].strip()
                if current_cell == '   ':
                    continue
                elif '-' in current_cell:
                    current_row = row
                    if (current_row < self.rows - 1 and
                        column + 1 < self.columns and
                        copy_grid[current_row + 1][column] == '   ' and
                        copy_grid[current_row + 1][column + 1] == '   '):
                        copy_grid[current_row + 1][column] = f" {current_cell} "
                        copy_grid[current_row + 1][column + 1] = f" {copy_grid[row][column + 1]} "
                        copy_grid[current_row][column] = '   '
                        copy_grid[current_row][column + 1] = '   '
                        isGravity = True

                elif current_cell in ['R', 'B', 'Y']:
                    current_row = row
                    if copy_grid[current_row + 1][column] == '   ':
                        copy_grid[current_row + 1][column] = f" {current_cell} "
                        copy_grid[current_row][column] = '   '
                        isGravity = True
        if copy_grid == self.grid:
            all_frozen = True
        return all_frozen

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
        isMatch = False
        isConnected = False
        matches = set()
        #horizontal match
        for row in range(self.rows):
            for column in range (self.columns-3):
                if (self.grid[row][column] != '   ' and "[" not in self.grid[row][column]):
                    first = self.grid[row][column].upper().replace('-', '').strip()
                    second = self.grid[row][column+1].upper().replace('-', '').strip()
                    third = self.grid[row][column+2].upper().replace('-', '').strip()
                    fourth = self.grid[row][column+3].upper().replace('-', '').strip()
                    if (first == second == third == fourth):
                        matches.update([(row, column), (row, column+1), (row, column+2), (row, column+3)])
                        isMatch = True
       
        #vertical match
        for column in range(self.columns):
            for row in range (self.rows-3):
                if (self.grid[row][column] != '   ' and "[" not in self.grid[row][column]):
                    first = self.grid[row][column].upper().replace('-', '').strip()
                    second = self.grid[row+1][column].upper().replace('-', '').strip()
                    third = self.grid[row+2][column].upper().replace('-', '').strip()
                    fourth = self.grid[row+3][column].upper().replace('-', '').strip()
                    if (first == second == third == fourth):
                        matches.update([(row, column), (row+1, column), (row+2, column), (row+3, column)])
                        isMatch = True
        #clear matches 
        for row, column in matches:
            if '-' in self.grid[row][column]:
                    self.grid[row][column] = self.grid[row][column].replace('-', '').strip()
            self.grid[row][column] = f"*{self.grid[row][column].strip()}*"
        if isMatch is True:
            #print('match1')
            self.print_grid()
            
        for row, column in matches:
            if column+1 < self.columns:
                #if the cell next to the ones after matching have '-' in it, 
                #we know it's a double capsule that changes to a single capsule
                if '-' in self.grid[row][column+1]:
                    #print('match2')
                    self.grid[row][column+1] = self.grid[row][column+1].upper().replace('-', ' ')
                    isConnected = True 
    
            self.grid[row][column] = '   '
            for virus in self.virus_lst:
                if virus.row == row and virus.column == column:
                    virus.is_remove = True
    
        self.board_matches = isMatch
        self.connected_capsule_in_match  = isConnected

        
        #remove viruses from virus list 
        i = 0
        while i < len(self.virus_lst):
            if self.virus_lst[i].is_remove:
                del self.virus_lst[i]
            else:
                i += 1
        #return isMatch
        #self.gravity()


    def create_virus(self, command_lst):
        if self.gravity_happening:
            self.print_grid()
            return
        row = int(command_lst[1])
        column = int(command_lst[2])
        color = command_lst[3].lower()
        a_virus = Virus(row, column, color)
        self.virus_lst.append(a_virus)
        if self.grid[row][column] == '   ':
            self.grid[row][column] = f' {color} '
        if not self.matches():
            self.print_grid()


    def print_grid(self):  
        for row in range(len(self.grid)):
            print('|', end='')
            columns = len(self.grid[0])
            for column in range(columns):
                print(f"{self.grid[row][column]}", end='')
            print('|')
        print(' '+ '-' * (columns * 3)  + ' ')
        if len(self.virus_lst) == 0 and self.gameover is False:
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
        grid_column = len(grid[0])
        if self.direction == 'vertical':
            new_column = self.column + 1
            top_capsule = grid[self.top_row][self.column]
            bottom_capsule = grid[self.top_row + 1][self.column]
            if new_column < grid_column:
                #if there's something under the lower capsule after moving, change faller state.
                if grid[self.top_row + 2][new_column] != '   ':
                    if self.faller_state == 1:
                        grid[self.top_row][new_column] = f"|{top_capsule[1]}|"
                        grid[self.top_row + 1][new_column] = f"|{bottom_capsule[1]}|"
                        grid[self.top_row][self.column] = '   '
                        grid[self.top_row + 1][self.column] = '   '
                    elif self.faller_state == 2:
                        grid[self.top_row][new_column] = f" {top_capsule[1]} "
                        grid[self.top_row + 1][new_column] = f" {bottom_capsule[1]} "
                        grid[self.top_row][self.column] = '   '
                        grid[self.top_row + 1][self.column] = '   '
                else:
                    #if there's nothing under lower capsule after moving, faller state remains the same. 
                    #move right 
                    grid[self.top_row][new_column] = grid[self.top_row][self.column]
                    grid[self.top_row + 1][new_column] = grid[self.top_row + 1][self.column]
                    grid[self.top_row][self.column] = '   '
                    grid[self.top_row + 1][self.column] = '   '
                
                #not sure if this should be placed here 
                self.column = new_column
            else:
                return
        elif self.direction == 'horizontal':
            new_left_column = self.column + 1
            new_right_column = self.column + 2
            
            if new_right_column < grid_column:
                left_capsule = grid[self.row][self.column]
                right_capsule = grid[self.row][self.column+1]
                print(left_capsule)
                print(right_capsule)
                #if there's something under after moving, change faller state 
                if grid[self.row+1][new_left_column] != '   ' or grid[self.row+1][new_right_column] != '   ':
                    # if it's currently in falling state, change it to landing 
                    if self.faller_state == 1:
                        grid[self.row][new_left_column] = f"|{left_capsule[1:]}"
                        grid[self.row][new_right_column] = f"{right_capsule[:-1]}|"
                        grid[self.row][self.column] = '   '
                    #it's in landing state, change it to freezing 
                    elif self.faller_state == 2:
                        grid[self.row][new_left_column] = f" {left_capsule[1:]}"
                        grid[self.row][new_right_column] = f"{right_capsule[:-1]} "
                        grid[self.row][self.column] = '   '
                #if there's nothing under, so faller state remains the same 
                else:
                    grid[self.row][new_left_column] = left_capsule
                    grid[self.row][new_right_column] = right_capsule
                    grid[self.row][self.column] = '   '

                #not sure if this should be placed here 
                self.column = new_left_column
            else:
                return
    
    def move_left(self, grid):

        grid_column = len(grid[0])

        if self.direction == 'vertical':
            new_column = self.column - 1
            if new_column >= 0:
                #move left 
                grid[self.top_row][new_column] = grid[self.top_row][self.column]
                grid[self.top_row + 1][new_column] = grid[self.top_row + 1][self.column]
                grid[self.top_row][self.column] = '   '
                grid[self.top_row + 1][self.column] = '   '
                
                self.column = new_column
            else:
                return
        
        elif self.direction == 'horizontal':
            new_left_column = self.column - 1
            new_right_column = self.column

            if new_left_column >= 0:
                left_capsule = grid[self.row][self.column]
                right_capsule = grid[self.row][self.column+1]

                grid[self.row][new_left_column] = left_capsule
                grid[self.row][new_right_column] = right_capsule
        
                grid[self.row][self.column+1] = '   '

                self.column = new_left_column
            else:
                return


    def get_direction(self):
        return self.direction
    
    def set_direction(self, direction):
        self.direction = direction
   
    def get_faller_position(self):
        return self.row, self.column
    
    def get_faller_vertical_position(self):
        return self.top_row, self.column
    
    # only use this method when using outside of class 
    def set_faller_position(self, row, col):
        self.row = row
        self.column = col

    def set_faller_vertical_position(self, row, col):
        self.top_row = row
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
                grid[self.row][self.column] = f"[{right_content[1]}]"
            
            elif self.faller_state == 2:
                new_top_row = self.row -1
                #left changes to top 
                grid[new_top_row][self.column] = f"|{left_content[1]}|"
                #left changes to bottom 
                grid[self.row][self.column] = f"|{right_content[1]}|"

            self.direction = 'vertical'
            #self.row = new_top_row
            self.top_row = new_top_row
            
        elif self.direction == 'vertical':
            #check if bottom right cell is empty. IF NOT, apply wall kick
            if grid[self.top_row + 1][self.column+1] != '   ':
                #check if able to move left for wall kick
                if grid[self.top_row + 1][self.column-1] == '   ':
                    top_content = grid[self.top_row][self.column]
                    bottom_content = grid[self.top_row + 1][self.column]
                    #clear position
                    grid[self.top_row][self.column] = '   '
                
                    new_right_column = self.column
                    new_left_column = self.column - 1
                    if self.faller_state == 1:
                        grid[self.top_row+1][new_left_column] = f"[{bottom_content[1]}-"
                        grid[self.top_row+1][new_right_column] = f"-{top_content[1]}]"
                    else: #it's landing
                        grid[self.top_row+1][new_left_column] = f"|{bottom_content[1]}-"
                        grid[self.top_row+1][new_right_column] = f"-{top_content[1]}|"

                    self.direction = 'horizontal'
                    self.column = new_left_column
                else:
                    #this is when wall kick should be applied but there's something on the left, so do nothing
                    return 
            else: #vertical and no wall kick 
                top_content = grid[self.top_row][self.column]
                bottom_content = grid[self.top_row + 1][self.column]
                #clear position
                grid[self.top_row][self.column] = '   '
            
                new_right_column = self.column +1
                if self.faller_state == 1:
                    grid[self.top_row+1][self.column] = f"[{bottom_content[1]}-"
                    grid[self.top_row+1][new_right_column] = f"-{top_content[1]}]"
                else: #it's landing
                    grid[self.top_row+1][self.column] = f"|{bottom_content[1]}-"
                    grid[self.top_row+1][new_right_column] = f"-{top_content[1]}|"

                self.direction = 'horizontal'


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
                grid[new_top_row][self.column] = f"[{right_content[1]}]"
                #left changes to bottom 
                grid[self.row][self.column] = f"[{left_content[1]}]"
            
            elif self.faller_state == 2:
                #right changes to top 
                grid[new_top_row][self.column] = f"|{right_content[1]}|"
                #left changes to bottom 
                grid[self.row][self.column] = f"|{left_content[1]}|"

            self.direction = 'vertical'

        elif self.direction == 'vertical':
            #check if bottom right cell is empty. IF NOT, apply wall kick
            if grid[self.top_row + 1][self.column+1] != '   ':
                #check if able to move left for wall kick
                if grid[self.top_row + 1][self.column-1] == '   ':
                    top_content = grid[self.top_row][self.column]
                    bottom_content = grid[self.top_row + 1][self.column]
                    #clear position
                    grid[self.top_row][self.column] = '   '
                
                    new_right_column = self.column
                    new_left_column = self.column - 1
                    if self.faller_state == 1:
                        grid[self.top_row+1][new_right_column] = f"-{bottom_content[1]}]"
                        grid[self.top_row+1][new_left_column] = f"[{top_content[1]}-"
                    else: #it's landing
                        grid[self.top_row+1][new_right_column] = f"-{bottom_content[1]}|"
                        grid[self.top_row+1][new_left_column] = f"|{top_content[1]}-"
                    
                    self.column = new_left_column

                    self.direction = 'horizontal'

                    #self.row = self.top_row+ 1
                else:
                    #this is when wall kick should be applied but there's something on the left, so do nothing
                    return 
            else: #vertical and no wall kick
                top_content = grid[self.top_row][self.column]
                bottom_content = grid[self.top_row + 1][self.column]

                #clear position
                grid[self.top_row][self.column] = '   '
            
                new_right_column = self.column +1
                if self.faller_state == 1:
                    grid[self.top_row + 1][new_right_column] = f"-{bottom_content[1]}]"
                    grid[self.top_row + 1][self.column] = f"[{top_content[1]}-"
                else: #it's landing
                    grid[self.top_row + 1][new_right_column] = f"-{bottom_content[1]}|"
                    grid[self.top_row + 1][self.column] = f"|{top_content[1]}-"

                self.direction = 'horizontal'

class Virus:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.is_remove = False
