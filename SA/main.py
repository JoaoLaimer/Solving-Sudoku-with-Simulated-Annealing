import sys
import os
### ADICIONA O CAMINHO DO DIRETÓRIO (MODULE,PAI) AO PATH PRA CONSEGUIR IMPORTAR FUNCOES###
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

"""
SIMULATED ANNEALING
PASSOS:
1 - Generate a random solution
2 - Calculate the cost of the solution
3 - Generate a new solution
4 - Calculate the cost of the new solution
5 - Compare the cost of the new solution with the cost of the old solution

Cost function:
1 - Number of conflicts in the solution
2 - Number of empty cells in the solution
3 - Number of repeated numbers in the solution

6 - If the new solution is better than the old solution, accept the new solution
8 - Select a starting temperature
9 - Calculate iterations per temperature
10 - Select a cooling rate

Probability of accepting the new solution: 1/1+e^(new_cost - old_cost)/T
"""

def SelectRandomSudoku():
    file = open("sudoku_incomplete.txt", "r")
    count = 0
    for line in file:
        if line.startswith("Sudoku"):
            count += 1
    random_sudoku_id = random.randint(0, count - 1)
    file.close()
    return random_sudoku_id

def GetSudoku():
    sudoku_id = SelectRandomSudoku()
    file = open("sudoku_incomplete.txt", "r")
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

def RandomSolution(sudoku):
    sudoku_grid = [row[:] for row in sudoku]  
    for row in range(9):
        for column in range(9):
            if sudoku_grid[row][column] == 0:
                checker = CKM(9, sudoku_grid)
                number = random.randint(1, 9)
                while not checker.Check_Square(number, column, row, sudoku_grid):
                    number = random.randint(1, 9)
                sudoku_grid[row][column] = number
    return sudoku_grid

def RowCostFunction(sudoku):
    conflicts = 0
    checked_numbers = set()
    for row in range(9):
        checked_numbers.clear()
        for column in range(9):
            number = sudoku[row][column]
            for i in range (column, 9):
                if i != column and sudoku[row][i] == number and number not in checked_numbers:
                    conflicts += 1
                    checked_numbers.add(number)
    return conflicts

def ColumnCostFunction(sudoku):
    conflicts = 0
    checked_numbers = set()
    for column in range(9):
        checked_numbers.clear()
        for row in range(9):
            number = sudoku[row][column]
            for i in range (row, 9):
                if i != row and sudoku[i][column] == number and number not in checked_numbers:
                    """
                    print(f"Number {number} in row {row} and column {column} is repeated in row {i}")
                    """
                    conflicts += 1
                    checked_numbers.add(number)
    return conflicts

def SelectSquare(sudoku):
    random_square_row = random.choice([3, 6, 9])
    random_square_column = random.choice([3, 6, 9])
    square_numbers = []
    #"""
    print("Selected Square: ")
    for row in range(random_square_row - 3, random_square_row):
        for column in range(random_square_column - 3, random_square_column):
            print(sudoku[row][column], end =" ")
            square_numbers.append((sudoku[row][column], row, column))
        print()
    #"""
    return square_numbers

def GetNonFixedNumbers(square_numbers, initial_sudoku):
    fixed_numbers = []
    for i in range(len(square_numbers)):
        if initial_sudoku[square_numbers[i][1]][square_numbers[i][2]] != 0:
            fixed_numbers.append(square_numbers[i][0])
    
    not_fixed_numbers = []
    for numbers in square_numbers:
        if numbers[0] not in fixed_numbers:
            not_fixed_numbers.append(numbers)
    #""" 
    print("Square Numbers: ", square_numbers)
    print("Fixed Numbers: ", fixed_numbers)
    print("Not fixed numbers: ", not_fixed_numbers)
    #"""
    return not_fixed_numbers

def ChangePlace( non_fixed_numbers, sudoku ):
    new_sudoku = [row[:] for row in sudoku]
    random_index_1 = random.randint( 0, len( non_fixed_numbers ) - 1)
    random_number_1 = non_fixed_numbers[ random_index_1 ][ 0 ]
    random_number_1_row     = non_fixed_numbers[ random_index_1 ][ 1 ]
    random_number_1_column  = non_fixed_numbers[ random_index_1 ][ 2 ]
    non_fixed_numbers.pop( random_index_1 )
    random_index_2 = random.randint( 0, len( non_fixed_numbers ) - 1)
    random_number_2 = non_fixed_numbers[ random_index_2 ][ 0 ]
    print( f"Random index 1: {random_index_1} and Random index 2: {random_index_2}")
    print( f"Random number 1: {random_number_1} and Random number 2: {random_number_2}" )


    
    random_number_2_row     = non_fixed_numbers[ random_index_2 ][ 1 ]
    random_number_2_column  = non_fixed_numbers[ random_index_2 ][ 2 ]

    new_sudoku[ random_number_1_row ][ random_number_1_column ] = random_number_2
    new_sudoku[ random_number_2_row ][ random_number_2_column ] = random_number_1

    return new_sudoku

if __name__ == "__main__":
    
    SIZE = 9
    initial_sudoku = GetSudoku()
    """
    DISPLAY = DM(SIZE, initial_sudoku)
    DISPLAY.DisplayGrid()
    """

    random_state_sudoku = RandomSolution(initial_sudoku)
    DISPLAY             = DM(SIZE, random_state_sudoku)
    DISPLAY.DisplayGridWithColor(initial_sudoku, random_state_sudoku)
    row_cost            = RowCostFunction(random_state_sudoku)
    column_cost         = ColumnCostFunction(random_state_sudoku)
    total_cost          = row_cost + column_cost
    print("Cost Function: ", total_cost)
    

    square_numbers      = SelectSquare(random_state_sudoku)
    non_fixed_numbers   = GetNonFixedNumbers(square_numbers, initial_sudoku)
    new_sudoku_state    = ChangePlace(non_fixed_numbers, random_state_sudoku)
    DISPLAY.DisplayGridWithColor(initial_sudoku, new_sudoku_state)
    new_row_cost        = RowCostFunction(new_sudoku_state)
    new_column_cost     = ColumnCostFunction(new_sudoku_state)
    new_total_cost      = new_row_cost + new_column_cost
    print("New Row Cost: ", new_total_cost)
