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
    global players, ge, nets, generation_number
    generation_number +=1
    #print(f"Generation Number: {generation_number}")
    players = []
    ge = []  # genome of each game player
    nets = [] # neural network of the player

    dead = 0

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
            direction = math.floor(abs(output[0]) * (4 - 1e-10))
            players[i], state, score = headless_puzzle.move(direction,player,dumbPlayer=True)
            
            if state != "not over":
                dead +=1
                print(f"{generation_number}, {dead}, {score}")
                #print(f"Player {dead} died.")
                ge[i].fitness = score
                remove(i)








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
    