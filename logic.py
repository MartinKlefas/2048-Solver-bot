

import random
import constants as c



def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix



def add_two(mat):
    if empty_cells(mat): # if there's space, put in a 2
        zero_positions = [(i, j) for i, row in enumerate(mat) for j, element in enumerate(row) if element == 0]
        zero_position = random.choice(zero_positions)
        mat[zero_position[0]][zero_position[1]] = 2
        
    #otherwise, just return the old matrix
    return mat

def empty_cells(mat):
    return any(0 in sublist for sublist in mat)

def game_state(mat, dumbPlayer: bool = False):
    # check for win cell
    if any(2048 in sublist for sublist in mat):
        return 'win'
    # check for any zero entries
    if empty_cells(mat):
        return 'not over'
    
    if not dumbPlayer: # using neat, the player can be so stupid that they don't see two touching blocks and end up having "not really lost" 
                       # - but being too dumb to know it and still mashing the down arrow... endlessly... never dying, but never winning either.
                       # if we just assume that a "dumb" neat player is dead as soon as there's no "0" cells on the board then this stalemate won't happen
                    
        # check for same values in cells that touch each other
        for i in range(len(mat)-1):
            # intentionally reduced to check the row on the right and below
            # more elegant to use exceptions but most likely this will be their solution
            for j in range(len(mat[0])-1):
                if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                    return 'not over'
        for k in range(len(mat)-1):  # to check the left/right entries on the last row
            if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
                return 'not over'
        for j in range(len(mat)-1):  # check up/down entries on last column
            if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
                return 'not over'
            
    
    return 'lose'




def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new



def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new



def cover_up(mat):
    new = []
    for j in range(c.GRID_LEN):
        partial_new = []
        for i in range(c.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done

def up(game):
    
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done

def down(game):
    
    # return matrix after shifting down
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done

def left(game):
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done

def right(game):
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done

def score(mat):
    score = 0
    for list in mat:
        for element in list:
            score += element
    
    return score