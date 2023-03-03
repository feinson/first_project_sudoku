import tkinter as tk
from tkinter import *
from solving import Board
import numpy as np


if __name__ == "__main__":
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
    display_board = np.zeros((9,9), dtype=int)


    def initialise():
        global entries
        entries=[]
        for i in range(9):
            for j in range(9):
                tmp=Entry(root, width=1, font=('FranklinGothicHeavy 30'), borderwidth=0, validate="key", validatecommand=vcmd)                    
                tmp.place(x=(120+(66.5*i)),y=(115+(66*j)))
                entries.append(tmp)



    def create_label(sol_board: Board):
        global labels
        for label in labels: label.destroy()
        labels=[]
        for i in range(9):
            for j in range(9):
                tmp=Label(root, width=1, font=('FranklinGothicHeavy 30'), text=str(sol_board[i, j]), bg='white')
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
        aboard = np.zeros((9,9), dtype=int)
        try:
            for i in range(9):
                for j in range(9):
                    entry_to_use = ijconverter.index([i,j])
                    if not entries[entry_to_use].get():
                        aboard[i][j] = 0
                    else:
                        aboard[i][j] = int(entries[entry_to_use].get())
            bo = Board(aboard.tolist())
            
            if bo.valid_check() and aboard.max()<10 and aboard.min()>-1:
                for entry in entries: entry.destroy()
                display_board = bo.solver()
                create_label(display_board)
            else:
                show_error()
                    
        except:
            print("here2")
            show_error()
            pass


    inputnew_button=Button(root, text = "Input new", command=start_new, font=('FranklinGothicHeavy 20'))
    canvas.create_window(170, 60, window=inputnew_button)
    inputnew_button=Button(root, text = "Solve", command=solve, font=('FranklinGothicHeavy 20'))
    canvas.create_window(656, 60, window=inputnew_button)

    initialise()

    root.mainloop()