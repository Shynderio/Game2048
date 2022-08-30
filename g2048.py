from cgi import print_form
import discord
import random
import asyncio
import cv2
import numpy as np
from PIL import Image
import copy


num_of_rows = 4
num_of_cols = 4
empty_square = ':white_large_square:'
blue_square = ':blue_square:'
brown_square = ':brown_square:'
orange_square = ':orange_square:'
yellow_square = ':yellow_square:'
green_square = ':green_square:'
purple_square = ':purple_square:'
red_square = ':red_square:'
embed_colour = 0x077ff7 #colour of line on embeds
# board = [] 

def make_empty_board():
    board = []
    for row in range(num_of_rows):
        board.append([])
        for col in range(num_of_cols):
            board[row].append(0)
    return board


def print_board(boar):
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            boar[row][col] = 0
 

def to_string(board):
    s=''
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            s = s + str(board[row][col]) + ' ' 
        s += '\n'
    return s

def add_two(board):

    a = []
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            if (board[row][col] == 0):
                a.append(row*4 + col)
    rannum = random.randint(0,len(a) - 1)
    
    board[int(a[rannum]/4)][int(a[rannum]%4)] = 2
    
    # board[2][3] = 4
    

def merge_board(board):
    for row in range(num_of_rows):
        for col in range(num_of_cols - 1):
            if (board[row][col] == board[row][col + 1] and board[row][col] != 0):
                board[row][col] *= 2
                board[row][col + 1] = 0
    return board

                    
def move_board(board):
    row = 0
    while (row < num_of_rows):
        col = 0
        while (col < num_of_cols - 1):
            if (board[row][col] ==0 and board[row][col + 1] != 0):
                board[row][col] = board[row][col + 1]
                board[row][col + 1] = 0
                if (col != 0):
                    col -= 2
            col += 1
        row += 1

def rotate_board(arr):
    np.rot90(arr, k = 1, axes = (0,1))

          

def left(board):
    board
    move_board(board)
    merge_board(board)
    move_board(board)
    
    return board

def right(board):
    a = np.rot90(board, 2)
    move_board(a)
    merge_board(a)
    move_board(a)
    
    return np.rot90(a, 2)
    
def down(board):
    a = np.rot90(board, 3)
    move_board(a)
    merge_board(a)
    move_board(a)
    
    return np.rot90(a, 1)
    
def up(board):
    a = np.rot90(board, 1)
    move_board(a)
    merge_board(a)
    move_board(a)
    
    return np.rot90(a, 3)

def to_png(n):
    string = 'Numbers/' + str(n) + '.png'
    return string

def convert_toimg(k):
    board = copy.deepcopy(k)
    list = []
    newimg = Image.new('RGB', (800, 800))
    for i in range(4):
        list.append([to_png(img) for img in board[i]])
    for i in range(4):
        for j in range(4):
            im = Image.open(list[i][j])
            newimg.paste(im, (j*200,i*200))
    return newimg

