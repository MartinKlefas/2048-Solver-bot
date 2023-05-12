import os
import random
import math
import sys
import neat
import headless_puzzle
from collections import deque
from functools import partial
from itertools import chain

from concurrent.futures import ProcessPoolExecutor

def eval_genomes(genomes, config):
    global generation_number
    generation_number +=1
    print(f"Generation Number: {generation_number}")

    
    func = partial(play_full_game, config, generation_number)

    chunks = list(chunkify(genomes, len(genomes) // 10))
  
    with ProcessPoolExecutor() as executor:
        resultsList = list(executor.map(func, chunks))


    resultsTxt_lists = []
    resultsTuples_lists = []
    for item in resultsList:
        resultsTxt_lists.append(item[0])
        resultsTuples_lists.append(item[1])


    log_lines(list(chain.from_iterable(resultsTxt_lists)))
    
    resultsTuples = list(chain.from_iterable(resultsTuples_lists))

    genomeDict = dict(genomes)

    for key, value in resultsTuples:
        genomeDict[key].fitness = value


def play_full_game(config, generation_number, genomes):
    resultsTxt = []
    resultsTuples = []
    #we can use a score history to check for a stalemate, and thereby pretend the players are not "dumb" anymore
    for genome_id, genome in genomes:
        player = headless_puzzle.init()
        turnBefore = player
        direction = 0
        scoreHistory = None
        scoreHistory = deque(maxlen=50)  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        turns = 0
        
        while True:
            turns += 1
            inputsToNet = headless_puzzle.toList(player)
            inputsToNet.append(direction) # add in the last move
            inputsToNet.extend(headless_puzzle.toList(turnBefore))

            turnBefore = player

            output = net.activate(inputsToNet)
            direction = math.floor(abs(output[0]) * (4 - 1e-10))
            player, state, score = headless_puzzle.move(direction,player,dumbPlayer=False)
            scoreHistory.append(score)

            if state != "not over" or (turns > 50 and len(set(scoreHistory)) == 1): # if the last 50 scores are the same, we've hit a stalemate.
                resultsTxt.append(f"{generation_number}, {genome_id}, {score}, {turns}")
                resultsTuples.append((genome_id, score))
                break

    return  (resultsTxt, resultsTuples)


def chunkify(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]




# Setup the NEAT Neural Network
def run(config_path):
    global pop, generation_number
    
    generation_number = 0
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 5000)


def log_lines(text: list):
    with open('log.csv', 'a') as the_file:
        the_file.writelines(f"{item}\n" for item in text)

def init_log():
    with open("log.csv","w") as the_file:
        the_file.write("Generation, Genome ID, Score, Turns\n")

if __name__ == '__main__':
    init_log()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-longmem.txt')
    run(config_path)
    