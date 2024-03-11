import random
import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from save.SaveSudoku       import SaveSudoku       as SAVE
from random import sample

# PARAMETROS PARA EXECUTAR

SIZE = 9            # TAMANHO DO SUDOKU

PERCENTAGE = 100   # PORCENTAGEM DE NUMEROS NO SUDOKU

class Sudoku:

    def __init__ ( self, SIZE, PERCENTAGE = 50 ):
        self.PERCENTAGE = PERCENTAGE
        self.SIZE = SIZE
        self.grid = [ ]
        self.numbers_list = list( range( 1, SIZE + 1 ) )
        self.box_size = int( SIZE ** 0.5 )

        start_time = time.time() 
        
        rows = []
        cols = []

        rBase = range(self.box_size)

        for g in self.Shuffle(rBase):
            for r in self.Shuffle(rBase):
                rows.append(g * self.box_size + r)

        for g in self.Shuffle(rBase):
            for c in self.Shuffle(rBase):
                cols.append(g * self.box_size + c)

        nums  = self.Shuffle(range(1,self.SIZE+1))

        for r in rows:
            row = []
            for c in cols:
                number = nums[self.Pattern(r, c)]
                row.append(number)
            self.grid.append(row)
        
        print(self.CheckSudoku())

        self.InsertZeros()

        self.DisplayGrid()
        

        end_time = time.time() 
        time_taken = end_time - start_time

        print( f"Time taken to generate the sudoku: {time_taken:.5f} seconds" )

    def Shuffle(self,s): return sample(s,len(s)) 
    def Pattern(self,row,col): 
        return (self.box_size*(row%self.box_size)+row//self.box_size+col)%self.SIZE

    def CheckSudoku(self):
        numberSet = set( range( 1, self.SIZE + 1 ) )
        for i in range( 0, self.SIZE ):
            rowSet = set( self.grid[ i ] )
            if rowSet != numberSet:
                return False
            
            columnSet = set( self.grid[ j ][ i ] for j in range( 0, self.SIZE ) )
            if columnSet != numberSet:
                return False
        
        for i in range(0,self.box_size):
            for j in range(0,self.box_size):
                boxSet = set()
                for k in range(0,self.box_size):
                    for l in range(0,self.box_size):
                        boxSet.add(self.grid[i*self.box_size+k][j*self.box_size+l])
                if boxSet != numberSet:
                    return False

        return True
    def InsertZeros( self ):
   
        for i in range( 0, self.SIZE ):
            for j in range( 0, self.SIZE ):
                number_dice_roll = random.randint( 1, 100 )
                if number_dice_roll > self.PERCENTAGE:
                    self.grid[ i ][ j ] = 0
        
        return True
              
    def DisplayGrid( self ):
        """
        print( "\n" )
        print( "     ", end=""	)
        for i in range(  self.SIZE ) :
            if i == 2 or i == 5:
                print( f"{i}|  ", end="" )
            else:
                print( f"{i}  ", end="" )
        print( "\n", end="" )
        """

        """
        for j in range( 3 *  self.SIZE + 5 ) :
            print( "-", end="" )
        print( "\n", end="" )
        """
        for row in range(  self.SIZE ) :
            """
            if row == 3 or row == 6:
                for j in range( 3 * self.SIZE  + 5 ) :
                    print( "-", end="" )
                print( "\n", end="" )
            print( f"{row} |", end="" )
            """
            for column in range( self.SIZE  ):
                print( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }|", end="" )
            print( "\n", end="" )
        """
        for j in range( 3 *  self.SIZE + 5 ) :
            print( "-", end="" )
        print( "\n", end="" )
        """
if __name__ == "__main__":
        sudoku = Sudoku( SIZE, PERCENTAGE )
        S = SAVE( SIZE, sudoku.grid )
        S.SaveSudokuIncomplete( PERCENTAGE )
