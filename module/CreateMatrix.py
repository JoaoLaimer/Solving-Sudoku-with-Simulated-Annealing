from module.CheckMatrix import CheckMatrix as CKM
from module.DisplayMatrix import DisplayMatrix as DM
import random
class CreateMatrix:

    def __init__( self, SIZE ):
        self.SIZE = SIZE
        self.grid = [ [ 0 for x in range( SIZE ) ] for y in range( SIZE ) ]
        self.CKM = CKM( SIZE, self.grid )
        self.numbers = list( range( 1, SIZE + 1 ) )

    def InitializeGrid( self ):
        for row in range( 0, self.SIZE ):
            for col in range( 0, self.SIZE ):
                self.grid[ row ][ col ] = 0

    def FillGrid( self ):
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                if self.grid[ row ][ column ] == 0:
                    random.shuffle( self.numbers )
                    for number in self.numbers:
                        if self.CKM.CheckGrid( number, column, row, self.grid ):
                            self.grid[ row ][ column ] = number
                            if self.CKM.IsGridFull(): 
                                return True
                            if self.FillGrid():
                                return True
                            self.grid[ row ][ column ] = 0
                    return False
        return True
    
    def Backtracking( self, grid, checker ):
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                if grid[ row ][ column ] == 0:
                    random.shuffle( self.numbers )
                    for number in self.numbers:
                        if checker.CheckGrid( number, column, row, grid ):
                            grid[ row ][ column ] = number
                            if self.Backtracking( grid, checker ):
                                return True
                            if checker.IsGridFull(): 
                                return True
                            grid[ row ][ column ] = 0
                    return False
        return True
    
    def Solve( self, grid ):
        checker = CKM( self.SIZE, grid )
        self.Backtracking( grid, checker )
        return grid
        #if checker.IsValidSolution():
            #return grid
        #else:
            #return self.Solve( grid )