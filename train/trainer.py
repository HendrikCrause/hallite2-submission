from rnn.rnn import DeepRecurrentNeuralNet
import uuid
import json
from train.game_runner import run_halite_game

INITIAL_BATCH_SIZE = 64


def create_initial_batch(size=INITIAL_BATCH_SIZE):
    out = []
    for _ in range(size):
        name = str(uuid.uuid4())
        out.append(name)
        net = DeepRecurrentNeuralNet()
        with open('temp/' + name + '.bot', 'w') as write_file:
            write_file.write(json.dumps(net.get_structure()))

    return out


if __name__ == '__main__':
    bots = create_initial_batch(2)
    run_halite_game(bots)
