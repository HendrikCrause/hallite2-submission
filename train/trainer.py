import json
import random
import itertools

import numpy as np

from rnn.rnn import DeepRecurrentNeuralNet
from train.game_runner import run_halite_game, determine_ranks
from train.cleanup import cleanup_temp_folder

INITIAL_BATCH_SIZE = 64
ROUNDS_PER_BATCH_2 = 4
ROUNDS_PER_BATCH_4 = 3
SURVIVORS_PER_ROUND = 8
GENERATIONS = 10


def create_initial_batch(size=INITIAL_BATCH_SIZE):
    out = []
    for idx in range(size):
        name = create_name(0, idx)
        out.append(name)
        net = DeepRecurrentNeuralNet()
        write_bot_file(name, net)

    return out


def create_name(generation, idx):
    return str(generation) + '-' + str(idx)


def write_bot_file(name, net):
    with open('temp/' + name + '.bot', 'w') as write_file:
        write_file.write(json.dumps(net.get_structure()))


def read_bot_file(name):
    with open('temp/' + name + '.bot') as file:
        structure = json.loads(file.read())
    return structure


def split_into_chunks(batch, chunk_size):
    return [batch[x:x + chunk_size] for x in range(0, len(batch), chunk_size)]


def play_batch(bot_chunks):
    winners = []
    for chunk in bot_chunks:
        result = run_halite_game(chunk)
        ranks = determine_ranks(result, chunk)
        winners.append(ranks[1])
    return winners


def play_round(bots):
    results = dict([(bot, 0) for bot in bots])

    for _ in range(ROUNDS_PER_BATCH_2):
        random.shuffle(bots)
        chunks = split_into_chunks(bots, 2)
        winners = play_batch(chunks)
        for winner in winners:
            results[winner] += 1

    for _ in range(ROUNDS_PER_BATCH_4):
        random.shuffle(bots)
        chunks = split_into_chunks(bots, 4)
        winners = play_batch(chunks)
        for winner in winners:
            results[winner] += 1

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in sorted_results[:SURVIVORS_PER_ROUND]]


def offspring(bot1, bot2, bot3):
    bot1_structure = read_bot_file(bot1)
    bot2_structure = read_bot_file(bot2)
    bot3_structure = read_bot_file(bot3)

    new_structure = {}

    for layer in bot1_structure.keys():
        new_structure[layer] = {}

        for weight_vector_name in bot1_structure[layer].keys():
            new_structure[layer][weight_vector_name] = np.average(
                np.array([
                    bot1_structure[layer][weight_vector_name],
                    bot2_structure[layer][weight_vector_name],
                    bot3_structure[layer][weight_vector_name],
                ]), axis=0
            )

    return DeepRecurrentNeuralNet(new_structure)


def create_new_batch(survivors, generation):
    new_batch = [s for s in survivors]
    combinations = list(itertools.combinations(survivors, 3))
    for idx in range(len(combinations)):
        name = create_name(generation + 1, idx)
        child = offspring(combinations[idx][0], combinations[idx][1], combinations[idx][2])
        write_bot_file(name, child)
        new_batch.append(name)

    return new_batch


if __name__ == '__main__':
    batch = create_initial_batch(INITIAL_BATCH_SIZE)

    for gen in range(GENERATIONS):
        print('Starting round for generation: ', gen)
        survivors = play_round(batch)

        if str(gen) not in [s.split('-')[0] for s in survivors]:
            print('No survivors from current generation', gen)
            break

        cleanup_temp_folder(survivors)
        batch = create_new_batch(survivors, gen)
        print('Generation survivors:', survivors)
        print()

