import random

import headless_puzzle

finalScores = []
totalGames = 500

for i in range(1,totalGames):
    Matrix = headless_puzzle.init()
    KeepPlaying = True
    turns = 0
    while KeepPlaying:
        turns += 1
        nextDirection = random.randint(0,3)
        Matrix, gameState, score = headless_puzzle.move(nextDirection, Matrix)
        #print(f"turn {turns}, score {score}")
        if gameState != 'not over':
            finalScores.append(score)
            KeepPlaying = False


print(f"Games over. From {totalGames} tries the best score was: {max(finalScores)}")