import numpy as np
import pprint
import random
from operator import itemgetter
from numpy.random import default_rng

pp = pprint.PrettyPrinter(indent=4)
rng = default_rng()

pieces = [
    [8, 3],
    [5, 1],
    [2, 2],
    [1, 1],
    [9, 4],
    [6, 2],
    [4, 3],
    [7, 5],
    [3, 2],
    [4, 2]
]


def generate():
    board = np.zeros((10, 10))
    options = pieces.copy()
    return fill(board, options)


def fill(board: np.array, options: list):
    while options:
        selected = random.choice(options)
        options.remove(selected)
        piece = pieces.index(selected) + 1
        if random.randrange(2) == 1:
            selected = [selected[1], selected[0]]
        zeros = list(np.where(board == 0))
        while zeros[0].size:
            empty = True
            if zeros[0][0] + selected[0] < 10 and zeros[1][0] + selected[1] < 10:
                if (board[zeros[0][0]:zeros[0][0] + selected[0], zeros[1][0]:zeros[1][0] + selected[1]] == 0).all():
                    board[zeros[0][0]:zeros[0][0] + selected[0], zeros[1][0]:zeros[1][0] + selected[1]] = piece
                else:
                    empty = False
            else:
                empty = False
            if not empty:
                zeros[0] = zeros[0][1:]
                zeros[1] = zeros[1][1:]
            else:
                break
    return board


def evolutive_fill(board: np.array, options: list):
    used = []
    while options:
        selected = random.choice(options)
        options.remove(selected)
        piece = pieces.index(selected) + 1
        if random.randrange(2) == 1:
            selected = [selected[1], selected[0]]
        zeros = list(np.where(board == 0))
        while zeros[0].size:
            empty = True
            if zeros[0][0] + selected[0] < 10 and zeros[1][0] + selected[1] < 10:
                if (board[zeros[0][0]:zeros[0][0] + selected[0], zeros[1][0]:zeros[1][0] + selected[1]] == 0).all():
                    board[zeros[0][0]:zeros[0][0] + selected[0], zeros[1][0]:zeros[1][0] + selected[1]] = piece
                    used.append(selected)
                else:
                    empty = False
            else:
                empty = False
            if not empty:
                zeros[0] = zeros[0][1:]
                zeros[1] = zeros[1][1:]
            else:
                break
    return board, used


def successor(state: np.array):
    board = state.copy()
    used = np.unique(board)[1:]
    # print(used)
    board[board == random.choice(used)] = 0
    # print(board)
    used = np.unique(board)[1:]
    # print(used)
    options = np.array(pieces)[~np.isin(np.arange(1, 11), used)]
    # print(options)
    board = fill(board, options.tolist())
    # print(board)
    return board


def heuristic(state):
    return state[state == 0].size


def hill_climbing():
    current = generate()
    print(current)
    value = heuristic(current)
    for _ in range(1000):
        neighbor = successor(current)
        neighbor_value = heuristic(neighbor)
        if neighbor_value == 0:
            return neighbor, neighbor_value
        if neighbor_value < value :
            current = neighbor
            value = neighbor_value
    return current, value

# def simulated_annealing():
#     initial_temp = 10000
#     alpha = -1
#     current = generate()
#     print(current)
#     value = heuristic(current)
#     best = current
#     best_value = value
#     for T in range(initial_temp, 1, alpha):
#         neighbor = successor(current)
#         neighbor_value = heuristic(neighbor)
#
#         if neighbor_value == 0:
#             return neighbor, neighbor_value
#
#         if neighbor_value < value or random.uniform(0, 1) < np.exp(value-neighbor_value / T):
#             if neighbor_value < value and neighbor_value < best_value:
#                 best = neighbor
#                 best_value = neighbor_value
#             current = neighbor
#             value = neighbor_value
#     return best, best_value


def simulated_annealing():
    initial_temp = 100000
    alpha = -1
    current = generate()
    print(current)
    value = heuristic(current)
    for T10 in range(initial_temp, 1, alpha):
        T = T10/1000
        neighbor = successor(current)
        neighbor_value = heuristic(neighbor)

        if neighbor_value == 0:
            return neighbor, neighbor_value

        if neighbor_value < value or random.uniform(0, 1) < np.exp(value-neighbor_value / T):
            current = neighbor
            value = neighbor_value
    return current, value


def generate_boards(n: int):
    original = np.zeros((10, 4))
    N = 10
    p = 0.6
    #llenar tableros con los diferentes conjuntos de fichas
    population = []
    board = np.zeros((10, 10))

    for _ in range(n):
        valid = False
        while not valid:
            meta = original.copy()
            is_in = rng.choice(a=[False, True], size=N, p=[p, 1-p])
            for _ in range(10):
                board = np.zeros((10, 10))
                pieces_to_use = np.array(pieces)[is_in]
                board, used_pieces = evolutive_fill(board, pieces_to_use.tolist())
                used = np.unique(board).astype(np.intc)[1:]
                if np.array_equal(used, np.arange(1, 11)[is_in]):
                    valid = True
                    break
        #metadatos para las fichas: [pieza usada?, horizontal?, pos x, pos y]
        for i in used:
            meta[i-1][0] = 1
            if pieces[i-1] in used_pieces:
                meta[i-1][1] = 0
            else:
                meta[i-1][1] = 1
            meta[i-1][2], meta[i-1][3] = np.array(np.where(board == i))[:, 0]
        population.append(meta)
    return population


def fit(state: np.array):
    is_in = state[:, 0].astype(bool)
    used_pieces = np.array(pieces)[is_in]
    area = np.sum(used_pieces[:, 0]*used_pieces[:, 1])
    return 100-area


def merge(a, b):

    firstHalfA = a[:5, :]
    secondHalfB = b[5:, :]
    son1 = np.concatenate((firstHalfA, secondHalfB), axis=0)
    return




def evolutive():
    population = generate_boards(100)
#    for j in range(5):
      #  print(j)
    fits = [[i, fit(population[i])] for i in range(100)]
    fits = sorted(fits, key=itemgetter(1))
    print(fits)
    new = []
    for i in range(len(population)):
        new.append(population[fits[i][0]])

    population = new[0:100]

    for i in range(20):
        population[-i] = population[i]
    print(population)
    top50 = population[:50]
    bottom50 = population[50:]

    newPopulation=[]

    for i in range(25):
        newPopulation.append(merge(top50[-i], top50[i]))
        newPopulation.append(merge(bottom50[-i], bottom50[i]))
    newPopulation.append(top50[:20])
    population = newPopulation

    #fits = [[i, fit(population[i])] for i in range(100)]
    #fits = sorted(fits, key=itemgetter(1))




def main():
    generated = generate()
    print(generated)
    # heuristic function
    print(heuristic(generated))
    generated = successor(generated)
    print(generated)
    print(heuristic(generated))


if __name__ == '__main__':
    # main()
    # print(hill_climbing())
    # print(simulated_annealing())
    evolutive()
