from module.CreateMatrix import CreateMatrix as CM
from module.DisplayMatrix import DisplayMatrix as DM
from module.CheckMatrix import CheckMatrix as CKM
from save.SaveSudoku import SaveSudoku as SAVE
import time
import random
import sys
sys.setrecursionlimit(1500)
SIZE = 16

def CountSudokus():
    file  = open(f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r" )
    count = 0
    for line in file:
        if line.startswith( "Sudoku" ):
            count += 1
    file.close()
    return count

def Randomsudoku():
    file  = open(f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r" )
    count = 0
    for line in file:
        if line.startswith( "Sudoku" ):
            count += 1
    random_sudoku_id = random.randint( 0, count - 1 )
    file.close()
    return random_sudoku_id

def GetSudoku(sudoku_id):
    file      = open( f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r" )
    sudoku    = []
    for line in file:
        if line.startswith( "Sudoku: " + str( sudoku_id ) ):
            for i in range( SIZE ):
                row = file.readline()
                row = row.split() 
                row = [ int( num ) for num in row ]  
                sudoku.append(row)
            break
    file.close()
    return sudoku

def GenerateSudoku():
    start_time = time.time() 
    M = CM( SIZE )
    M.InitializeGrid()
    M.FillGrid()
    end_time   = time.time() 
    time_taken = end_time - start_time
    #S = SAVE( SIZE, M.grid )
    #S.SaveSudokuWithHiddenNumbers( 15 )
    D = DM( SIZE, M.grid )
    D.DisplayGrid()
    print( "\n" )

def SolveSudoku(id):
    
    sudoku = GetSudoku(id)

    M = CM( SIZE )

    start_time = time.time()
    solved = M.Solve( sudoku )
    end_time = time.time()

    time_taken = end_time - start_time


    D = DM( SIZE, solved )
    D.DisplayGrid()
    checker = CKM( SIZE, solved )
    print( f"Sudoku ID: {id} | Is the solution valid? {checker.IsValidSolution()} | Time taken to solve the sudoku: {time_taken:.10f} seconds" )
    print("------------------------------------------------------------------------------------------------")


if __name__ == "__main__":

    count = CountSudokus()

    for i in range( 10 ):
        SolveSudoku(7)
        print( "\n" )