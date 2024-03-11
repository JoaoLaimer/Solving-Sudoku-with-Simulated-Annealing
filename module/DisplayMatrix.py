class DisplayMatrix:
    
    def __init__( self, SIZE, grid ):
        self.SIZE = SIZE   
        self.grid = grid

    def DisplayGrid( self ):
        #"""
        print("\n")
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
                    print( f"{ str( self.grid[ row ][ column ] ).rjust( 3 )}", end="" )
            print( "\n", end="" )
        #"""
        for j in range( 3 *  self.SIZE + 5 ) :
            print( "-", end="" )
        print( "\n", end="" )
        #"""

    def DisplayGridWithColor( self, initial_grid, difference_grid ):
        #"""
        print("\n")
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
                if initial_grid[row][column] == 0:
                    if column == 2 or column == 5:
                        print( f"\033[1;31;40m{ str( difference_grid[ row ][ column ] ).rjust( 3 )}\033[0m|", end="" )
                    else:
                        print( f"\033[1;31;40m{ str( difference_grid[ row ][ column ] ).rjust( 3 )}\033[0m", end="" )
                else:
                    if column == 2 or column == 5:
                        print( f"{ str( difference_grid[ row ][ column ] ).rjust( 3 )}|", end="" )
                    else:
                        print( f"{ str( difference_grid[ row ][ column ] ).rjust( 3 ) }", end="" )
            print( "\n", end="" )
        print( "\n" )