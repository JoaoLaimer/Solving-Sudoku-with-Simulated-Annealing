def CheckSudoku( board ):
        numberSet = set( range( 1, side + 1 ) )
        for i in range( 0, side ):
            rowSet = set( board[ i ] )
            if rowSet != numberSet:
                return False
            
            columnSet = set( board[ j ][ i ] for j in range( 0, side ) )
            if columnSet != numberSet:
                return False
        
        for i in range(0,base):
            for j in range(0,base):
                boxSet = set()
                for k in range(0,base):
                    for l in range(0,base):
                        boxSet.add(board[i*base+k][j*base+l])
                if boxSet != numberSet:
                    return False

        return True


base  = 3
side  = base*base
# pattern for a baseline valid solution
def pattern(r,c): 

    return (base*(r%base)+r//base+c)%side


# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s)) 
rBase = range(base) 

rows = []
cols = []

for g in shuffle(rBase):
    for r in shuffle(rBase):
        rows.append(g * base + r)

for g in shuffle(rBase):
    for c in shuffle(rBase):
        cols.append(g * base + c)
nums  = shuffle(range(1,base*base+1))

board = []

for r in rows:
    row = []
    for c in cols:
        number = nums[pattern(r, c)]
        row.append(number)
    board.append(row)

board[1][1] = 1 

for line in board: print(line)

print(CheckSudoku(board))

