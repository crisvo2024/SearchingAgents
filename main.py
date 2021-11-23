import numpy as np
import random

pieces = [
    [8, 3],
    [5, 1],
    [2, 2],
    [1, 1],
    [9, 4],
    [6, 2],
    [4, 3],
    [5, 7],
    [3, 2],
    [4, 2]
]


def generate():
    board = np.zeros((10, 10))
    options = pieces.copy()
    while options:
        selected = random.choice(options)
        options.remove(selected)
        piece = pieces.index(selected)
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


def main():
    generated = generate()
    print(generated)
    print(generated[generated == 0].size)


if __name__ == '__main__':
    main()
