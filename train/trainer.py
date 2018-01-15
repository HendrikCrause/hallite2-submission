import uuid
import json
import os
import random
from rnn.rnn import DeepRecurrentNeuralNet
from train.game_runner import run_halite_game, determine_ranks

INITIAL_BATCH_SIZE = 64
ROUNDS_PER_BATCH_2 = 4
ROUNDS_PER_BATCH_4 = 3
SURVIVORS_PER_ROUND = 8


def create_initial_batch(size=INITIAL_BATCH_SIZE):
    out = []
    for _ in range(size):
        name = str(uuid.uuid4())
        out.append(name)
        net = DeepRecurrentNeuralNet()
        with open('temp/' + name + '.bot', 'w') as write_file:
            write_file.write(json.dumps(net.get_structure()))

    return out


def split_into_chunks(batch, chunk_size):
    return [batch[x:x+chunk_size] for x in range(0, len(batch), chunk_size)]


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
    return [x for x in sorted_results[:SURVIVORS_PER_ROUND]]


def cleanup_temp_folder():
    folder = 'temp/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bots = create_initial_batch(INITIAL_BATCH_SIZE)
    survivors = play_round(bots)
    print(survivors)
