import random
import time

class Sudoku:

    def __init__ ( self, SIZE, PERCENTAGE = 50 ):
        self.PERCENTAGE = PERCENTAGE
        self.SIZE = SIZE
        self.grid = [ [ 0 for x in range( SIZE ) ] for y in range( SIZE ) ]
        self.numbers_list = list( range( 1, SIZE + 1 ) )
        self.box_size = int( SIZE ** 0.5 )
        start_time = time.time() 
        self.InitializeGrid()
        while( not self.FillGrid() ):
            self.InitializeGrid()
        
        self.DisplayGrid()

        end_time = time.time() 
        time_taken = end_time - start_time
        print( f"Time taken to generate the sudoku: {time_taken:.5f} seconds" )
  
    def InitializeGrid( self ):
        for row in range( 0, self.SIZE ):
            for col in range( 0, self.SIZE ):
                self.grid[ row ][ col ] = 0

    def CheckGrid( self, number, column, row ):

        for i in range( 0, self.SIZE ):
            if self.grid[ i ][ column ] == number:
                return False
            
        for j in range(0, self.SIZE ):
            if self.grid[ row ][ j ] == number:
                return False
            
        column_check = column - column % self.box_size
        row_check    = row - row % self.box_size
        for i in range( 0, self.box_size ):
            for j in range( 0, self.box_size ):
                if self.grid[ i + row_check ][ j + column_check ] == number:
                    return False
    
        return True


    def FillGrid( self ):
        for row in range( self.SIZE ):
            full_numbers = list( range( 1, self.SIZE + 1 ) )
            self.numbers_list = full_numbers
            column = 0
            infLoop = 0
            while column < self.SIZE:
                
                if self.grid[ row ][ column ] == 0:
                    number_dice_roll = random.randint( 1, 6 )
                    number = random.choice( self.numbers_list )

                    loopCount = 0
                    while True:
                        number = random.choice( self.numbers_list )
                        if self.CheckGrid( number, column, row) :
                            self.grid[ row ][ column ] = number
                            self.numbers_list.remove( number )
                            break
                        elif loopCount > 30:
                            for i in range( 0, self.SIZE ):
                                self.grid[ row ][ i ] = 0
                            column = -1
                            self.numbers_list = list( range( 1, self.SIZE + 1 ) )
                            break

                        loopCount += 1

                    infLoop += 1
                    if infLoop > 10000:
                        print( "Infinit loop" )
                        return False
                column += 1
            
        for i in range( 0, self.SIZE ):
            for j in range( 0, self.SIZE ):
                number_dice_roll = random.randint( 1, 100 )
                if number_dice_roll >= self.PERCENTAGE:
                    self.grid[ i ][ j ] = 0
        
        return True
              
                           
    
    def DisplayGrid( self ):
        #"""
        print( "\n" )
        print( "     ", end=""	)
        for i in range(  self.SIZE ) :
            if i == 2 or i == 5:
                print( f"{i}|  ", end="" )
            else:
                print( f"{i}  ", end="" )
        print( "\n", end="" )
        #"""

        #"""
        for j in range( 3 *  self.SIZE + 5 ) :
            print( "-", end="" )
        print( "\n", end="" )
        #"""
        for row in range(  self.SIZE ) :
            #"""
            if row == 3 or row == 6:
                for j in range( 3 * self.SIZE  + 5 ) :
                    print( "-", end="" )
                print( "\n", end="" )
            print( f"{row} |", end="" )
            #"""
            for column in range( self.SIZE  ):
                if column == 2 or column == 5:
                    print( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }|", end="" )
                else:
                    print( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }", end="" )
            print( "\n", end="" )
        #"""
        for j in range( 3 *  self.SIZE + 5 ) :
            print( "-", end="" )
        print( "\n", end="" )
        #"""


if __name__ == "__main__":
    sudoku = Sudoku(9,85)

                        