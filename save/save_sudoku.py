import random
class SaveSudoku:

    def __init__ ( self, SIZE, grid ):
        self.SIZE = SIZE
        self.grid = grid

    def CountSavedSudokus( self ):
        count = 0
        file  = open( "sudokus\\sudoku_complete.txt", "r+" )
        for line in file:
            if line.startswith( "Sudoku" ):
                count += 1
        file.close()
        return count

    def SaveSudoku( self , time, hidden_numbers ):
        saved_sudoku_numbers = self.Count_Saved_Sudokus()
        file = open( "sudokus\\sudoku_complete.txt", "a" ) 
        file.write( f"Sudoku {saved_sudoku_numbers}:\n" )
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                file.write( f"{ str( self.grid[ row ][ column ] ).rjust( 3 ) }" )
            file.write( "\n" )
        file.write( f"Tempo de geração: {time} segundos\n\n" )  
        file.close()
        self.Save_Sudoku_With_Hidden_Numbers( hidden_numbers )

    def Save_Sudoku_With_Hidden_Numbers( self, hidden_numbers ):
        saved_sudoku_numbers = self.Count_Saved_Sudokus() - 1
        file = open( "sudokus\\sudoku_incomplete.txt", "a" ) 
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
    