import os
import random
import math
import sys
import neat
import headless_puzzle

def eval_genomes(genomes, config):
    global generation_number, dead
    generation_number +=1


    dead = 0

    for genome_id, genome in genomes:
        play_full_game(genome=genome,config=config)

def play_full_game(genome, config):
    global dead
    player = headless_puzzle.init()
        
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    while True:
        output = net.activate(headless_puzzle.toList(player))
        direction = math.floor(abs(output[0]) * (4 - 1e-10))
        player, state, score = headless_puzzle.move(direction,player,dumbPlayer=True)
        
        if state != "not over":
            dead +=1
            print(f"{generation_number}, {dead}, {score}")
            genome.fitness = score
            break






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


if __name__ == '__main__':
    print("Generation, Player, score")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    