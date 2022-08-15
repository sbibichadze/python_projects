#!/usr/bin/env python
# coding: utf-8

# In[19]:


import random
import time 

class Minesweeper():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        
        # bombs should be 17% of board 
        self.bomb_count = 17*rows*columns // 100
        self.board = self.get_board()
        self.correct_count = 0
        self.game_finished = False
        self.start_time = time.time()
    
    
    # set up board for __init__ fun
    def get_board(self):
        board = [['_' for _ in range(self.columns)] for _ in range(self.rows)]
        cnt = self.bomb_count
        while cnt > 0:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.columns - 1)
            if board[x][y] == '_':
                board[x][y] = 'X'
                cnt -= 1
        
        return board 
    
    # returns number of bombs around the passed location
    # this function is only called for safe spots so no need to check if i,j == x,y (a.k start loc) for skip condition
    def get_bomb_count_in_neighbours(self, x, y):
        cnt = 0
        for i in range(max(x-1, 0), min(x+2, self.rows)):
            for j in range(max(y-1, 0), min(y+2, self.columns)):
                if self.board[i][j] == 'X':
                    cnt += 1
        return str(cnt)
    
    
    # returns status of the game after compleating user action - choosing (x, y) loc
    def action(self, x, y):
        # game lost wrong guess
        if self.board[x][y] == 'X':
            return -1
        elif self.board[x][y].isdigit():
            print('given location is already displayed')
            return 0
        
        # if player chose safe move we need to get neighbour bomb count for given location
        # if number of neighbour bombs are 0 we should call this function again for all neighbours 
        # after each call count of correct moves should be increased
        def wrapper(x, y):
            if self.board[x][y] == '_':
                self.board[x][y] = self.get_bomb_count_in_neighbours(x, y)
                self.correct_count += 1
                if self.board[x][y] == '0':
                    for i in range(max(x-1, 0), min(x+2, self.rows)):
                        for j in range(max(y-1, 0), min(y+2, self.columns)):
                            wrapper(i, j)
        # call wrapper
        wrapper(x, y)
        
        # 0 if game's still in progress if all spots are filled return 1 
        return int(self.correct_count + self.bomb_count == self.rows * self.columns)
    
    # return users valid input
    def get_user_input(self):
        try:
            x, y = input('>>>>> x:y - ').split(':')
            x = int(x)
            y = int(y)
            if x < 0 or x >= self.rows or y < 0 or y >= self.columns:
                raise
        except:
            print('Input is not valid')
            print('right format is: x:y')
            return None

        return (x, y)
    
    
    # pass ovr boolean to display full board if game ends
    def print_board(self, ovr = False):
        print('    ' + '   '.join([str(i) for i in range(self.columns)]) + '  ')
        if not ovr:
            for i, row in enumerate(self.board):
                print('   ' + '_' * 4 * (len(row)))
                print(str(i) + ' | ' + ' | '.join([x if x.isdigit() else ' ' for x in row]) + ' |')
        else:
            for i, row in enumerate(self.board):
                print('   ' + '_' * 4 * (len(row)))
                print(str(i) + ' | ' + ' | '.join([self.get_bomb_count_in_neighbours(i, j) if row[j] == '_' else row[j] for j in range(len(row))]) + ' |')
    
        print('   ' + '_' * 4 * (len(row)))
    
    def print_time(self):
        print(f'Time : {(time.time()-self.start_time):.2f}s')
    
    def __str__(self):
        return f"number of bombs left : {self.bomb_count}\nnumber of safe spots : {self.rows*self.columns - self.correct_count - self.bomb_count}"
                    


# In[20]:


def play():
    # get dimensions from player
    rows = 8
    columns = 8
    print('Enter x y dimensions space separated')
    print('min dim-size = 6 && max dim-size = 15')
    try:
        x, y = input('rows:columns - ').split(':')
        x = int(x)
        y = int(y)
        if x < 5 or x >= 15 or y < 5 or y >= 15:
                raise
        rows = x
        columns = y
    except:
        print('either type error or invalid dimensions')
        print('game will use default values 8x8 board')
    
    game = Minesweeper(rows, columns)
    print(game)
    game.print_board()
    
    while True:
        # get valid user input otw skip 
        print('>>> Enter safe location')
        user_input = game.get_user_input()
        if user_input is None:
            continue
        x, y = user_input
        # action display check exit condition
        finish_flg = game.action(x, y)
        
        if finish_flg == 0:
            print(game)
            game.print_board()
        else:
            game.print_board(True)
            game.print_time()
            if finish_flg == 1:
                print('congrats you win')
            else:
                print('you lose')
            break


# In[21]:


play()


# In[ ]:




