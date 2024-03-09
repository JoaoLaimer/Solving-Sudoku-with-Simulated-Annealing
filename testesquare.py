import sys
import os
import numpy
import math
import statistics 

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from module.create_matrix   import CreateMatrix     as CM
from module.display_matrix  import DisplayMatrix    as DM
from module.check_matrix    import CheckMatrix      as CKM
from save.save_sudoku       import SaveSudoku       as SAVE
import random
import time

SIZE = 9



def SelectRandomSudoku():
    file = open("sudokus\\sudoku_incomplete.txt", "r")
    count = 0
    for line in file:
        if line.startswith("Sudoku"):
            count += 1
    random_sudoku_id = random.randint(0, count - 1)
    file.close()
    return random_sudoku_id

def GetSudoku():
    sudoku_id = SelectRandomSudoku()
    file = open("sudokus\\sudoku_incomplete.txt", "r")
    sudoku = []
    for line in file:
        if line.startswith("Sudoku " + str(sudoku_id)):
            for i in range(9):
                row = file.readline()
                row = row.split() 
                row = [int(num) for num in row]  
                sudoku.append(row)
            break
    file.close()
    return sudoku

def SelectSquare(sudoku, random_square_row, random_square_column):

    square_numbers = []
    
    print("Selected Square: ")
    for row in range(random_square_row - 3, random_square_row):
        for column in range(random_square_column - 3, random_square_column):
            print(sudoku[row][column], end=" ")
            square_numbers.append((sudoku[row][column], row, column))
        print()
            
    return square_numbers

if __name__ == "__main__":
    inital_sudoku = GetSudoku()
    SelectSquare(inital_sudoku, 3, 3)
    SelectSquare(inital_sudoku, 3, 6)
    SelectSquare(inital_sudoku, 3, 9)

    SelectSquare(inital_sudoku, 6, 3)
    SelectSquare(inital_sudoku, 6, 6)
    SelectSquare(inital_sudoku, 6, 9)

    SelectSquare(inital_sudoku, 9, 3)
    SelectSquare(inital_sudoku, 9, 6)
    SelectSquare(inital_sudoku, 9, 9)