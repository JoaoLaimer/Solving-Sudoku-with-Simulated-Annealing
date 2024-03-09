from module.check_matrix import CheckMatrix as CKM
from module.display_matrix import DisplayMatrix as DM
import random
class CreateMatrix:

    def __init__( self, SIZE ):
        self.SIZE = SIZE
        self.grid = [ [ 0 for x in range( SIZE ) ] for y in range( SIZE ) ]
        self.CKM = CKM( SIZE, self.grid )
        self.numbers = list( range( 1, SIZE + 1 ) )

    def Initialize_Grid( self ):
        for row in range( 0, self.SIZE ):
            for col in range( 0, self.SIZE ):
                self.grid[ row ][ col ] = 0

    def Fill_Grid( self ):
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                if self.grid[row][column] == 0:
                    random.shuffle( self.numbers )
                    for number in self.numbers:
                        if self.CKM.Check_Grid( number, column, row, self.grid ):
                            self.grid[row][column] = number
                            if self.CKM.Is_Grid_Full(): 
                                return True
                            if self.Fill_Grid():
                                return True
                            self.grid[row][column] = 0
                    return False
        return True
    
    def Backtracking(self, grid, checker):
        for row in range( self.SIZE ):
            for column in range( self.SIZE ):
                if grid[row][column] == 0:
                    random.shuffle( self.numbers )
                    for number in self.numbers:
                        if checker.Check_Grid( number, column, row, grid ):
                            grid[row][column] = number
                            if checker.Is_Grid_Full(): 
                                return True
                            if self.Backtracking(grid, checker):
                                return True
                            grid[row][column] = 0
                    return False
        return True
    
    def Solve(self, grid):
        checker = CKM(self.SIZE, grid)
        self.Backtracking(grid, checker)
        if checker.Is_Valid_Solution():
            return grid
        else:
            return self.Solve(grid)