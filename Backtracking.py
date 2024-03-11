from module.DisplayMatrix import DisplayMatrix as DM
from save.SaveSudoku import SaveSudoku as SAVE
import time
import sys
sys.setrecursionlimit(1500)

#PARAMETROS

SIZE = 16
SIZE_SQUARE = int(SIZE ** 0.5)

def GetSudoku():
    sudoku_id = 5
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

def CheckSudoku(sudoku):
        numberSet = set( range( 1, SIZE + 1 ) )
        for i in range( 0, SIZE ):
            rowSet = set( sudoku[ i ] )
            if rowSet != numberSet:
                return False
            
            columnSet = set( sudoku[ j ][ i ] for j in range( 0, SIZE ) )
            if columnSet != numberSet:
                return False
        
        for i in range(0, SIZE_SQUARE):
            for j in range(0, SIZE_SQUARE):
                boxSet = set()
                for k in range(0, SIZE_SQUARE):
                    for l in range(0, SIZE_SQUARE):
                        boxSet.add(sudoku[i* SIZE_SQUARE+k][j* SIZE_SQUARE+l])
                if boxSet != numberSet:
                    return False

        return True

def CheckColumn (  num, column, grid ):
        for row in range( SIZE ):
            if grid[ row ][ column ] == num:
                return False
        return True
    
def CheckRow (  num, row, grid ):
    for column in range( SIZE ):
        if grid[ row ][ column ] == num:
            return False
    return True

def CheckSquare (  num, column, row, grid ):
    column_check = column - column % SIZE_SQUARE
    row_check = row - row % SIZE_SQUARE
    for i in range( 0, SIZE_SQUARE ):
        for j in range( 0, SIZE_SQUARE ):
            if grid[ i + row_check ][ j + column_check ] == num:
                return False
    return True

def CheckGrid ( num, column, row, grid ):
    return CheckColumn( num, column, grid ) and CheckRow( num, row, grid ) and CheckSquare( num, column, row, grid )

def Backtracking( grid):
    numbers = list( range( 1, SIZE + 1 ) )
    for row in range( SIZE ):
        for column in range( SIZE ):
            if grid[ row ][ column ] == 0:
                #random.shuffle( numbers )
                for number in numbers:
                    if CheckGrid( number, column, row, grid ):
                        grid[ row ][ column ] = number
                        if Backtracking( grid):
                            return True
                        if CheckSudoku(grid): 
                            return True
                        grid[ row ][ column ] = 0
                return False
    return True

if __name__ == "__main__":
    
    sudoku = GetSudoku()
    start_time = time.time()
    Backtracking(sudoku)
    print(CheckSudoku(sudoku))
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken}")
    S = SAVE(SIZE, sudoku)
    S.SaveSudokuComplete( 0, time_taken)
    DISPLAY = DM(SIZE, sudoku)
    DISPLAY.DisplayGrid()