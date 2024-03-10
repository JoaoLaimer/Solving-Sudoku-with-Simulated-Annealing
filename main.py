from module.CreateMatrix import CreateMatrix as CM
from module.DisplayMatrix import DisplayMatrix as DM
from module.CheckMatrix import CheckMatrix as CKM
from save.SaveSudoku import SaveSudoku as SAVE
import time
import random
SIZE = 25

def Randomsudoku():
    file  = open(f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r" )
    count = 0
    for line in file:
        if line.startswith( "Sudoku" ):
            count += 1
    random_sudoku_id = random.randint( 0, count - 1 )
    file.close()
    return random_sudoku_id

def GetSudoku():
    sudoku_id = Randomsudoku()
    file      = open( f"sudokus\\sudoku_incomplete_{str(SIZE)}.txt", "r" )
    sudoku    = []
    for line in file:
        if line.startswith( "Sudoku " + str( sudoku_id ) ):
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
    S = SAVE( SIZE, M.grid )
    S.SaveSudokuWithHiddenNumbers( 15 )
    D = DM( SIZE, M.grid )
    D.DisplayGrid()
    print( "\n" )

def SolveSudoku():
    sudoku = GetSudoku()
    D = DM( SIZE, sudoku )
    D.DisplayGrid()
    print( "\n" )
    M = CM( SIZE )
    solved = M.Solve( sudoku )
    D = DM( SIZE, solved )
    D.DisplayGrid()


if __name__ == "__main__":

    while True:
        print( "1. Generate a new Sudoku\n2. Solve a Sudoku\n3. Exit" )
        option = int( input( "Enter your choice: " ) )
        if option == 1:
            GenerateSudoku()
        elif option == 2:
            SolveSudoku()
        elif option == 3:
            print( "Exiting..." )
            break
        else:
            print( "Invalid option. Please choose again." )