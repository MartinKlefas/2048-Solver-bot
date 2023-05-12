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
    print(f"Generation: {generation_number}")
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
                log_line(f"{generation_number}, {dead}, {score}")
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

def log_line(text: str):
    with open('log.csv', 'a') as the_file:
        the_file.write(f"{text}\n")

def init_log():
    with open("log.csv","w") as the_file:
        the_file.write("Generation, Player, Score\n")

if __name__ == '__main__':
    init_log()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)


