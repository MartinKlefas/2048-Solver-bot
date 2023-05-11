import random
import logic
import constants as c

def gen():
    return random.randint(0, c.GRID_LEN - 1)


def init():
    return logic.new_game(c.GRID_LEN)
    

commands = {
            0: logic.up,
            1: logic.down,
            2: logic.left,
            3: logic.right,
}

def move(direction : int, gameMatrix):
    gameMatrix, done = commands[direction](game=gameMatrix)
    gameMatrix = logic.add_two(gameMatrix)

    return gameMatrix, logic.game_state(gameMatrix), logic.score(gameMatrix)

def toList(gameMatrix):
    return [item for sublist in gameMatrix for item in sublist]