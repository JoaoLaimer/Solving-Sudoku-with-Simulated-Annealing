from module.create_matrix import CreateMatrix as CM
from module.display_matrix import DisplayMatrix as DM
from module.check_matrix import CheckMatrix as CKM
from save.save_sudoku import SaveSudoku as SAVE
import time
import random
SIZE = 9

def Random_sudoku():
    file = open("sudokus\\sudoku_incomplete.txt", "r")
    count = 0
    for line in file:
        if line.startswith("Sudoku"):
            count += 1
    random_sudoku_id = random.randint(0, count - 1)
    file.close()
    return random_sudoku_id

def Get_Sudoku():
    sudoku_id = Random_sudoku()
    file = open("sudokus\\sudoku_incomplete.txt", "r")
    sudoku = []
    for line in file:
        if line.startswith("Sudoku " + str(sudoku_id)):
            for i in range(9):
                row = file.readline()
                row = row.split() 
                row = [int(num) for num in row]  
                sudoku.append(row)
            break
    file.close()
    return sudoku

def Generate_Sudoku():
    start_time = time.time() 
    M = CM(SIZE)
    M.Initialize_Grid()
    M.Fill_Grid()
    end_time = time.time() 
    time_taken = end_time - start_time
    S = SAVE(SIZE, M.grid)
    S.Save_Sudoku(time_taken, 15)
    D = DM(SIZE, M.grid)
    D.DisplayGrid()
    print("\n")

def Solve_Sudoku():
    sudoku = Get_Sudoku()
    D = DM(SIZE, sudoku)
    D.DisplayGrid()
    print("\n")
    M = CM(SIZE)
    solved = M.Solve(sudoku)
    D = DM(SIZE, solved)
    D.DisplayGrid()


if __name__ == "__main__":

    while True:
        print("1. Generate a new Sudoku\n2. Solve a Sudoku\n3. Exit")
        option = int(input("Enter your choice: "))
        if option == 1:
            Generate_Sudoku()
        elif option == 2:
            Solve_Sudoku()
        elif option == 3:
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")