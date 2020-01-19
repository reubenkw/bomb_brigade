from Classes.Game import Game
from Classes.Config import Cfg
import neat
import os
import pickle

POP_SIZE = 20
genome_num = 0


def output_interpreter(nn_output):
    commands = ["MOVE_UP", "MOVE_DOWN", "MOVE_LEFT", "MOVE_RIGHT", "HARVEST", "BOMB", "WALL"]

    max_index = nn_output.index(max(nn_output))
    if nn_output[max_index] > 0.5:
        return commands[max_index]
    else:
        return "NONE"


def eval_fitness(genomes, config):
    global genome_num

    nets = []
    names = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        names.append("AI" + str(genome_num))
        genome_num += 1

    for player1 in range(len(ge)):
        for player2 in range(player1 + 1, len(ge)):
            game = Game(names[player1], names[player2])

            p1_nn_input = []
            p2_nn_input = []
            map_linear = []
            game_state_repeat_cnt = 0
            game_state = []
            game_state_prev = []
            game_state_2prev = []
            while not game.game_over:
                map_linear.clear()
                for y in range(Cfg.map_y_tiles):
                    for x in range(Cfg.map_x_tiles):
                        map_linear.append(game.map.grid[x][y])

                p1_nn_input.clear()
                p1_nn_input.extend(map_linear)
                p1_nn_input.append(game.player1.bombs)
                p1_nn_input.append(game.player1.health)
                p1_nn_input.append(game.player1.walls)
                p1_nn_input.append(game.player1.x)
                p1_nn_input.append(game.player1.y)
                p1_nn_input.append(game.player2.x)
                p1_nn_input.append(game.player2.y)

                p2_nn_input.clear()
                p2_nn_input.extend(map_linear)
                p2_nn_input.append(game.player2.bombs)
                p2_nn_input.append(game.player2.health)
                p2_nn_input.append(game.player2.walls)
                p2_nn_input.append(game.player2.x)
                p2_nn_input.append(game.player2.y)
                p2_nn_input.append(game.player1.x)
                p2_nn_input.append(game.player1.y)

                p1_output = nets[player1].activate(p1_nn_input)
                p2_output = nets[player1].activate(p2_nn_input)

                p1_command = output_interpreter(p1_output)
                p2_command = output_interpreter(p2_output)

                # print(p1_command, p2_command)
                game.loop(p1_command, p2_command)

                game_state.clear()
                game_state.extend(map_linear)

                game_state.append(game.player1.bombs)
                game_state.append(game.player1.health)
                game_state.append(game.player1.walls)
                game_state.append(game.player1.x)
                game_state.append(game.player1.y)

                game_state.append(game.player2.bombs)
                game_state.append(game.player2.health)
                game_state.append(game.player2.walls)
                game_state.append(game.player2.x)
                game_state.append(game.player2.y)

                if game_state == game_state_prev or game_state == game_state_2prev:
                    game_state_repeat_cnt += 1
                    if game_state_repeat_cnt > 5:
                        game.game_over = True
                elif game_state_repeat_cnt > 0:
                    game_state_repeat_cnt = 0

                game_state_2prev.clear()
                game_state_2prev.extend(game_state_prev)

                game_state_prev.clear()
                game_state_prev.extend(game_state)

            print(game.outcome)
            if game.outcome == names[player1]:
                ge[player1].fitness += 20
            if game.outcome == names[player1]:
                ge[player2].fitness += 20
            if game.outcome == "Tie":
                ge[player1].fitness += min(game.player1.fitness, 10)
                ge[player2].fitness += min(game.player2.fitness, 10)
                print(min(game.player1.fitness, 10), min(game.player2.fitness, 10))

            del game


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_fitness, 500)

    pickle.dump(winner, open( "BestAI.p", "wb" ))

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NeatConfig')
    run(config_path)
