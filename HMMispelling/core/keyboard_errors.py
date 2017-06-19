from abc import ABCMeta

import math
import numpy as np
import sys

simple_qwerty = {
    'A': [[None, 'Q', 'W'],
          [None, 'A', 'S'],
          [None, None, 'Z']
          ],
    'B': [[None, 'G', 'H'],
          ['V', 'B', 'N'],
          [None, None, None]
          ],
    'C': [[None, 'D', 'F'],
          ['X', 'C', 'V'],
          [None, None, None]
          ],
    'D': [[None, 'E', 'R'],
          ['S', 'D', 'F'],
          ['X', 'C', None]
          ],
    'E': [[None, None, None],
          ['W', 'E', 'R'],
          ['S', 'D', None]
          ],
    'F': [[None, 'R', 'T'],
          ['D', 'F', 'G'],
          ['C', 'V', None]
          ],
    'G': [[None, 'T', 'Y'],
          ['F', 'G', 'H'],
          ['V', 'B', None]
          ],
    'H': [[None, 'Y', 'U'],
          ['G', 'H', 'J'],
          ['B', 'N', None]
          ],
    'I': [[None, None, None],
          ['U', 'I', 'O'],
          ['J', 'K', None]
          ],
    'J': [[None, 'U', 'I'],
          ['H', 'J', 'K'],
          ['N', 'M', None]
          ],
    'K': [[None, 'I', 'O'],
          ['J', 'K', 'L'],
          ['M', None, None]
          ],
    'L': [[None, 'O', 'P'],
          ['K', 'L', None],
          [None, None, None]
          ],
    'M': [[None, 'J', 'K'],
          ['N', 'M', None],
          [None, None, None]
          ],
    'N': [[None, 'H', 'J'],
          ['B', 'N', 'M'],
          [None, None, None]
          ],
    'O': [[None, None, None],
          ['I', 'O', 'P'],
          ['K', 'L', None]
          ],
    'P': [[None, None, None],
          ['O', 'P', None],
          ['L', None, None]
          ],
    'Q': [[None, None, None],
          [None, 'Q', 'W'],
          [None, 'A', None]
          ],
    'R': [[None, None, None],
          ['E', 'R', 'T'],
          ['D', 'F', None]
          ],
    'S': [['Q', 'W', 'E'],
          ['A', 'S', 'D'],
          ['Z', 'X', None]
          ],
    'T': [[None, None, None],
          ['R', 'T', 'Y'],
          ['F', 'G', None]
          ],
    'U': [[None, None, None],
          ['Y', 'U', 'I'],
          ['H', 'J', None]
          ],
    'V': [[None, 'F', 'G'],
          ['C', 'V', 'B'],
          [None, None, None]
          ],
    'W': [[None, None, None],
          ['Q', 'W', 'E'],
          ['A', 'S', None]
          ],
    'X': [[None, 'S', 'D'],
          ['Z', 'X', 'C'],
          [None, None, None]
          ],
    'Y': [[None, None, None],
          ['T', 'Y', 'U'],
          ['G', 'H', None]
          ],
    'Z': [[None, 'A', 'S'],
          [None, 'Z', 'X'],
          [None, None, None]
          ],
    'a': [[None, 'q', 'w'],
          [None, 'a', 's'],
          [None, None, 'z']
          ],
    'b': [[None, 'g', 'h'],
          ['v', 'b', 'n'],
          [None, None, None]
          ],
    'c': [[None, 'd', 'f'],
          ['x', 'c', 'v'],
          [None, None, None]
          ],
    'd': [[None, 'e', 'r'],
          ['s', 'd', 'f'],
          ['x', 'c', None]
          ],
    'e': [[None, None, None],
          ['w', 'e', 'r'],
          ['s', 'd', None]
          ],
    'f': [[None, 'r', 't'],
          ['d', 'f', 'g'],
          ['c', 'v', None]
          ],
    'g': [[None, 't', 'y'],
          ['f', 'g', 'h'],
          ['v', 'b', None]
          ],
    'h': [[None, 'y', 'u'],
          ['g', 'h', 'j'],
          ['b', 'n', None]
          ],
    'i': [[None, None, None],
          ['u', 'i', 'o'],
          ['j', 'k', None]
          ],
    'j': [[None, 'u', 'i'],
          ['h', 'j', 'k'],
          ['n', 'm', None]
          ],
    'k': [[None, 'i', 'o'],
          ['j', 'k', 'l'],
          ['m', None, None]
          ],
    'l': [[None, 'o', 'p'],
          ['k', 'l', None],
          [None, None, None]
          ],
    'm': [[None, 'j', 'k'],
          ['n', 'm', None],
          [None, None, None]
          ],
    'n': [[None, 'h', 'j'],
          ['b', 'n', 'm'],
          [None, None, None]
          ],
    'o': [[None, None, None],
          ['i', 'o', 'p'],
          ['k', 'l', None]
          ],
    'p': [[None, None, None],
          ['o', 'p', None],
          ['l', None, None]
          ],
    'q': [[None, None, None],
          [None, 'q', 'w'],
          [None, 'a', None]
          ],
    'r': [[None, None, None],
          ['e', 'r', 't'],
          ['d', 'f', None]
          ],
    's': [['q', 'w', 'e'],
          ['a', 's', 'd'],
          ['z', 'x', None]
          ],
    't': [[None, None, None],
          ['r', 't', 'y'],
          ['f', 'g', None]
          ],
    'u': [[None, None, None],
          ['y', 'u', 'i'],
          ['h', 'j', None]
          ],
    'v': [[None, 'f', 'g'],
          ['c', 'v', 'b'],
          [None, None, None]
          ],
    'w': [[None, None, None],
          ['q', 'w', 'e'],
          ['a', 's', None]
          ],
    'x': [[None, 's', 'd'],
          ['z', 'x', 'c'],
          [None, None, None]
          ],
    'y': [[None, None, None],
          ['t', 'y', 'u'],
          ['g', 'h', None]
          ],
    'z': [[None, 'a', 's'],
          [None, 'z', 'x'],
          [None, None, None]
          ]
}


class KeyBoardErrorModel(metaclass=ABCMeta):
    def __init__(self, layout=simple_qwerty):
        self.layout = layout

    def evaluate_error(self):
        """
        Creates the distribution of error for each key based on its neighbors
        :return: A dictionary of letters containing a list of tuples (letter, probability)
        """
        distributions = {}
        for key in self.layout:
            key_neighbors = self.layout[key]
            distributions[key] = self._distribution_(key_neighbors)

        return distributions

    def _distribution_(self, neighbors):
        """
        Implements the model specific logic of error distribution
        :param neighbors:
        :return:
        """
        pass


class KeyboardUniformError(KeyBoardErrorModel):
    def _distribution_(self, neighbors):
        """
        Implements the the uniform error distribution
        :param neighbors:
        :return:
        """
        size = len(neighbors)
        elements = sum(key is not None for keys in neighbors for key in keys)
        probability = 1 / elements

        result = []

        for i in range(0, size):
            for j in range(0, size):
                if neighbors[i][j] is not None:
                    result += [(neighbors[i][j], probability)]

        return result


class KeyboardPseudoUniformError(KeyBoardErrorModel):
    def __init__(self, layout=simple_qwerty, key_prob=0.7):
        super().__init__(layout)
        self.key_prob = key_prob

    def _distribution_(self, neighbors):
        """
        Implements the uniform distribution, but the probability the wanted key has a prior probability
        :param neighbors:
        :return:
        """
        size = len(neighbors)
        elements = sum(key is not None for keys in neighbors for key in keys)
        probability = self.pseudo_uniform(size, elements)

        result = []

        for i in range(0, size):
            for j in range(0, size):
                if neighbors[i][j] is not None:
                    result += [(neighbors[i][j], probability[i][j])]

        return result

    def pseudo_uniform(self, size, elements):
        result = [[(1 - self.key_prob) / (elements - 1)] * size for _ in range(0, size)]

        half_size = int(math.floor(size // 2))

        result[half_size][half_size] = self.key_prob

        return result


class KeyBoardGaussianError(KeyBoardErrorModel):
    def __init__(self, layout=simple_qwerty, mean=0, variance=1):
        super().__init__(layout)
        self.mean = mean
        self.variance = variance

    def _distribution_(self, neighbors):
        """
        Implements the gaussian model error
        :param neighbors:
        :return:
        """
        size = len(neighbors)

        result = []
        probability = self._2d_gaussian_distribution_(size)
        for i in range(0, size):
            for j in range(0, size):
                if neighbors[i][j] is not None:
                    result += [(neighbors[i][j], probability[i][j])]

        total = sum(prob for neighbor, prob in result)
        normalized_result = [(neighbor, prob / total) for neighbor, prob in result]
        return normalized_result

    def _single_dist_(self, x):
        result = (1 / (math.sqrt(2 * math.pi * self.variance))) * (
            math.e ** ((-(x - self.mean) ** 2) / (2 * self.variance ** 2)))

        return result

    def _2d_gaussian_distribution_(self, size):
        half_size = int(math.floor(size // 2))

        x = 0
        gaussian = [[0] * size for _ in range(0, size)]
        for i in range(-half_size, half_size + 1):
            y = 0
            for j in range(-half_size, half_size + 1):
                x_dist = self._single_dist_(i)
                y_dist = self._single_dist_(j)
                gaussian[x][y] = x_dist * y_dist
                y += 1
            x += 1

        return gaussian


epsilon = sys.float_info.epsilon


def map_to_zero(key):
    key_val = ord(key)
    if 65 <= key_val <= 90:
        return key_val - 65

    if 97 <= key_val <= 122:
        return key_val - 97 + (65 - 90)


def create_emission_matrix(errors_distributions):
    size = len(errors_distributions)

    emission_matrix = np.full((size, size), epsilon, dtype=float)
    key_list = []
    for key in errors_distributions:
        key_list += [key]
        for letter, probability in errors_distributions[key]:
            i = map_to_zero(key)
            j = map_to_zero(letter)
            emission_matrix[i, j] = probability

    for i in range(0, size):
        emission_matrix[i] = emission_matrix[i] / sum(emission_matrix[i])

    result = np.matrix(emission_matrix)

    observations = list(errors_distributions.keys())
    observations.sort()

    return observations, result


error_model = KeyBoardGaussianError()
x = error_model.evaluate_error()

print(x)
for key in x:
    a = sum(n for _, n in x[key])
    print("Key {} - Sum {}".format(key, a))

em = create_emission_matrix(x)
print(type(em))
# print(em.sum(axis=1))
