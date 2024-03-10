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
import module.SudokuGenerator as SudokuGenerator
from save.save_sudoku       import SaveSudoku       as SAVE
import random
import time

SIZE        = 9
SIZE_SQUARE = int(SIZE ** 0.5)
SQUARE_SIZE = int(SIZE / SIZE_SQUARE)
PERCENTAGEOFNUMBERS  = 70
"""
SIMULATED ANNEALING
PASSOS:
1 - Generate a random solution                                              XXXXXXXXXXXXXXXXXXXXXX
2 - Calculate the cost of the solution                                      XXXXXXXXXXXXXXXXXXXXXX
3 - Generate a new solution                                                 XXXXXXXXXXXXXXXXXXXXXX
4 - Calculate the cost of the new solution                                  XXXXXXXXXXXXXXXXXXXXXX
5 - Compare the cost of the new solution with the cost of the old solution  XXXXXXXXXXXXXXXXXXXXXX

Cost function:
1 - Number of conflicts in the solution
3 - Number of repeated numbers in the solution

6 - If the new solution is better than the old solution, accept the new solution XXXXXXXXXXXXXXXXXXXXXX
8 - Select a starting temperature                                                XXXXXXXXXXXXXXXXXXXXXX
9 - Calculate iterations per temperature                                         XXXXXXXXXXXXXXXXXXXXXX
10 - Select a cooling rate                                                       XXXXXXXXXXXXXXXXXXXXXX

Probability of accepting the new solution: 1/1+e^(new_cost - old_cost)/T or
                                           exp(−δ/t )
"""
"""
The algorithm works by first guessing a solution at random -- filling in the empty cells above with random digits between 1 and 9. 
Then it "scores" this solution by counting the number of digits duplicated in all the rows, columns and blocks. 
Next it evaluates a number of candidate new solutions by tweaking one of the free digits, and scores those. 
The algorithm then selects one of the candidate solutions at random for the next step, weighted by the change in the score.
"""
"""
def SelectRandomSudoku():
    file = open( "sudokus\\sudoku_incomplete.txt", "r" )
    count = 0
    for line in file:
        if line.startswith( "Sudoku" ):
            count += 1
    random_sudoku_id = random.randint( 0, count - 1 )
    file.close()
    return random_sudoku_id

def GetSudoku():
    sudoku_id = SelectRandomSudoku()
    file = open( "sudokus\\sudoku_incomplete.txt", "r" )
    sudoku = []
    for line in file:
        if line.startswith( "Sudoku " + str( sudoku_id ) ):
            for i in range( SIZE ):
                row = file.readline()
                row = row.split() 
                row = [ int(num) for num in row ]  
                sudoku.append( row )
            break
    file.close()
    return sudoku, sudoku_id
"""
def RandomSolution( sudoku ):
    sudoku_grid = [ row[:] for row in sudoku ]  
    for row in range( SIZE ):
        for column in range( SIZE ):
            if sudoku_grid[ row ][ column ] == 0:
                checker = CKM( SIZE, sudoku_grid )
                number = random.randint( 1, SIZE )
                while not checker.CheckSquare( number, column, row, sudoku_grid ):
                    number = random.randint( 1, SIZE )
                sudoku_grid[ row ][ column ] = number
    return sudoku_grid

def RowCostFunction( sudoku ):
    conflicts = 0
    checked_numbers = set()
    for row in range( SIZE ):
        checked_numbers.clear()
        for column in range( SIZE ):
            number = sudoku[ row ][ column ]
            for i in range ( column, SIZE ):
                if i != column and sudoku[ row ][ i ] == number and number not in checked_numbers:
                    conflicts += 1
                    checked_numbers.add( number )
    return conflicts

def ColumnCostFunction( sudoku ):
    conflicts = 0
    checked_numbers = set()
    for column in range( SIZE ):
        checked_numbers.clear()
        for row in range( SIZE ):
            number = sudoku[ row ][ column ]
            for i in range ( row, SIZE ):
                if i != row and sudoku[ i ][ column ] == number and number not in checked_numbers: 
                    #print(f"Number {number} in row {row} and column {column} is repeated in row {i}")
                    conflicts += 1
                    checked_numbers.add( number )
    return conflicts

def CalculateTotalCost( sudoku ):
    row_cost    = RowCostFunction( sudoku )
    column_cost = ColumnCostFunction( sudoku )
    return row_cost + column_cost

def SelectRandomSquare( sudoku ):
    random_square_row_index     = random.randint( 0, SQUARE_SIZE - 1 )
    random_square_column_index  = random.randint( 0, SQUARE_SIZE - 1 )
    square_numbers = []
    
    #print("Selected Square: ")
    for row in range( random_square_row_index * SQUARE_SIZE, ( random_square_row_index + 1 ) * SQUARE_SIZE ):
        for column in range( random_square_column_index * SQUARE_SIZE, ( random_square_column_index + 1 ) * SQUARE_SIZE ):
            #print(sudoku[row][column], end=" ")
            square_numbers.append( ( sudoku[ row ][ column ], row, column ) )
        #print()
    return square_numbers

def GetNonFixedNumbers(square_numbers, initial_sudoku):
    """   
    fixed_numbers = []
    for i in range( len( square_numbers ) ):
        if initial_sudoku[square_numbers[i][1]][square_numbers[i][2]] != 0:
            fixed_numbers.append( square_numbers[i][0] )
    
    not_fixed_numbers = []
    for numbers in square_numbers:
        if numbers[0] not in fixed_numbers:
            not_fixed_numbers.append( numbers )
    """
    not_fixed_numbers = []
    for numbers in square_numbers:
        if initial_sudoku[numbers[1]][numbers[2]] == 0:
            not_fixed_numbers.append(numbers)
    """
    print("Square Numbers: ", square_numbers)
    print("Fixed Numbers: ", fixed_numbers)
    print("Not fixed numbers: ", not_fixed_numbers)
    """
    return not_fixed_numbers

def SwapTwoCells( non_fixed_numbers, sudoku ):
    if non_fixed_numbers == []:
        return sudoku
    if len( non_fixed_numbers ) < 2:
        return sudoku
    new_sudoku = numpy.copy( sudoku )

    cell_1 = random.choice( non_fixed_numbers )
    cell_2 = random.choice( non_fixed_numbers )
    while cell_1 == cell_2:
        cell_2 = random.choice( non_fixed_numbers )
    temp_cell = new_sudoku[cell_1[1]][cell_1[2]]
    new_sudoku[cell_1[1]][cell_1[2]] = new_sudoku[cell_2[1]][cell_2[2]]
    new_sudoku[cell_2[1]][cell_2[2]] = temp_cell

    return new_sudoku

def ChooseState( new_sudoku, new_cost, old_sudoku, old_cost, TEMPERATURE ):
    if new_cost < old_cost:
        return new_sudoku, new_cost
    else:
        probability = 1 / ( 1 + ( 2.71828 ** ( new_cost - old_cost ) / TEMPERATURE ) )
        if random.random() < probability:
            return new_sudoku, new_cost
        else:
            return old_sudoku, old_cost

def CalculateInitialTemperature(sudoku_grid, num_neighborhood_moves):
    neighborhood_costs = []
    temp_sudoku = [row[:] for row in sudoku_grid]
    for i in range(num_neighborhood_moves):
        random_state_sudoku = RandomSolution(temp_sudoku)
        square_numbers      = SelectRandomSquare(temp_sudoku)
        non_fixed_numbers   = GetNonFixedNumbers(square_numbers, sudoku_grid)
        new_sudoku_state    = SwapTwoCells(non_fixed_numbers, random_state_sudoku)
        new_total_cost      = CalculateTotalCost(new_sudoku_state)
        neighborhood_costs.append(new_total_cost)

    standard_deviation = ( statistics.pstdev( neighborhood_costs ) )
    if standard_deviation == 0:
        standard_deviation = 1

    return standard_deviation

def ChooseNumberOfItterations(sudoku_grid):
    numberOfItterations = 0
    for i in range (0,SIZE):
        for j in range (0,SIZE):
            if sudoku_grid[i][0] != 0:
                numberOfItterations += 1
    #print(f"Number of itterations: {numberOfItterations}")
    return numberOfItterations
        
def SimulatedAnnealing():
    initial_sudoku = SudokuGenerator.Sudoku( SIZE, PERCENTAGEOFNUMBERS )
    
    INITIAL_TEMPERATURE     =       CalculateInitialTemperature( initial_sudoku.grid, num_neighborhood_moves=20 )
    TEMPERATURE = INITIAL_TEMPERATURE
    ITTERATIONS_PER_TEMPERATURE =   ChooseNumberOfItterations(initial_sudoku.grid)
    COLLING_RATE    = 0.99
    SOLUTION_FOUND  = 0
    STUCK_COUNTER   = 0

    random_state_sudoku         =   RandomSolution    ( initial_sudoku.grid )
    random_state_total_cost     =   CalculateTotalCost( random_state_sudoku )

    current_sudoku = random_state_sudoku
    current_cost   = random_state_total_cost
    #"""
    DISPLAY = DM( SIZE, random_state_sudoku )
    DISPLAY.DisplayGridWithColor( initial_sudoku.grid, random_state_sudoku )
    #"""
    STEP = 1
    while SOLUTION_FOUND == 0:
            
        for i in range( ITTERATIONS_PER_TEMPERATURE ):
            #print(f"Step: {STEP} | Temperature: {TEMPERATURE} | Current Cost: {current_cost}| Stuck Counter: {STUCK_COUNTER}")
            previous_cost       = current_cost
            square_numbers      = SelectRandomSquare    ( random_state_sudoku )
            non_fixed_numbers   = GetNonFixedNumbers    ( square_numbers, initial_sudoku.grid )
            new_sudoku_state    = SwapTwoCells          ( non_fixed_numbers, current_sudoku )
            new_total_cost      = CalculateTotalCost    ( new_sudoku_state )
            current_sudoku, current_cost = ChooseState  ( new_sudoku_state, new_total_cost, current_sudoku, current_cost, TEMPERATURE )
            TEMPERATURE *= COLLING_RATE
            if current_cost <= 0:
                SOLUTION_FOUND = 1
                break
            if current_cost >= previous_cost:
                STUCK_COUNTER += 1
            else:
                STUCK_COUNTER = 0
            if ( STUCK_COUNTER > 100 ):
                TEMPERATURE = INITIAL_TEMPERATURE
                STUCK_COUNTER = 0
            STEP += 1
            
    return current_sudoku

if __name__ == "__main__":
    start_time    = time.time()

    solved_sudoku = SimulatedAnnealing()
    
    end_time      = time.time()
    time_taken    = end_time - start_time
    print( f"Time taken: {time_taken}" )

    DISPLAY = DM(SIZE, solved_sudoku)
    DISPLAY.DisplayGrid()
    #checker = CKM(SIZE, solved_sudoku)
    #print(checker.Is_Valid_Solution())
