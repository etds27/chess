#!/usr/bin/python3

'''
ISSUES:
    Complete: All spaces go white when slecting piece to move. Stopped program from changing bg
    Complete: Cannot move piece after selecting, then deselecting piece. Properly reset self.grid after deselecting piece
    Complete: After taking piece, piece that killed other can be moved as other player. Added self.alive == true to piece move check
'''

import numpy as np
import sys
from piece_moves import *
from copy import deepcopy
import tkinter as tk
import pprint
import preferences
import os

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
        tk.Tk.__init__(self)
        self.geometry("1100x875+0+0")
        self.winfo_toplevel().title("Chess")

        #self.god_button = tk.Button(self,command= lambda t = 'test' :self.ressurect(t))
        #self.god_button.place(relx=.1,rely=.1)

        self.grid = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
        self.gui = {}
        self.board_frame = tk.Frame(self)
        self.board_frame.place(rely=.5,relx=.5,relheight=.75,relwidth=.75,anchor='c')
        self.min_frame = tk.Frame(self.board_frame)
        self.min_frame.place( anchor="c", relx=.5, rely=.5)
        self.p1_graveyard = tk.Frame(self)
        self.p2_graveyard = tk.Frame(self)
        self.p1_graveyard.place(relx=0.05,relwidth=0.1,rely=.5,relheight=.75,anchor='c')
        self.p2_graveyard.place(relx=0.95,relwidth=0.1,rely=.5,relheight=.75,anchor='c')

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
        #C1 "tan"
        #C2 "burlywood4"
        pref_file=os.path.dirname(sys.argv[0]) + "/chess_prefs.json"
        self.prefs = preferences.preferences(pref_file)
        self.prefs.make_default( checker1="tan", checker2="burlywood4", player1="black", player2="white")
        #self.prefs.change_pref( checker1="tan", checker2="burlywood4", player1="black", player2="white")




    def run(self):
        self.classes_to_grid()
        fg = self.prefs.read_pref("general","player1","player2")
        for c,row in enumerate(self.grid):
            self.gui[c] = {}
            for d,col in enumerate(row):
                if col == 0:
                    state = "disabled"
                else:
                    state = "normal"
                if col < 0:
                    fgc = fg[0]
                    anc='sw'
                else:
                    fgc = fg[1]
                    anc='ne'
                self.gui[c][d]=tk.Button(self.min_frame,text=piece.mapping[abs(col)],\
                    height=4,width=8,anchor=anc,bg=self.checker(c,d),fg=fgc,command= lambda row=c,col=d :self.check_piece_move(row,col), state = state)
                self.gui[c][d].grid(row=c,column=d,sticky='news')
            self.grid_columnconfigure(c)
            self.grid_rowconfigure(c)

        #pprint.pprint(self.gui)
        self.mainloop()
        #while True:
        #    self.choose_move()

    def choose_move(self):
        print("########################################")
        self.print_board()
        print("########################################")
        #row,col = str(input("Choose row,column (r,c): ")).split(',')

        self.check_piece_move(int(row),int(col))


    #Writes the pieces to the board grid
    def classes_to_grid(self):
        for white,black in zip(self.whites,self.blacks):
            self.grid[white.row, white.col] = white.num
            self.grid[black.row, black.col] = black.num

    #Checks what piece was selected and calls that pieces specific moving method
    def check_piece_move(self,row,col):
        #print(row,col)
        piq = 0
        for pi in self.whites+self.blacks:
            #print(row,pi.row,col,pi.col,self.turn,pi.owner)
            if pi.row == row and pi.col == col and pi.owner == self.turn and pi.alive == True:
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
            #self.gui[row][col].flash()
            self.flash_square(row,col,"BAD")

            #self.choose_move()
    def flash_square(self,row,col,error):
        if error == "BAD":
            bcolor = "red"
        if error == "WARN":
            bcolor = "yellow"
        self.gui[row][col].config(bg = bcolor,activebackground=bcolor)
        self.after(500, lambda: self.gui[row][col].config(bg = self.checker(row,col),activebackground='white'))

    #Takes in list of possible coordinates to move selected piece. Checks which moves are valid. 99 = Open. 50 = Kill
    def place_check(self,orig,pmoves):
        cnt = 1
        apmove = []
        for pmove in pmoves:

            i,j = pmove[0],pmove[1]
            if self.grid[pmove[0]][pmove[1]] == 0:
                self.grid[i,j] = '99'
                print('%i)%i,%i' % (cnt ,i,j))
                apmove.append([i,j,99,0])
                cnt+=1
            elif self.is_enemy(self.turn,self.grid[i][j]):
                num = self.grid[i][j]
                self.grid[i,j] = 50
                print ('%i)%i,%i Kill %s' % (cnt , i,j,self.grid[i][j]))
                apmove.append([i,j,50,num])
                cnt+=1
            else:
                self.grid[i,j] = self.grid[orig[0]][orig[1]]
            #print(apmove)
        self.print_board()
        if apmove == []:
            print ("Piece cannot move. Choose another")
            self.flash_square(orig[0],orig[1],"BAD")

            #self.choose_move()
        else:
            try:
                self.gui_pmove(orig,apmove)
                #ans = int(input('Choose Move:\n'))
                #mover = apmove.pop(ans-1)
                #self.remove_pmoves(mover,apmove)
                #self.move_piece(orig,mover)
            except ValueError:
                self.remove_pmoves([0,0,0],apmove)
                #self.choose_move()



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
        print (pi.num,self.turn)
        print (piece.mapping[pi.num * self.turn * -1])
        if self.turn == 1:
            t_b= tk.Button(self.p1_graveyard,bg='red',text=piece.mapping[abs(pi.num)],state='disabled')
            t_b.pack(side = "bottom")
        else:
            t_b= tk.Button(self.p2_graveyard,bg='blue',text=piece.mapping[abs(pi.num)],state='disabled')
            t_b.pack(side = "bottom")
            print("children:",self.p2_graveyard.winfo_children())
        pi.alive = False
        if pi.num * self.turn * -1 == 6:
            print ("%i won!" % self.turn)
            exit()
        if pi.owner == 1:
            self.white_gy.append(pi)
        elif pi.owner == -1:
            self.black_gy.append(pi)
            '''
    def open_graveyard(self,pi):
        if self.turn == 1:
            t_frm = self.p1_graveyard
        else:
            t_frm = self.p2_graveyard
        print("children:",self.p2_graveyard.winfo_children())
        #print("children:",self.min_frame.winfo_children())
        for child in t_frm.winfo_children():
            piece_name = piece.mapping[]
            child.configure(state="normal",command= lambda c=child : self.ressurect(pi,c)
    def ressurect(self,pawn,zombie):
        print
        '''
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

    #Changing GUI to relect the possible moves for selected piece
    def gui_pmove(self,orig,apmove):

        #for k,v in self.gui.items():
        #    for l,w in v.items():
        #        self.gui[k][l].configure(bg="white",state = "disabled")
        for mov in apmove:
            if self.grid[mov[0],mov[1]] == 99:
                color = "blue"
            elif self.grid[mov[0],mov[1]] == 50:
                color = "green"
            elif self.grid[mov[0],mov[1]] == 0:
                color = "black"
            else:
                color = "red"
            self.gui[mov[0]][mov[1]].configure(bg=color,state = "normal",command=lambda mov=mov : self.gui_move(orig,mov,apmove) )
            self.gui[orig[0]][orig[1]].configure(command=lambda:self.return_to_normal(),state="normal")

    def gui_move(self,orig,move,apmove):
        #print (apmove)
        apmove.remove(move)
        for pmove in apmove:
                self.grid[pmove[0],pmove[1]]=pmove[3]
        onum = self.grid[orig[0],orig[1]]
        nnum = self.grid[move[0],move[1]]
        if nnum != 0:
            for pi in self.whites+self.blacks:
                if pi.row == move[0] and pi.col == move[1] and pi.alive:
                    self.update_graveyard(pi)
                if pi.row == orig[0] and pi.col == orig[1]:
                    pi.row, pi.col = move[0], move[1]
        self.grid[orig[0],orig[1]] = 0
        self.grid[move[0],move[1]] = onum

        self.gui[move[0]][move[1]].configure(text=piece.mapping[onum * self.turn])
        self.gui[orig[0]][orig[1]].configure(text=piece.mapping[0])




        self.turn = self.turn * -1
        self.print_board()
        self.return_to_normal()
        #for pi in self.whites+self.blacks:
        #    print("%s: row:%i col:%i, alive:%r" % (pi.mapping[abs(pi.num)], pi.row, pi.col, pi.alive))

    def return_to_normal(self):
        fg = self.prefs.read_pref("general","player1","player2")
        #Clears board
        for c,row in enumerate(self.grid):
            for d,col in enumerate(row):
                self.grid[c,d]=0
        #Places mapping number at each position
        for pi in self.whites + self.blacks:
            if pi.alive:
                self.grid[pi.row,pi.col] = pi.num
        #self.print_board()

        for c,row in enumerate(self.grid):
            for d,col in enumerate(row):
                #self.print_board()
                if col == 0:
                    state = "disabled"
                else:
                    state = "normal"
                if col < 0:
                    self.gui[c][d].configure(fg=fg[0],command= lambda row=c,col=d :self.check_piece_move(row,col), state = state)
                elif col > 0:
                    self.gui[c][d].configure(fg=fg[1],command= lambda row=c,col=d :self.check_piece_move(row,col), state = state)
                else:
                    self.gui[c][d].configure(command= lambda row=c,col=d :self.check_piece_move(row,col), state = state)

                self.gui[c][d].configure(bg=self.checker(c,d))


        self.print_board()


    def checker(self,row,col):
        if ( row * 7 + col ) % 2:
            return self.prefs.read_pref("general","checker1")
        else:
            return self.prefs.read_pref("general","checker2")
            #return "firebrick4"

chess_game = chess()
chess_game.run()
