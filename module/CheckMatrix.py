
class CheckMatrix:

    def __init__ ( self, SIZE, grid ):
        self.SIZE = SIZE
        self.grid = grid
        self.box_size = int( SIZE ** 0.5 )

    def CheckColumn ( self, num, column, grid ):
        for row in range( self.SIZE ):
            if grid[ row ][ column ] == num:
                return False
        return True
    
    def CheckRow ( self, num, row, grid ):
        for column in range( self.SIZE ):
            if grid[ row ][ column ] == num:
                return False
        return True
    
    def CheckSquare ( self, num, column, row, grid ):
        column_check = column - column % self.box_size
        row_check = row - row % self.box_size
        for i in range( 0, self.box_size ):
            for j in range( 0, self.box_size ):
                if grid[ i + row_check ][ j + column_check ] == num:
                    return False
        return True

    def CheckGrid ( self, num, column, row, grid ):
        return self.CheckColumn( num, column, grid ) and self.CheckRow( num, row, grid ) and self.CheckSquare( num, column, row, grid )
    
    def CheckQuadrant( self, start_col, start_row, grid ):
        nums = set()
        for row in range( start_row, start_row + self.box_size ):
            for col in range( start_col, start_col + self.box_size ):
                num = grid[ row ][ col ]
                if num in nums or num < 1 or num > 9:
                    return False
                nums.add( num )
        return True
    
    def GetCellNumber( self, column, row ):
        return self.grid[ row ][ column ]

    def IsGridFull ( self ):
        for row in range (self.SIZE ):
            for column in range ( self.SIZE ):
                if self.grid[ row ][ column ] == 0:
                    return False
        return True
                                
    def IsValidSolution( self ):
        for row in range( 0, self.SIZE, self.box_size ):
            for col in range( 0, self.SIZE, self.box_size ):
                if not self.CheckQuadrant( row, col, self.grid ):
                    return False
        return True
