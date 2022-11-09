import tkinter as tk
from tkinter import *
import copy
import numpy as np


def print_board(bo):        #This first function is for printing sudoku boards in the terminal. After the addition of the tkinter GUI, its obselete.
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - + - - - + - - -") #tells us to add a row of  - on
                                                # every third row
        for j in range(len(bo[i])):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            if j == 8:
                if bo[i][j] == 0:
                    print(".")
                else:
                    print(str(bo[i][j])) #we have to add this case so that it doesn't print the space rows on the same line
            else:
                if bo[i][j] == 0:
                    print("." + " ", end = "")
                else:
                    print(str(bo[i][j]) + " ", end ="")

def valid_check(bo):
    target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    score = 0
    for n in range(len(target)):
        num = target[n]
        # print("This is the ", end = "")
        # print(num, end = "")
        # print(" section.")
        for i in range(len(bo)):
            row = bo[i] # define row

            col = [0]*len(bo)
            for j in range(len(bo)):
                col[j] = bo[j][i] # defines col (column) fairly straightforward

             # defining the i'th block will be a little bit of a bitch
            if i < 3:
                block = bo[0][3*i:(3*i)+3] + bo[1][3*i:(3*i)+3] + bo[2][3*i:(3*i)+3]
            if i >=3 and i < 6:
                block = bo[3][(3*i)-9:(3*i)-6] + bo[4][(3*i)-9:(3*i)-6] + bo[5][(3*i)-9:(3*i)-6]
            if i >= 6 and i < 9:
                block = bo[6][(3*i)-18:(3*i)-15] + bo[7][(3*i)-18:(3*i)-15] + bo[8][(3*i)-18:(3*i)-15]



            if row.count(num) > 1 or col.count(num) > 1 or block.count(num) > 1:
                score += 1
                #we add a penalty score if any of the conditions break

    if score == 0:
        return True
    else:
        return False

def find_empties(bo):
    coords = []
    for i in range(len(bo)):
        for j in range(len(bo[i])):
            if bo[i][j] == 0:
                coords.append([i,j])
    return coords

def solved_check(bo):
    score = 0
    target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(bo)):
        row = bo[i] # define row

        col = [0]*len(bo)
        for j in range(len(bo)):
            col[j] = bo[j][i] # defines col (column) fairly straightforward

         # defining the i'th block will be a little bit of a bitch
        if i < 3:
            block = bo[0][3*i:(3*i)+3] + bo[1][3*i:(3*i)+3] + bo[2][3*i:(3*i)+3]
        if i >=3 and i < 6:
            block = bo[3][(3*i)-9:(3*i)-6] + bo[4][(3*i)-9:(3*i)-6] + bo[5][(3*i)-9:(3*i)-6]
        if i >= 6 and i < 9:
            block = bo[6][(3*i)-18:(3*i)-15] + bo[7][(3*i)-18:(3*i)-15] + bo[8][(3*i)-18:(3*i)-15]

        srow = sorted(row)
        scol = sorted(col)
        sblock = sorted(block)

        if srow == target and scol == target and sblock == target:
            score += 1
    if score == 9:
        return True
    else:
        return False

def solver(bo):
    newbo=copy.deepcopy(bo)
    empties = find_empties(newbo)
    i = 0
    while not solved_check(newbo):
        newbo[empties[i][0]][empties[i][1]] += 1
        if newbo[empties[i][0]][empties[i][1]] == 10:
            newbo[empties[i][0]][empties[i][1]] = 0
            i -= 1
        elif valid_check(newbo):
            i += 1
    return newbo

#These boarrd are just test boards for testing the algorithm works.
# board = [
#         [7, 8, 0, 4, 0, 0, 1, 2, 0],
#         [6, 0, 0, 0, 7, 5, 0, 0, 9],
#         [0, 0, 0, 6, 0, 1, 0, 7, 8],
#         [0, 0, 7, 0, 4, 0, 2, 6, 0],
#         [0, 0, 1, 0, 5, 0, 9, 3, 0],
#         [9, 0, 4, 0, 6, 0, 0, 0, 5],
#         [0, 7, 0, 3, 0, 0, 0, 1, 2],
#         [1, 2, 0, 0, 0, 7, 4, 0, 0]
#     ]


# board_2 = [
#         [0, 0, 5, 0, 0, 0, 8, 0, 0],
#         [8, 1, 6, 0, 0, 5, 4, 2, 7],
#         [7, 0, 2, 6, 0, 0, 0, 1, 9],
#         [2, 0, 0, 0, 0, 7, 3, 0, 1],
#         [6, 9, 0, 1, 0, 8, 7, 0, 0],
#         [3, 7, 1, 5, 0, 0, 0, 4, 0],
#         [0, 6, 0, 9, 0, 2, 0, 0, 0],
#         [1, 0, 3, 0, 4, 0, 9, 7, 0],
#         [5, 8, 0, 7, 0, 0, 2, 6, 4]
#     ]



#gui begins here
root = Tk()
root.title("Sudoku solver")
root.resizable(False,False)

#This here is all just drawing the background
canvas = tk.Canvas(root, height=800, width=800, bg='DarkSeaGreen')
canvas.pack()
canvas.create_rectangle(100,100,700,700, fill='white', width=5)
canvas.create_line(100,300,700,300, fill="black", width=5)
canvas.create_line(100,500,700,500, fill="black", width=5)
canvas.create_line(300,100,300,700, fill="black", width=5)
canvas.create_line(500,100,500,700, fill="black", width=5)

for i in range(3):
    canvas.create_line(100+(200*i)+66,100,100+(200*i)+66,700, fill='black', width=1)
for i in range(3):
    canvas.create_line(100+(200*i)+132,100,100+(200*i)+132,700, fill='black', width=1)
for i in range(3):
    canvas.create_line(100,100+(200*i)+66,700,100+(200*i)+66, fill='black', width=1)
for i in range(3):
    canvas.create_line(100,100+(200*i)+132,700,100+(200*i)+132, fill='black', width=1)

charlie = Label(root, font=('FranklinGothicHeavy 22'), text = "Charlie's Sudoku Solver")
charlie.place(x=0,y=767)

disclaimer = Label(root, font=('FranklinGothicHeavy 10'), text = "**some very crazy inputs may lead to problems**", fg='red')
disclaimer.place(x=514,y=780)

#itd probably be worth making something which takes i,j input and turns it into normal
ijconverter =[]
for i in range(9):
    for j in range(9):
        ijconverter.append([i,j])

labels=[]


def validate(P):
    if len(P) == 0:
        # empty Entry is ok
        return True
    elif len(P) == 1 and P.isdigit() and int(P)>0:
        # Entry with 1 digit is ok
        return True
    else:
        # Anything else, reject it
        return False

vcmd = (root.register(validate), '%P')

global display_board
display_board=np.zeros((9,9), dtype=int)


def initialise():
    global entries
    entries=[]
    for i in range(9):
        for j in range(9):
            tmp=Entry(root, width=1, font=('FranklinGothicHeavy 30'), borderwidth=0, validate="key", validatecommand=vcmd)                    
            tmp.place(x=(120+(66.5*i)),y=(115+(66*j)))
            entries.append(tmp)



def create_label(sol_board):
    global labels
    for label in labels: label.destroy()
    labels=[]
    for i in range(9):
        for j in range(9):
            tmp=Label(root, width=1, font=('FranklinGothicHeavy 30'), text=str(sol_board[i][j]), bg='white')
            tmp.place(x=(118+(66.5*i)),y=(113+(66*j)))
            labels.append(tmp)



def start_new():
    global labels
    try:
        ermsg.destroy()
    except:
        pass
    for label in labels: label.destroy()
    labels=[]
    for entry in entries: entry.destroy()
    initialise()

def show_error():
    global ermsg
    ermsg=Label(root, text="Please enter a valid board.", font=('FranklinGothicHeavy 15'), fg ='red')
    ermsg.place(x=310,y=50)
    labels.append(ermsg)

def solve():
    aboard=np.zeros((9,9), dtype=int)
    try:
        for i in range(9):
            for j in range(9):
                entry_to_use=ijconverter.index([i,j])
                if not entries[entry_to_use].get():
                    aboard[i][j]=0
                else:
                    aboard[i][j]=int(entries[entry_to_use].get())
        board=aboard.tolist()
        
    
        if valid_check(board) and aboard.max()<10 and aboard.min()>-1:
            for entry in entries: entry.destroy()
            display_board=solver(board)
            create_label(display_board)
        else:
            show_error()
                
    except:
        show_error()
        pass

    

inputnew_button=Button(root, text = "Input new", command=start_new, font=('FranklinGothicHeavy 20'))
canvas.create_window(170, 60, window=inputnew_button)
inputnew_button=Button(root, text = "Solve", command=solve, font=('FranklinGothicHeavy 20'))
canvas.create_window(656, 60, window=inputnew_button)

initialise()

root.mainloop()