import numpy as np

# Hyper parameters
HIDDEN_LAYER_SIZE = 10
OUTPUT_SIZE = 2
INPUT_SIZE = 8


class RecurrentNeuralNet:
    def __init__(self, weights_hidden_output=None, weights_input_hidden=None, weights_hidden_hidden=None):
        self.W_hy = np.array(weights_hidden_output) \
            if weights_hidden_output is not None \
            else np.random.uniform(low=-1, high=1, size=(OUTPUT_SIZE, HIDDEN_LAYER_SIZE))

        self.W_xh = np.array(weights_input_hidden) \
            if weights_input_hidden is not None \
            else np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, INPUT_SIZE))

        self.W_hh = np.array(weights_hidden_hidden) \
            if weights_hidden_hidden is not None \
            else np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE))

        self.h = np.zeros(len(self.W_hh))

    def reset(self):
        self.h = np.zeros(len(self.W_hh))

    def get_state(self):
        return {
            'weights_hidden_output': self.W_hy.tolist(),
            'weights_input_hidden': self.W_xh.tolist(),
            'weights_hidden_hidden': self.W_hh.tolist(),
            'hidden_layer': self.h
        }

    def step(self, x):
        dot_hh = np.dot(self.W_hh, self.h)
        dot_xh = np.dot(self.W_xh, x)
        self.h = np.tanh(dot_hh + dot_xh)
        y = np.dot(self.W_hy, self.h)
        return y


if __name__ == '__main__':
    brain = RecurrentNeuralNet()
    print(brain.get_state())

    for _ in range(10):
        print(brain.step([0.2, 0.3, 0.6]))

