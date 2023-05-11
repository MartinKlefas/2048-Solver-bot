import random

import headless_puzzle

Matrix = headless_puzzle.init()

KeepPlaying = True
turns = 0
while KeepPlaying:
    turns += 1
    nextDirection = random.randint(0,3)
    Matrix, gameState, score = headless_puzzle.move(nextDirection, Matrix)
    print(f"turn {turns}, score {score}")
    if gameState != 'not over':
        KeepPlaying = False

print(f"Game over, you {gameState}. Final score: {score}")