import sys
import os
import numpy
import statistics 

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from module.DisplayMatrix  import DisplayMatrix    as DM
from save.SaveSudoku       import SaveSudoku       as SAVE
import random
import time


# PARAMETROS PARA EXECUTAR

SIZE        = 9                             # TAMANHO DO SUDOKU
SELECTED_SUDOKU = 5                         # SUDOKU SELECIONADO
SIZE_SQUARE = int(SIZE ** 0.5)              # TAMANHO DO QUADRADO


def GetSudokuFromFile():
    sudoku_id = SELECTED_SUDOKU #SelectRandomSudoku()
    file = open(f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r")
    sudoku = []
    for line in file:
        if line.startswith("Sudoku: " + str(sudoku_id)):
            for i in range(SIZE):
                row = file.readline()
                row = row.split() 
                row = [int(num) for num in row]  
                sudoku.append(row)
            break
    file.close()
    return sudoku, sudoku_id

def CreateRandomSolution(sudoku):
    sudoku_grid = [row[:] for row in sudoku]  
    for row in range(SIZE):
        for column in range(SIZE):
            if sudoku_grid[row][column] == 0:
                number = random.randint(1, SIZE)
                while not CheckSquare(number, column, row, sudoku_grid):
                    number = random.randint(1, SIZE)
                sudoku_grid[row][column] = number
    return sudoku_grid

def CheckSquare(num, column, row, grid ):
        column_check = column - column % SIZE_SQUARE
        row_check = row - row % SIZE_SQUARE
        for i in range( 0, SIZE_SQUARE ):
            for j in range( 0, SIZE_SQUARE ):
                if grid[ i + row_check ][ j + column_check ] == num:
                    return False
        return True

def GetRowCost(sudoku):
    conflicts = 0
    checked_numbers = set()
    for row in range(SIZE):
        checked_numbers.clear()
        for column in range(SIZE):
            number = sudoku[row][column]
            for i in range (column, SIZE):
                if i != column and sudoku[row][i] == number and number not in checked_numbers:
                    conflicts += 1
                    checked_numbers.add(number)
    return conflicts

def GetColumnCost(sudoku):
    conflicts = 0
    checked_numbers = set()
    for column in range(SIZE):
        checked_numbers.clear()
        for row in range(SIZE):
            number = sudoku[row][column]
            for i in range (row, SIZE):
                if i != row and sudoku[i][column] == number and number not in checked_numbers: 
                    #print(f"Number {number} in row {row} and column {column} is repeated in row {i}")
                    conflicts += 1
                    checked_numbers.add(number)
    return conflicts

def CalculateTotalCost(sudoku):
    row_cost    = GetRowCost(sudoku)
    column_cost = GetColumnCost(sudoku)
    return row_cost + column_cost

def SelectSquare(sudoku):
    random_square_row_index     = random.randint(0, SIZE_SQUARE - 1)
    random_square_column_index  = random.randint(0, SIZE_SQUARE - 1)
    square_numbers = []
    
    #print("Selected Square: ")
    for row in range(random_square_row_index * SIZE_SQUARE, (random_square_row_index + 1) * SIZE_SQUARE):
        for column in range(random_square_column_index * SIZE_SQUARE, (random_square_column_index + 1) * SIZE_SQUARE):
            #print(sudoku[row][column], end=" ")
            square_numbers.append((sudoku[row][column], row, column))
        #print()
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

    return not_fixed_numbers

def SwapTwoCells( non_fixed_numbers, sudoku ):
    if non_fixed_numbers == []:
        return sudoku
    if len(non_fixed_numbers) < 2:
        return sudoku
    new_sudoku = numpy.copy(sudoku)

    cell_1 = random.choice(non_fixed_numbers)
    cell_2 = random.choice(non_fixed_numbers)
    while cell_1 == cell_2:
        cell_2 = random.choice(non_fixed_numbers)
    temp_cell = new_sudoku[cell_1[1]][cell_1[2]]
    new_sudoku[cell_1[1]][cell_1[2]] = new_sudoku[cell_2[1]][cell_2[2]]
    new_sudoku[cell_2[1]][cell_2[2]] = temp_cell

    return new_sudoku

def ChooseState(new_sudoku, new_cost, old_sudoku, old_cost, TEMPERATURE):
    if new_cost < old_cost:
        return new_sudoku, new_cost
    else:
        num = random.random()
        #probability =  math.exp(new_cost - old_cost/TEMPERATURE)
        probability = 1 / (1 + (2.71828 ** (new_cost - old_cost) / TEMPERATURE))
        if num < probability:
            return new_sudoku, new_cost
        else:
            return old_sudoku, old_cost

def CalculateInitialTemperature(initial_sudoku, num_neighborhood_moves):
    neighborhood_costs = []
    temp_sudoku = [row[:] for row in initial_sudoku]
    for i in range(num_neighborhood_moves):
        random_state_sudoku = CreateRandomSolution(temp_sudoku)
        square_numbers      = SelectSquare(temp_sudoku)
        non_fixed_numbers   = GetNonFixedNumbers(square_numbers, initial_sudoku)
        new_sudoku_state    = SwapTwoCells(non_fixed_numbers, random_state_sudoku)
        new_total_cost      = CalculateTotalCost(new_sudoku_state)
        neighborhood_costs.append(new_total_cost)

    standard_deviation = (statistics.pstdev(neighborhood_costs))
    if standard_deviation == 0:
        standard_deviation = 1

    return standard_deviation

def ChooseNumberOfItterations(initial_sudoku):
    numberOfItterations = 0
    for i in range (0,SIZE):
        for j in range (0,SIZE):
            if initial_sudoku[i][0] != 0:
                numberOfItterations += 1
    #print(f"Number of itterations: {numberOfItterations}")
    return numberOfItterations

def CheckSudoku(sudoku):
        numberSet = set( range( 1, SIZE + 1 ) )
        for i in range( 0, SIZE ):
            rowSet = set( sudoku[ i ] )
            if rowSet != numberSet:
                return False
            
            columnSet = set( sudoku[ j ][ i ] for j in range( 0, SIZE ) )
            if columnSet != numberSet:
                return False
        
        for i in range(0,SIZE_SQUARE):
            for j in range(0,SIZE_SQUARE):
                boxSet = set()
                for k in range(0,SIZE_SQUARE):
                    for l in range(0,SIZE_SQUARE):
                        boxSet.add(sudoku[i*SIZE_SQUARE+k][j*SIZE_SQUARE+l])
                if boxSet != numberSet:
                    return False

        return True
        
def SimulatedAnnealing():
    initial_sudoku, initial_sudoku_id  = GetSudokuFromFile()
    print(f"Initial Sudoku ID: {initial_sudoku_id}")

    INITIAL_TEMPERATURE     = CalculateInitialTemperature(initial_sudoku, num_neighborhood_moves=20)
    TEMPERATURE = INITIAL_TEMPERATURE
    ITTERATIONS_PER_TEMPERATURE = ChooseNumberOfItterations(initial_sudoku)
    COLLING_RATE    = 0.99
    SOLUTION_FOUND  = 0
    STUCK_COUNTER   = 0

    random_state_sudoku         = CreateRandomSolution(initial_sudoku)
    
    random_state_total_cost     = CalculateTotalCost(random_state_sudoku)

    current_sudoku = random_state_sudoku
    current_cost   = random_state_total_cost
    #"""
    DISPLAY = DM(SIZE, random_state_sudoku)
    DISPLAY.DisplayGridWithColor(initial_sudoku, random_state_sudoku)
    #"""
    STEP = 1
    while SOLUTION_FOUND == 0:
            
        for i in range(ITTERATIONS_PER_TEMPERATURE):
            #print(f"Step: {STEP} | Temperature: {TEMPERATURE} | Current Cost: {current_cost}| Stuck Counter: {STUCK_COUNTER}")
            previous_cost       = current_cost
            square_numbers      = SelectSquare          (random_state_sudoku)
            non_fixed_numbers   = GetNonFixedNumbers    (square_numbers, initial_sudoku)
            new_sudoku_state    = SwapTwoCells          (non_fixed_numbers, current_sudoku)
            new_total_cost      = CalculateTotalCost    (new_sudoku_state)
            current_sudoku, current_cost = ChooseState  (new_sudoku_state, new_total_cost, current_sudoku, current_cost, TEMPERATURE)
            TEMPERATURE *= COLLING_RATE
            if current_cost <= 0:
                SOLUTION_FOUND = 1
                break
            if current_cost >= previous_cost:
                STUCK_COUNTER += 1
            else:
                STUCK_COUNTER = 0
            if (STUCK_COUNTER > 100):
                TEMPERATURE = INITIAL_TEMPERATURE
            STEP += 1
            
    print(CheckSudoku(current_sudoku))
    return current_sudoku

if __name__ == "__main__":
    
    start_time = time.time()
    solved_sudoku = SimulatedAnnealing()
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken}")
    S = SAVE(SIZE, solved_sudoku)
    S.SaveSudokuComplete( 0, time_taken)
    DISPLAY = DM(SIZE, solved_sudoku)
    DISPLAY.DisplayGrid()