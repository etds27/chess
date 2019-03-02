#!/usr/bin/python3

import numpy as np
import sys
from piece_moves import *
from copy import deepcopy
import tkinter as tk
import pprint

class piece:
    mapping = {
    0:'',
    1:'Pawn',
    2:'Rook',
    3:'Knight',
    4:'Bishop',
    5:'Queen',
    6:'King'
    }

    def __init__(self,player,num,row,col):
        self.piece_type = piece.mapping[abs(num)]
        self.owner, self.row, self.col, self.num = player, row, col, num
        self.alive = True





class chess(tk.Tk):
    def __init__(self):
        #tk.Tk.__init__(self)
        #self.geometry("800x800+0+0")
        #self.winfo_toplevel().title("Chess")


        self.grid = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        #self.gui = {}
        #self.board_frame = tk.Frame(self)
        #self.board_frame.grid(row=0,column=0)
        #self.grid = np.array
        wpieces = ['w1p1','w1p2','w1p3','w1p4','w1p5','w1p6','w1p7','w1p8', \
                  'w2p1','w3p2','w4p3','w5p4','w6p5','w4p6','w3p7','w2p8']
        bpieces = ['b1p1','b1p2','b1p3','b1p4','b1p5','b1p6','b1p7','b1p8', \
                  'b2p1','b3p2','b4p3','b5p4','b6p5','b4p6','b3p7','b2p8']

        i = 0
        j = 1
        self.whites = []
        self.blacks = []
        self.white_gy = []
        self.black_gy = []
        self.brd = []
        for white,black in zip(wpieces,bpieces):
            a = piece(1,int(white[1]),j,7 - i)
            b = piece(-1,-int(black[1]),7 - j,7 - i)

            self.whites.append(a)
            self.blacks.append(b)

            i+=1
            if i == 8:
                i = 0
                j-= 1
        #print (whites,blacks)


        self.turn = 1
        self.white = 1
        self.black = -1




    def run(self):
        self.classes_to_grid()

        #for c,row in enumerate(self.grid):
        #    self.gui[c] = {}
        #    for d,col in enumerate(row):
        #        self.gui[c][d]=tk.Button(self.board_frame,text=piece.mapping[abs(col)],\
        #            height=4,width=8,anchor='c',bg='black',fg='white',command= lambda row=c,col=d :self.check_piece_move(row,col))
        #        self.gui[c][d].grid(row=c,column=d,sticky='news')
        #    self.grid_columnconfigure(c)
        #    self.grid_rowconfigure(c)

        #pprint.pprint(self.gui)
        #self.mainloop()
        while True:
            self.choose_move()

    def choose_move(self):
        print("########################################")
        self.print_board()
        print("########################################")
        row,col = str(input("Choose row,column (r,c): ")).split(',')

        self.check_piece_move(int(row),int(col))


    #Writes the pieces to the board grid
    def classes_to_grid(self):
        for white,black in zip(self.whites,self.blacks):
            self.grid[white.row, white.col] = white.num
            self.grid[black.row, black.col] = black.num

    #Checks what piece was selected and calls that pieces specific moving method
    def check_piece_move(self,row,col):
        print(row,col)
        piq = 0
        for pi in self.whites+self.blacks:
            if pi.row == row and pi.col == col and pi.owner == self.turn:
                piq = pi
                break
        if piq != 0:
            if abs(pi.num) == 1:
                print("PAWN")
                pmoves = pawn_move(row,col,self.grid,self.turn)
            if abs(pi.num) == 2:
                print("ROOK")
                pmoves = rook_move(row,col,self.grid,self.turn)
            if abs(pi.num) == 3:
                print("KNIGHT")
                pmoves = knight_move(row,col,self.grid,self.turn)
            if abs(pi.num) == 4:
                print("BISHOP")
                pmoves = bishop_move(row,col,self.grid,self.turn)
            if abs(pi.num) == 5:
                print("QUEEN")
                pmoves = queen_move(row,col,self.grid,self.turn)
            if abs(pi.num) == 6:
                print("KING")
                pmoves = king_move(row,col,self.grid,self.turn)

            self.place_check([row,col],pmoves)
        else:
            print ("Choose a space with a piece on it")
            self.choose_move()

    #Takes in list of possible coordinates to move selected piece. Checks which moves are valid. 99 = Open. 50 = Kill
    def place_check(self,orig,pmoves):
        cnt = 1
        apmove = []
        for pmove in pmoves:

            i,j = pmove[0],pmove[1]
            if self.grid[pmove[0]][pmove[1]] == 0:
                self.grid[i,j] = '99'
                print('%i)%i,%i' % (cnt ,i,j))
                apmove.append([i,j,99])
                cnt+=1
            elif self.is_enemy(self.turn,self.grid[i][j]):
                num = self.grid[i][j]
                self.grid[i,j] = '50'
                print ('%i)%i,%i Kill %s' % (cnt , i,j,self.grid[i][j]))
                apmove.append([i,j,50,num])
                cnt+=1
            else:
                self.grid[i,j] = self.grid[orig[0]][orig[1]]
            #print(apmove)
        self.print_board()
        if apmove == []:
            print ("Piece cannot move. Choose another")
            self.choose_move()
        else:
            try:
                #for ap in apmove:
                #    self.gui_move(ap[0],ap[1],ap[2])
                ans = int(input('Choose Move:\n'))
                mover = apmove.pop(ans-1)
                self.remove_pmoves(mover,apmove)
                self.move_piece(orig,mover)
            except ValueError:
                self.remove_pmoves([0,0,0],apmove)
                self.choose_move()



    def move_piece(self,orig,move):
        #Find object at coordinate
        for pi in self.whites+self.blacks:
            if pi.row == move[0] and pi.col == move[1]:
                pi.alive = False
                self.update_graveyard(pi)
            if pi.row == orig[0] and pi.col == orig[1]:
                pi.row, pi.col = move[0], move[1]
                self.grid[pi.row, pi.col] = pi.num
        self.grid[orig[0], orig[1]] = 0
        #self.print_board()
        self.turn = self.turn * -1

    def update_graveyard(self,pi):
        if pi.num == 6:
            print ("%i won!" % self.turn)
            exit()
        if pi.owner == 1:
            self.white_gy.append(pi)
        elif pi.owner == -1:
            self.black_gy.append(pi)

    def remove_pmoves(self,amov,apmove):
        for mov in apmove:
            if mov != amov:
                if int(self.grid[mov[0],mov[1]]) == 99:
                    #self.gui_move(mov[0],mov[1],0)
                    self.grid[mov[0],mov[1]] = 0
                elif mov[2] == 50:
                    self.grid[mov[0],mov[1]] = mov[3]
                    #self.gui_move(mov[0],mov[1],mov[3])

    #Need to create list of actual possible moves
    @staticmethod
    def is_enemy(turn,enemy):
        if turn == 1 and enemy < 0:
            return True
        elif turn == -1 and enemy > 0:
            return True
        return False

    def print_board(self):
        sys.stdout.write('   0  1  2  3  4  5  6  7\n_________________________\n')
        sys.stdout.flush()
        for c,x in enumerate(self.grid):
            #print(x)
            sys.stdout.write(str(c)+'|')
            sys.stdout.flush()
            for y in x:
                sys.stdout.write('%02s ' % (str(y)))
                sys.stdout.flush()
            print()

    #def gui_move(self,row,col,type):
    #    if type == 99:
    #        color = "blue"
    #    elif type == 50:
    #        color == "green"
    #    elif type == 0:
    #        color == "black"
    #    self.gui[row][col].configure(bg=color)
    #    pass
    #def update_gui(self):


chess_game = chess()
chess_game.run()
