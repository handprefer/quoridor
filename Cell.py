def user(turn) -> tuple[int, int]:
    import main
    if turn == "black":
        position = main.black_user.pos
    else:
        position = main.white_user.pos
    wall_size = 0

    first_x = position[0] - 198 - 56 * ((position[0] - 198) // 56)  # 0~55
    i = 0
    if first_x // 28 > 0:
        mid_x = (first_x - 56) * (-1)
    else:
        mid_x = first_x
    if mid_x <= wall_size:
        if first_x // 28 > 0:
            i = (((position[0] - 198) // 56) + 1) * 2
        else:
            i = ((position[0] - 198) // 56) * 2
    else:
        i = ((position[0] - 198) // 56) * 2 + 1
    if (position[0] - 198) % 56 == 0:
        i = ((position[0] - 198) // 56) * 2

    first_y = position[1] + 2 - 56 * ((position[1] + 2) // 56)  # 0~55
    j = 0
    if first_y // 28 > 0:
        mid_y = (first_y - 56) * (-1)
    else:
        mid_y = first_y
    if mid_y <= wall_size:
        if first_y // 28 > 0:
            j = (((position[1] + 2) // 56) + 1) * 2
        else:
            j = ((position[1] + 2) // 56) * 2
    else:
        j = ((position[1] + 2) // 56) * 2 + 1
    if (position[1] + 2) % 56 == 0:
        j = ((position[1] + 2) // 56) * 2
    return int(j), int(i)


def click(position) -> tuple[int, int]:
    wall_size = 3

    first_x = position[0] - 198 - 56 * ((position[0] - 198) // 56)
    i = 0
    if first_x // 28 > 0:
        mid_x = (first_x - 56) * (-1)
    else:
        mid_x = first_x
    if mid_x <= wall_size:
        if first_x // 28 > 0:
            i = (((position[0] - 198) // 56) + 1) * 2
        else:
            i = ((position[0] - 198) // 56) * 2
    else:
        i = ((position[0] - 198) // 56) * 2 + 1
    if (position[0] - 198) % 56 == 0:
        i = ((position[0] - 198) // 56) * 2
    first_y = position[1] + 2 - 56 * ((position[1] + 2) // 56)  # 0~55
    j = 0
    if first_y // 28 > 0:
        mid_y = (first_y - 56) * (-1)
    else:
        mid_y = first_y
    if mid_y <= wall_size:
        if first_y // 28 > 0:
            j = (((position[1] + 2) // 56) + 1) * 2
        else:
            j = ((position[1] + 2) // 56) * 2
    else:
        j = ((position[1] + 2) // 56) * 2 + 1
    if (position[1] + 2) % 56 == 0:
        j = ((position[1] + 2) // 56) * 2
    return int(j), int(i)
