import main


def user(turn):
    for i in range(19):
        for j in range(19):
            if main.board_array[i, j] == 1 and turn == "black":
                x = i
                y = j
            elif main.board_array[i, j] == 2 and turn == "white":
                x = i
                y = j
    return 202 + (y - 1) * 27.9, (x - 1) * 28
