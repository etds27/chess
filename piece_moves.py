#!/usr/bin/python3

pmoves=[]

#Pawn moving method. Can only move forward 1 unless at start. Or diagnol for a kill
def pawn_move(row,col,grid,turn):
    pmoves=[]
    if turn == 1 and row == 1:
        mov = 2 * turn
        pmoves.append([row + mov,col])
    elif turn == -1 and row == 6:
        mov = 2 * turn
        pmoves.append([row + mov,col])

    mov = 1 * turn

    if in_bounds(row + mov):
        pmoves.append([row + mov,col])

    #Pawn kill if enemy is 1 infront and to right or left
    if in_bounds(row + 1 * turn) and in_bounds(col + 1):
        if is_enemy(turn,grid[row + 1 * turn][col + 1]):
            pmoves.append([row + 1 * turn,col + 1])
    if in_bounds(row + 1 * turn) and in_bounds(col - 1):
        if is_enemy(turn,grid[row + 1 * turn][col - 1]):
            pmoves.append([row + 1 * turn,col - 1])
    return pmoves

#Rook moving method. Move in all directions until you hit board boundary, or sqaure that is not friend. If enemy dont look farther
def rook_move(row,col,grid,turn):
    pmoves=[]
    for sin in [-1,1]:
        i=1
        while True:
            if in_bounds(row + i * sin):
                siq = grid[row + i * sin,col]
                print(row + i * sin,col,siq)
                if siq == 0:
                    pmoves.append([row + i * sin,col])
                    i += 1
                elif is_enemy(turn,siq):
                    pmoves.append([row + i * sin,col])
                    i += 1
                    break
                else:
                    break
            else:
                break
    for sin in [-1,1]:
        i=1
        while True:
            if in_bounds(col + i * sin):
                siq = grid[row,col + i * sin]
                if siq == 0:
                    pmoves.append([row,col + i * sin])
                    i += 1
                elif is_enemy(turn,siq):
                    pmoves.append([row,col + i * sin])
                    i += 1
                    break
                else:
                    break
            else:
                break
    #print(pmoves)
    return pmoves

#Knight moving method. Able to move up 2 and over 1 in any direction
def knight_move(row,col,grid,turn):
    pmoves=[]
    for sin in [-2,2]:
        for cos in [-1,1]:
            if in_bounds(row + sin) and in_bounds(col + cos):
                if not is_friendly(turn,grid[row + sin,col + cos]):
                    pmoves.append([row+sin,col+cos])
    for sin in [-2,2]:
        for cos in [-1,1]:
            if in_bounds(row + cos) and in_bounds(col + sin):
                if not is_friendly(turn,grid[row + cos,col + sin]):
                    pmoves.append([row+cos,col+sin])
    return pmoves

#Bishop Move Method. First loop solves in QII and QIV. Second loop solves in QI and QIII
def bishop_move(row,col,grid,turn):
    pmoves=[]
    for sin in [-1,1]:
        i = 1
        while True:
            if in_bounds(row + i * sin) and in_bounds(col + i * sin) :
                siq = grid[row + i * sin][col + i * sin]
                if siq == 0:
                    pmoves.append([row + i * sin,col + i * sin])
                elif is_enemy(turn,siq):
                    pmoves.append([row + i * sin,col + i * sin])
                    break
                else:
                    break
                i = i + 1
            else:
                break
    for sin in [-1,1]:
        i = 1
        while True:
            if in_bounds(row - i * sin) and in_bounds(col + i * sin) :
                siq = grid[row - i * sin][col + i * sin]
                if siq == 0:
                    pmoves.append([row - i * sin,col + i * sin])
                elif is_enemy(turn,siq):
                    pmoves.append([row - i * sin,col + i * sin])
                    break
                else:
                    break
                i = i + 1
            else:
                break
    return pmoves

#Queen Move Method. Literally just a copy and paste of the rook_move and bishop move methods
def queen_move(row,col,grid,turn):
    pmoves=[]
    for sin in [-1,1]:
        i=1
        while True:
            if in_bounds(row + i * sin):
                siq = grid[row + i * sin,col]
                if siq == 0:
                    pmoves.append([row + i * sin,col])
                    i += 1
                elif is_enemy(turn,siq):
                    pmoves.append([row + i * sin,col])
                    i += 1
                    break
                else:
                    break
            else:
                break
    for sin in [-1,1]:
        i=1
        while True:
            if in_bounds(col + i * sin):
                siq = grid[row,col + i * sin]
                if siq == 0:
                    pmoves.append([row,col + i * sin])
                    i += 1
                elif is_enemy(turn,siq):
                    pmoves.append([row,col + i * sin])
                    i += 1
                    break
                else:
                    break
            else:
                break
    for sin in [-1,1]:
        i = 1
        while True:
            if in_bounds(row + i * sin) and in_bounds(col + i * sin) :
                siq = grid[row + i * sin][col + i * sin]
                if siq == 0:
                    pmoves.append([row + i * sin,col + i * sin])
                elif is_enemy(turn,siq):
                    pmoves.append([row + i * sin,col + i * sin])
                    break
                else:
                    break
                i = i + 1
            else:
                break
    for sin in [-1,1]:
        i = 1
        while True:
            if in_bounds(row - i * sin) and in_bounds(col + i * sin) :
                siq = grid[row - i * sin][col + i * sin]
                if siq == 0:
                    pmoves.append([row - i * sin,col + i * sin])
                elif is_enemy(turn,siq):
                    pmoves.append([row - i * sin,col + i * sin])
                    break
                else:
                    break
                i = i + 1
            else:
                break
    return pmoves

#King Move Method. Just a copy paste of knight_move, but the movement values were changed to 1,0 and 1,1
def king_move(row,col,grid,turn):
    pmoves=[]
    for sin in [-1,1]:
        for cos in [0,0]:
            if in_bounds(row + sin) and in_bounds(col + cos):
                if not is_friendly(turn,grid[row + cos,col + sin]):
                    pmoves.append([row+sin,col+cos])
    for sin in [-1,1]:
        for cos in [-1,1]:
            if in_bounds(row + cos) and in_bounds(col + sin):
                if not is_friendly(turn,grid[row + cos,col + sin]):
                    pmoves.append([row+cos,col+sin])
    return pmoves

def in_bounds(i):
    if i >= 0 and i<=7:
        return True
    return False

def is_enemy(turn,enemy):
    if turn == 1 and enemy < 0:
        return True
    elif turn == -1 and enemy > 0:
        return True
    return False

def is_friendly(turn,friend):
    if turn == 1 and friend > 0:
        return True
    elif turn == -1 and friend < 0:
        return True
    return False

if __name__ == "__main__":
    import numpy as np
    grid = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[-1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
    pawn_move(3,1,grid,1)
