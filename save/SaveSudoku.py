import random
class SaveSudoku:

    def __init__ ( self, SIZE, grid ):
        self.SIZE = SIZE
        self.grid = grid

    def CountSavedSudokus( self ):
        count = 0
        file  = open( f"sudokus\\sudoku_incomplete_{str(self.SIZE)}.txt", "r+" )
        for line in file:
            if line.startswith( "Sudoku" ):
                count += 1
        file.close()
        return count

    def SaveSudokuIncomplete( self, percentage = 0 ):
        saved_sudoku_numbers = self.CountSavedSudokus()
        file = open( f"sudokus\\sudoku_incomplete_{str(self.SIZE)}.txt", "a" ) 
        file.write( f"Sudoku: {saved_sudoku_numbers} | Percentage: {percentage}\n" )
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                file.write( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }" )
            file.write( "\n" )
        file.write( "\n" )
        file.close()
        #self.Save_Sudoku_With_Hidden_Numbers( hidden_numbers )

    def SaveSudokuComplete( self, percentage = 0, timetaken = 0 ):
        saved_sudoku_numbers = self.CountSavedSudokus()
        file = open( f"sudokus\\sudoku_complete_{str(self.SIZE)}.txt", "a" ) 
        file.write( f"Sudoku: {saved_sudoku_numbers} | Percentage: {percentage} | Time: {timetaken}\n")
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                file.write( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }" )
            file.write( "\n" )
        file.write( "\n" )
        file.close()
    
    def SaveSudokuWithHiddenNumbers( self, hidden_numbers ):
        saved_sudoku_numbers = self.CountSavedSudokus() - 1
        file = open( f"sudokus\\sudoku_incomplete_teste_{str(self.SIZE)}.txt", "a" ) 
        file.write( f"Sudoku {saved_sudoku_numbers}:\n" )
        while hidden_numbers > 0:
            row = random.randint( 0, self.SIZE - 1 )
            column = random.randint( 0, self.SIZE - 1 )
            if self.grid[ row ][ column ] != 0:
                self.grid[ row ][ column ] = 0
                hidden_numbers -= 1
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                file.write( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }" )
            file.write( "\n" )
        file.close()
