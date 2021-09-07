def black():
    import main
    x, y = 0, 0

    for i in range(19):
        for j in range(19):
            if main.board_array[i, j] == 1:
                x, y = i, j

    return 202 + (y - 1) * 27.9, (x - 1) * 28


def white():
    import main
    x, y = 0, 0

    for i in range(19):
        for j in range(19):
            if main.board_array[i, j] == 2:
                x, y = i, j

    return 202 + (y - 1) * 27.9, (x - 1) * 28
