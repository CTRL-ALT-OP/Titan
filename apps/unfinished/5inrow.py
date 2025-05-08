from tkinter import *
from tkinter import messagebox

root = Tk()

global turn
turn = "r"

def create_board(width):
    a = 0
    b = 0
    grid = []

    grid_pieces = []

    while a < width:
        row = []
        row_pieces = []
        while b < width:
            label = Button(root, text = "  ", command = lambda _row = a, _column = b: object_pressed(_row, _column))
            label.place(x=b*20,y=a*20,height=20,width=20)
            row.append(label)
            row_pieces.append("")
            b += 1
        b = 0
        grid.append(row)
        grid_pieces.append(row_pieces)
        a += 1
    return(grid,grid_pieces)

def object_pressed(_row, _column):
    global grid
    global grid_pieces
    global turn
    
    if turn == 'r':
        if grid_pieces[_row][_column] != "R" and grid_pieces[_row][_column] != "B":
            turn = 'b'
            grid[_row][_column].configure(bg = "red")
            grid_pieces[_row][_column] = "R"
            #print(grid_pieces)
            win_r = verify_board("R")
            if win_r:
                print("Red won the game!")
                ans = messagebox.askyesno(
                "Red won!", "Red won! Do you want to play again?")
                if ans:
                    for row in grid:
                        for piece in row:
                            piece.destroy()
                    grid = []
                    grid, grid_pieces = create_board(40)
    elif turn == 'b':
        if grid_pieces[_row][_column] != "R" and grid_pieces[_row][_column] != "B":
            turn = 'r'
            grid[_row][_column].configure(bg = "blue")
            grid_pieces[_row][_column] = "B"
            #print(grid_pieces)
            win_r = verify_board("B")
            if win_r:
                print("Blue won the game!")
                ans = messagebox.askyesno(
                "Blue won!", "Blue won! Do you want to play again?")
                if ans:
                    for row in grid:
                        for piece in row:
                            piece.destroy()
                    grid = []
                    grid, grid_pieces = create_board(40)
    
def verify_board(player):
    row_num = 0
    column_num = 0
    for rowe in grid_pieces:
        for piece in rowe:
            current_coords = [row_num, column_num]
            if grid_pieces[row_num][column_num] == player:
                #check entire radius
                #check left
                def check_line(row_change, column_change):
                    if grid_pieces[row_num+row_change][column_num+column_change] == player:
                        if grid_pieces[row_num+(2*row_change)][column_num+(2*column_change)] == player:
                            if grid_pieces[row_num+(3*row_change)][column_num+(3*column_change)] == player:
                                if grid_pieces[row_num+(4*row_change)][column_num+(4*column_change)] == player:
                                    print("line found starting at " + str(current_coords))
                                    return(True)
                win = False
                        
                if column_num >= 4:
                    win = check_line(0,-1)
                if not win and column_num <= width - 5:
                    win = check_line(0,1)
                if not win and row_num >= 4:
                    win = check_line(-1,0)
                if not win and row_num <= width - 5:
                    win = check_line(1,0)
                if not win and column_num >= 4 and row_num >= 4:
                    win = check_line(-1,-1)
                if not win and column_num <= width - 5 and row_num >= 4:
                    win = check_line(-1,1)
                if not win and column_num >= 4 and row_num <= width - 5:
                    win = check_line(1,-1)
                if not win and column_num <= width - 5 and row_num <= width - 5:
                    win = check_line(1,1)
                
                if win:
                    return(True)
                else:
                    return(False)
               
            column_num += 1
        column_num = 0
        row_num += 1


width = 40
canvas = Canvas(root,width = width*20, height = width*20)
canvas.pack()

global grid
global grid_pieces

grid, grid_pieces = create_board(width)

root.title("5 in a row")


root.mainloop()
