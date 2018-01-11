import numpy as np

# Hyper parameters
HIDDEN_LAYER_SIZE = 64
OUTPUT_SIZE = 2
INPUT_SIZE = 8
NUMBER_OF_LAYERS = 3


class DeepRecurrentNeuralNet:
    def __init__(self, structure_dict=None):
        if structure_dict is None:
            structure_dict = {
                'input_layer': {
                    'weights_hidden_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                    'weights_input_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, INPUT_SIZE)),
                    'weights_hidden_output': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE))
                }, 'hidden_layer': {
                    'weights_hidden_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                    'weights_input_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                    'weights_hidden_output': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE))
                }, 'output_layer': {
                    'weights_hidden_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                    'weights_input_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                    'weights_hidden_output': np.random.uniform(low=-1, high=1, size=(OUTPUT_SIZE, HIDDEN_LAYER_SIZE))
                },
            }

        self.input_layer = RecurrentNeuralNetLayer(structure_dict['input_layer'])
        self.hidden_layer = RecurrentNeuralNetLayer(structure_dict['hidden_layer'])
        self.output_layer = RecurrentNeuralNetLayer(structure_dict['output_layer'])

    def step(self, x):
        output = self.input_layer.step(x)
        output = self.hidden_layer.step(output)
        return self.output_layer.step(output)

    def reset(self):
        self.input_layer.reset()
        self.hidden_layer.reset()
        self.output_layer.reset()

    def get_structure(self):
        return {
            'input_layer': self.input_layer.get_structure(),
            'hidden_layer': self.hidden_layer.get_structure(),
            'output_layer': self.output_layer.get_structure()
        }


class RecurrentNeuralNetLayer:
    def __init__(self, structure_dict=None):
        if structure_dict is None:
            structure_dict = {
                'weights_hidden_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, HIDDEN_LAYER_SIZE)),
                'weights_input_hidden': np.random.uniform(low=-1, high=1, size=(HIDDEN_LAYER_SIZE, INPUT_SIZE)),
                'weights_hidden_output': np.random.uniform(low=-1, high=1, size=(OUTPUT_SIZE, HIDDEN_LAYER_SIZE))
            }

        self.W_hy = np.array(structure_dict['weights_hidden_output'])
        self.W_xh = np.array(structure_dict['weights_input_hidden'])
        self.W_hh = np.array(structure_dict['weights_hidden_hidden'])

        self.h = np.zeros(len(self.W_hh))

    def reset(self):
        self.h = np.zeros(len(self.W_hh))

    def get_structure(self):
        return {
            'weights_hidden_output': self.W_hy.tolist(),
            'weights_input_hidden': self.W_xh.tolist(),
            'weights_hidden_hidden': self.W_hh.tolist()
        }

    def step(self, x):
        dot_hh = np.dot(self.W_hh, self.h)
        dot_xh = np.dot(self.W_xh, x)
        self.h = np.tanh(dot_hh + dot_xh)
        y = np.dot(self.W_hy, self.h)
        return self._sigmoid(y)

    @staticmethod
    def _sigmoid(y):
        return 1 / (1 + np.exp(-y))


if __name__ == '__main__':
    brain = RecurrentNeuralNetLayer()

    for key, value in brain.get_structure().items():
        print(key, value)

    for _ in range(10):
        uniform = np.random.uniform(low=-1, high=1, size=INPUT_SIZE)
        print('input', uniform)
        print('output', brain.step(uniform))

