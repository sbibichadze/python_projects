#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time
import random


# In[2]:


# for x y coordinate check available moves in range 1-9 
def get_available_moves(board, x, y):
    result = {a for a in range(1, 10)}
    
    row_used = set(board[x])
    col_used = set(board[:, y])
    
    # need to get top-left point of a square in which x,y is
    i, j = x - x%3, y - y%3
    square_used = set(np.unique(board[i:i+3, j:j+3]))
    total_used = row_used | col_used | square_used
    
    return list(result - total_used)


# In[3]:


# increase column if its higher than board y_dim set it to 0 and increase x
def get_next_location(board, x, y):
    if y + 1 == board.shape[1]:
        return (x+1, 0)
    return (x, y+1)


# In[4]:


def solve(board, x=0, y=0):
    # board has been filled x went out of range
    if x == board.shape[0]:
        return True
    
    # get next move its already filled
    if board[x, y] != 0:
        nx, ny = get_next_location(board, x, y)
        return solve(board, nx, ny)
    else:
        avaliable_moves = get_available_moves(board, x, y)
        # if correct choice is 9 this will take too much time 
        ### so this should normalise time complexity
        random.shuffle(avaliable_moves)
        for move in avaliable_moves:
            # try move
            board[x, y] = move
            #if move was correct and is solvable return True
            if solve(board, x, y):
                return True
            # unmake move
            board[x, y] = 0
        return False


# In[5]:


def get_test_board(s):
    test = [list(s[i*9 : (i+1)*9]) for i in range(9)]
    test = [[int(test[i][j]) if test[i][j].isdigit() else 0 for j in range(9)] for i in range(9)]
    return np.array(test)


# In[6]:


def test_solver(board, solution):
    st = time.time()
    print(board)
    print('solving ...')
    s = solve(board)
    print(board)
    print('\nstats: ')
    print(f'Time : {(time.time() - st):.2f}s\n')
    assert s 
    print('solvable')
    assert solution == ''.join([''.join([str(elem) for elem in row]) for row in board])
    print('solution is correct')


# In[7]:


test1 = get_test_board('2564891733746159829817234565932748617128.6549468591327635147298127958634849362715')
test_solver(test1, '256489173374615982981723456593274861712836549468591327635147298127958634849362715')


# In[8]:


test2 = get_test_board('3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8')
test_solver(test2, '365427819487931526129856374852793641613248957974165283241389765538674192796512438')


# In[16]:


test3 = get_test_board('..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4..')
test_solver(test3, '672435198549178362831629547368951274917243856254867931193784625486592713725316489')


# In[10]:


test4 = get_test_board('9..1....4.14.3.8....3....9....7.8..18....3..........3..21....7...9.4.5..5...16..3')
test_solver(test4, '')


# In[ ]:


'.89.7..4.3...........1..2.......8..4.76.9..8..5.......5......6.4...3.....637....1'


# In[22]:


test5 = get_test_board('.89.7..4.3...........1..2.......8..4.76.9..8..5.......5......6.4...3.....637....1')
test_solver(test5, '')


# In[20]:


len('98.7.....7...6.9....5..9.7.5....6.8...4.3.6.....2....1.5...7.4....6....3....1.2..11.7')%81

