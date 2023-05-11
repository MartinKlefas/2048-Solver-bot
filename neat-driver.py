import os
import random
import math
import sys
import neat
import headless_puzzle

def remove(index):
    players.pop(index)
    ge.pop(index)
    nets.pop(index)

def eval_genomes(genomes, config):
    global players, ge, nets
    players = []
    ge = []  # genome of each game player
    nets = [] # neural network of the player



    for genome_id, genome in genomes:
        players.append(headless_puzzle.init())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True

    while run:

        if len(players) == 0:
            break

        
        for i, player in enumerate(players):
            output = nets[i].activate(headless_puzzle.toList(player))
            
            direction = math.floor(output[0] * 4 - 1e-10)
            players[i], state, score = headless_puzzle.move(direction,player)
            if state != "not over":
                ge[i].fitness = score
                remove(i)








# Setup the NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)