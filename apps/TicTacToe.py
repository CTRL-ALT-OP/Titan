import tkinter as d3

global turn
turn = "r"

def create_board(_width):
    global page
    global grid
    global grid_pieces
    global width
    width = _width
    a = 0
    b = 0
    grid = []

    grid_pieces = []

    while a < width:
        row = []
        row_pieces = []
        while b < width:
            label = d3.Button(page.page_frame, bg = "black", activebackground = "dark grey", text = "  ", command = lambda _row = a, _column = b: object_pressed(_row, _column), font = ("Alien Encounters", 60, "bold"))
            label.place(x=b*100,y=a*100,height=100,width=100)
            row.append(label)
            row_pieces.append("")
            b += 1
        b = 0
        grid.append(row)
        grid_pieces.append(row_pieces)
        a += 1
    return(grid,grid_pieces)

def object_pressed(_row, _column):
    global width
    global page
    global grid
    global grid_pieces
    global turn
    
    if turn == 'r':
        if grid_pieces[_row][_column] != "R" and grid_pieces[_row][_column] != "B":
            turn = 'b'
            grid[_row][_column].configure(text = "X", fg = "red")
            grid_pieces[_row][_column] = "R"
            #print(grid_pieces)
            win_r = verify_board("R")
            if win_r:
                print("Red won the game!")
                btn = d3.Label(page.page_frame, text = "Red won!\nDo you want to play again?", fg = "lime green",
                               font = ("Alien Encounters", 14, "bold"), relief = "groove", bg = "black")
                btn.place(relx = 0.5, rely = 0.5, anchor = "center")
                def do(btn, btn_2):
                    btn.destroy()
                    btn_2.destroy()
                    global grid
                    global grid_pieces
                    for row in grid:
                        for piece in row:
                            piece.destroy()
                    grid = []
                    grid, grid_pieces = create_board(3)
                btn_2 = d3.Button(page.page_frame, text = "Yes",font = ("Alien Encounters", 30, "bold"),
                                  fg = "lime green", relief = "groove", bg = "black", activebackground = "dark grey")
                btn_2.configure(command = lambda bt1 = btn, bt2 = btn_2: do(bt1, bt2))
                btn_2.place(relx = 0.5, rely = 0.65, anchor = "center")
                
    elif turn == 'b':
        if grid_pieces[_row][_column] != "R" and grid_pieces[_row][_column] != "B":
            turn = 'r'
            grid[_row][_column].configure(text = "O", fg = "blue")
            grid_pieces[_row][_column] = "B"
            #print(grid_pieces)
            win_r = verify_board("B")
            if win_r:
                print("Blue won the game!")
                btn = d3.Label(page.page_frame, text = "Blue won!\nDo you want to play again?", fg = "lime green",
                               font = ("Alien Encounters", 14, "bold"), relief = "groove", bg = "black")
                btn.place(relx = 0.5, rely = 0.5, anchor = "center")
                def do(btn, btn_2):
                    btn.destroy()
                    btn_2.destroy()
                    global grid
                    global grid_pieces
                    for row in grid:
                        for piece in row:
                            piece.destroy()
                    grid = []
                    grid, grid_pieces = create_board(3)
                btn_2 = d3.Button(page.page_frame, text = "Yes",font = ("Alien Encounters", 30, "bold"),
                                  fg = "lime green", relief = "groove", bg = "black", activebackground = "dark grey")
                btn_2.configure(command = lambda bt1 = btn, bt2 = btn_2: do(bt1, bt2))
                btn_2.place(relx = 0.5, rely = 0.65, anchor = "center")
    
def verify_board(player):
    global page
    global width
    
    global grid
    global grid_pieces
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
                            print("line found starting at " + str(current_coords))
                            return(True)
                win = False
                        
                if column_num >= 2:
                    win = check_line(0,-1)
                if not win and column_num <= width - 3:
                    win = check_line(0,1)
                if not win and row_num >= 2:
                    win = check_line(-1,0)
                if not win and row_num <= width - 3:
                    win = check_line(1,0)
                if not win and column_num >= 2 and row_num >= 2:
                    win = check_line(-1,-1)
                if not win and column_num <= width - 3 and row_num >= 2:
                    win = check_line(-1,1)
                if not win and column_num >= 2 and row_num <= width - 3:
                    win = check_line(1,-1)
                if not win and column_num <= width - 3 and row_num <= width - 3:
                    win = check_line(1,1)
                
                if win:
                    return(True)
                else:
                    return(False)
               
            column_num += 1
        column_num = 0
        row_num += 1





def create(_page, root):
    global width
    global page
    page = _page
    width = 3
    
    global grid
    global grid_pieces
    
    grid, grid_pieces = create_board(width)

def destroy(page, root):
    page.page_frame.destroy()
