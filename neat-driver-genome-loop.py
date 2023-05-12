import os
import random
import math
import sys
import neat
import headless_puzzle
from collections import deque
from functools import partial

from concurrent.futures import ProcessPoolExecutor

def eval_genomes(genomes, config):
    global generation_number, dead
    generation_number +=1
    print(f"Generation Number: {generation_number}")
    
    
    dead = 0
    
    ge = []
    for genome in genomes:
        ge.append(genome)

    func = partial(play_full_game, config, generation_number)

    chunks = list(chunkify(ge, len(ge) // 5))
   



    with ProcessPoolExecutor() as executor:
        results_list = executor.map(func, chunks)

    write_log(results_list)
    
    print("got here")

def play_full_game(config, generation_number, genomes):
    results = []
    
    #we can use a score history to check for a stalemate, and thereby pretend the players are not "dumb" anymore
    for genome_id, genome in genomes:
        player = headless_puzzle.init()
        scoreHistory = None
        scoreHistory = deque(maxlen=50)  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        turns = 0
        
        while True:
            turns += 1
            output = net.activate(headless_puzzle.toList(player))
            direction = math.floor(abs(output[0]) * (4 - 1e-10))
            player, state, score = headless_puzzle.move(direction,player,dumbPlayer=False)
            scoreHistory.append(score)
            #print(f"stat: {state}")
            #print(f"turns {turns}")
            if state != "not over" or (turns > 50 and len(set(scoreHistory)) == 1): # if the last 50 scores are the same, we've hit a stalemate.
                results.append(f"{generation_number}, {genome_id}, {score}, {turns}")
                genome.fitness = score
                break

    return results


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


def log_line(text: str):
    with open('log.csv', 'a') as the_file:
        the_file.write(f"{text}\n")

def init_log():
    with open("log.csv","w") as the_file:
        the_file.write("Generation, Genome ID, Score, Turns\n")

if __name__ == '__main__':
    init_log()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    