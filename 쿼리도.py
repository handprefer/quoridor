import copy
import sys

import numpy as np
import pygame


# 기본 함수들#####################################################################


def board_init():
    for i in range(19):
        for j in range(19):
            if i % 2 == 1 and j % 2 == 1:
                board_array[i, j] = 0
            else:
                board_array[i, j] = 3
    for i in range(19):
        for j in range(19):
            if j == 0 or j == 18 or i == 0 or i == 18:
                board_array[i, j] = 4
    board_array[9, 1] = 1
    board_array[9, 17] = 2


def text(text_value, text_size, c1, c2, c3):
    font = pygame.font.SysFont('malgungothic', text_size)
    letter = font.render(text_value, True, (c1, c2, c3))
    return letter


class Object:
    def __init__(self, src: str, pos: list[int], size: tuple[int, int]):
        self.img = pygame.image.load(src)
        self.pos = pos
        self.size = size


# 이미지 갱신 관련 함수 #####################################################################


def display_base_objects():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), [33, 40, 130, 130])
    pygame.draw.rect(screen, (0, 0, 0), [33, 180, 130, 130])
    pygame.draw.rect(screen, (0, 0, 0), [733, 40, 130, 130])
    pygame.draw.rect(screen, (0, 0, 0), [733, 180, 130, 130])
    screen.blits(
        (
            (board.img, board.pos),
            (horizon_wall1.img, horizon_wall1.pos),
            (horizon_wall2.img, horizon_wall2.pos),
            (vertical_wall1.img, vertical_wall1.pos),
            (vertical_wall2.img, vertical_wall2.pos)
        )
    )


def board_loading():
    temp_vertical = Object("세로벽.png", [0, 0], (3, 111))
    temp_horizon = Object("가로벽.png", [0, 0], (111, 3))
    for y in range(19):
        for x in range(19):
            if board_array[y, x] == 4:
                if not (x % 2 == 0 and y % 2 == 0) and not (x == 0 or y == 0) and not (x == 18 or y == 18):
                    if x % 2 == 0:
                        screen.blit(temp_vertical.img, [200 + 27.8 * x, 28 * (y - 1)])
                    elif y % 2 == 0:
                        screen.blit(temp_horizon.img, [202 + 27.8 * (x - 1), 27.7 * y])
        black_user.pos = user_pos("black")
        white_user.pos = user_pos("white")
        screen.blits(
            (
                (black_user.img, black_user.pos),
                (white_user.img, white_user.pos)
            )
        )


# 마우스 클릭위치 확인 함수들#####################################################################


def user_click_event(user):
    if user == "black":
        if black_user.pos[0] < pygame.mouse.get_pos()[0] < black_user.pos[0] + 55 and \
                black_user.pos[1] < pygame.mouse.get_pos()[1] < black_user.pos[1] + 55:
            return True
    if user == "white":
        if white_user.pos[0] < pygame.mouse.get_pos()[0] < white_user.pos[0] + 55 and \
                white_user.pos[1] < pygame.mouse.get_pos()[1] < white_user.pos[1] + 55:
            return True
    return False


def wall_click_event(user, wall, pos):
    if user == "black":
        if wall == "horizon":
            if 33 <= pos[0] <= 167 and 40 <= pos[1] <= 170:
                return True
        elif wall == "vertical":
            if 33 <= pos[0] <= 167 and 180 <= pos[1] <= 310:
                return True
    elif user == "white":
        if wall == "vertical":
            if 733 <= pos[0] <= 863 and 180 <= pos[1] <= 310:
                return True
        if wall == "horizon":
            if 733 <= pos[0] <= 863 and 40 <= pos[1] <= 170:
                return True
    return False


def user_cell(turn):  # turn색깔 돌의 위치를 return
    if turn == "black":
        position = black_user.pos
    else:
        position = white_user.pos
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


def user_checker(turn):  # 클릭한곳에 돌 이동 가능여부 판단
    location = click_cell(pygame.mouse.get_pos())
    x = user_cell(turn)[0]
    y = user_cell(turn)[1]
    click_x = location[0]
    click_y = location[1]

    if click_x == x and click_y == y - 4:  # 뛰어넘기 왼쪽
        if board_array[x, y - 1] == 3 and board_array[x, y - 2] != 0 and board_array[x, y - 3] == 3:
            return True
    elif click_x == x and click_y == y + 4:  # 뛰어넘기 오른쪽
        if board_array[x, y + 1] == 3 and board_array[x, y + 2] != 0 and board_array[x, y + 3] == 3:
            return True
    elif click_x == x - 4 and click_y == y:  # 뛰어넘기 위쪽
        if board_array[x - 1, y] == 3 and board_array[x - 2, y] != 0 and board_array[x - 3, y] == 3:
            return True
    elif click_x == x + 4 and click_y == y:  # 뛰어넘기 아래쪽
        if board_array[x + 1, y] == 3 and board_array[x + 2, y] != 0 and board_array[x + 3, y] == 3:
            return True
    elif click_x == x + 2 and click_y == y - 2:  # 왼쪽 아래
        if (board_array[x + 1, y] == 3 and board_array[x + 2, y] != 0 and board_array[x + 3, y] == 4 and board_array[
            x + 2, y - 1] == 3) or \
                (board_array[x, y - 1] == 3 and board_array[x, y - 2] != 0 and board_array[x, y - 3] == 4 and
                 board_array[x + 1, y - 2] == 3):
            return True
    elif click_x == x - 2 and click_y == y - 2:  # 오른쪽 아래

        if (board_array[x - 1, y] == 3 and board_array[x - 2, y] != 0 and board_array[x - 3, y] == 4 and board_array[
            x - 2, y - 1] == 3) or \
                (board_array[x, y - 1] == 3 and board_array[x, y - 2] != 0 and board_array[x, y - 3] == 4 and
                 board_array[x - 1, y - 2] == 3):
            return True
    elif click_x == x + 2 and click_y == y + 2:  # 왼쪽 위
        if (board_array[x + 1, y] == 3 and board_array[x + 2, y] != 0 and board_array[x + 3, y] == 4 and board_array[
            x + 2, y + 1] == 3) or \
                (board_array[x, y + 1] == 3 and board_array[x, y + 2] != 0 and board_array[x, y + 3] == 4 and
                 board_array[x + 1, y + 2] == 3):
            return True
    elif click_x == x - 2 and click_y == y + 2:  # 오른쪽 위
        if (board_array[x - 1, y] == 3 and board_array[x - 2, y] != 0 and board_array[x - 3, y] == 4 and board_array[
            x - 2, y + 1] == 3) or \
                (board_array[x, y + 1] == 3 and board_array[x, y + 2] != 0 and board_array[x, y + 3] == 4 and
                 board_array[x - 1, y + 2] == 3):
            return True
    elif click_x == x and click_y == y - 2:  # 왼쪽
        if board_array[x, y - 1] == 3 and board_array[x, y - 2] == 0:
            return True
    elif click_x == x and click_y == y + 2:  # 오른쪽
        if board_array[x, y + 1] == 3 and board_array[x, y + 2] == 0:
            return True
    elif click_x == x - 2 and click_y == y:  # 위쪽
        if board_array[x - 1, y] == 3 and board_array[x - 2, y] == 0:
            return True
    elif click_x == x + 2 and click_y == y:  # 아래쪽
        if board_array[x + 1, y] == 3 and board_array[x + 2, y] == 0:
            return True
    return False


def click_cell(position):
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
    return j, i


def user_pos(type):
    global board_array
    for i in range(19):
        for j in range(19):
            if board_array[i, j] == 1 and type == "black":
                x = i
                y = j
            elif board_array[i, j] == 2 and type == "white":
                x = i
                y = j
    return 202 + (y - 1) * 27.9, (x - 1) * 28


# 게임룰에 맞는 행동인지 체크하는 함수#####################################################################

def make_graph(temp_board, pos_that_make_wall, type):
    result_board = copy.deepcopy(temp_board)
    result_board = return_board_that_add_wall(result_board, pos_that_make_wall, type)
    if result_board is None:
        return False
    graph = {}
    for x in range(19):
        for y in range(19):
            if not (x == 0 or x == 18 or y == 0 or y == 18):
                if result_board[x, y] == 0 or result_board[x, y] == 1 or result_board[x, y] == 2:
                    graph[(x, y)] = []
                    try:
                        # 아래쪽으로 갈 수 있는 경우
                        if result_board[x + 2, y] == 0 and result_board[x + 1, y] == 3:
                            graph[(x, y)].append((x + 2, y))
                        # 돌에 막힌 경우
                        elif (result_board[x + 2, y] == 1 or 2) and result_board[x + 1, y] == 3:
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x + 2, y - 2] == 0 and result_board[x + 2, y - 1] == 3:
                                graph[(x, y)].append((x + 2, y - 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x + 2, y + 2] == 0 and result_board[x + 2, y + 1] == 3:
                                graph[(x, y)].append((x + 2, y + 2))
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 4, y] == 0 and result_board[x + 3, y] == 3:
                                graph[(x, y)].append((x + 4, y))
                    except IndexError:
                        ...
                    try:
                        # 위쪽으로 갈 수 있는 경우
                        if result_board[x - 2, y] == 0 and result_board[x - 1, y] == 3:
                            graph[(x, y)].append((x - 2, y))
                        # 돌에 막힌 경우
                        elif (result_board[x - 2, y] == 1 or 2) and result_board[x - 1, y] == 3:
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x - 2, y - 2] == 0 and result_board[x - 2, y - 1] == 3:
                                graph[(x, y)].append((x - 2, y - 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x - 2, y + 2] == 0 and result_board[x - 2, y + 1] == 3:
                                graph[(x, y)].append((x - 2, y + 2))
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 4, y] == 0 and result_board[x - 3, y] == 3:
                                graph[(x, y)].append((x - 4, y))
                    except IndexError:
                        ...
                    try:
                        # 오른쪽으로 갈 수 있는 경우
                        if result_board[x, y + 2] == 0 and result_board[x, y + 1] == 3:
                            graph[(x, y)].append((x, y + 2))
                            # 돌에 막힌 경우
                        elif (result_board[x, y + 2] == 1 or 2) and result_board[x, y + 1] == 3:
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 2, y + 2] == 0 and result_board[x - 1, y + 2] == 3:
                                graph[(x, y)].append((x - 2, y + 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x, y + 4] == 0 and result_board[x, y + 3] == 3:
                                graph[(x, y)].append((x, y + 4))
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 2, y + 2] == 0 and result_board[x + 1, y + 2] == 3:
                                graph[(x, y)].append((x + 2, y + 2))
                    except IndexError:
                        ...
                    try:
                        # 왼쪽으로 갈 수 있는 경우
                        if result_board[x, y - 2] == 0 and result_board[x, y - 1] == 3:
                            graph[(x, y)].append((x, y - 2))
                        # 돌에 막힌 경우
                        elif (result_board[x, y - 2] == 1 or 2) and result_board[x, y - 1] == 3:
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 2, y - 2] == 0 and result_board[x + 1, y - 2] == 3:
                                graph[(x, y)].append((x + 2, y - 2))
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 2, y - 2] == 0 and result_board[x - 1, y - 2] == 3:
                                graph[(x, y)].append((x - 2, y - 2))
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x, y - 4] == 0 and result_board[x, y - 3] == 3:
                                graph[(x, y)].append((x, y - 4))
                    except IndexError:
                        ...
    return graph


# bfs
def wall_checker(graph, start, end):
    if not graph:
        return False
    queue = [start]  # idx 0: 노드, idx 1: 이동 거리
    visit = {start, }  # 방문한 노드 저장 공간

    while queue:
        node = queue.pop(0)
        for near_node in graph[node]:
            if near_node not in visit:
                if near_node[1] == end:
                    return True

                visit.add(near_node)
                queue.append(near_node)
    return False


# 게임을 진행할때 작동하는 함수들#####################################################################


def game(turn):
    display_base_objects()
    board_loading()
    if user_cell("black")[1] == 17:
        win("black")
        return 0
    elif user_cell("white")[1] == 1:
        win("white")
        return 0
    else:
        pygame.display.update()
        while True:
            clock.tick(3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if user_click_event(turn):
                        if turn == "black":
                            game_black(turn)
                        elif turn == "white":
                            game_white(turn)
                    elif wall_click_event(turn, "vertical", event.pos):
                        game_vertical(turn)
                    elif wall_click_event(turn, "horizon", event.pos):
                        game_horizon(turn)


def game_vertical(turn):
    global board_array
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_wall = Object("세로벽big.png", [0, 0], (4, 108))
    while True:
        clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_wall.pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 돌을 클릭한 경우
                if user_click_event(turn):
                    if turn == "black":
                        game_black(turn)
                    elif turn == "white":
                        game_white(turn)
                # 벽을 클릭한 경우
                elif wall_click_event(turn, "horizon", event.pos):
                    game_horizon(turn)
                # 벽을 설치하는 로직
                elif 200 <= event.pos[0] <= 700:
                    if wall_checker(
                            make_graph(board_array, event.pos, "vertical"),
                            user_cell("black"),
                            17
                    ) is True and \
                            wall_checker(
                                make_graph(board_array, event.pos, "vertical"),
                                user_cell("white"),
                                1
                            ) is True:
                        board_array = copy.deepcopy(
                            return_board_that_add_wall(board_array, pygame.mouse.get_pos(), "vertical"))
                        if user_cell(turn)[1] == 17:
                            print("win")
                        if turn == "black":
                            game("white")
                        elif turn == "white":
                            game("black")
        display_base_objects()
        board_loading()
        screen.blit(temp_wall.img,
                    [temp_wall.pos[0] - temp_wall.size[0] // 2, temp_wall.pos[1] - temp_wall.size[1] // 2]
                    )
        pygame.display.update()


def game_horizon(turn):
    global board_array
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_wall = Object("가로벽big.png", [0, 0], (108, 4))
    while True:
        clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_wall.pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if user_click_event(turn):
                    if turn == "black":
                        game_black(turn)
                    elif turn == "white":
                        game_white(turn)
                elif wall_click_event(turn, "vertical", event.pos):
                    game_vertical(turn)
                # 벽을 설치하는 로직
                elif 200 <= event.pos[0] <= 700:
                    if wall_checker(
                            make_graph(board_array, event.pos, "horizon"),
                            user_cell("black"),
                            17) is True and \
                            wall_checker(
                                make_graph(board_array, event.pos, "horizon"),
                                user_cell("white"),
                                1) is True:
                        board_array = return_board_that_add_wall(board_array, event.pos, "horizon")
                        if turn == "black":
                            game("white")
                        elif turn == "white":
                            game("black")
        display_base_objects()
        board_loading()
        screen.blit(temp_wall.img,
                    [temp_wall.pos[0] - temp_wall.size[0] // 2, temp_wall.pos[1] - temp_wall.size[1] // 2]
                    )
        pygame.display.update()


def game_black(turn):
    global board_array
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_user = Object("흑.png", [0, 0], (55, 55))
    while True:
        clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_user.pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if user_click_event(turn):
                    if turn == "white":
                        game_white(turn)
                elif wall_click_event(turn, "horizon", event.pos):
                    game_horizon(turn)
                elif wall_click_event(turn, "vertical", event.pos):
                    game_vertical(turn)
                # User Check
                elif user_checker(turn):
                    board_array = return_board_that_set_user_array(board_array, event.pos, "black")
                    game("white")
        display_base_objects()
        board_loading()
        screen.blit(temp_user.img,
                    [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                    )
        pygame.display.update()


def game_white(turn):
    global board_array
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_user = Object("백.png", [0, 0], (55, 55))
    while True:
        clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_user.pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if user_click_event(turn):
                    if turn == "white":
                        game_white(turn)
                elif wall_click_event(turn, "horizon", event.pos):
                    game_horizon(turn)
                elif wall_click_event(turn, "vertical", event.pos):
                    game_vertical(turn)
                # 벽을 설치하는 로직
                elif user_checker("white"):
                    board_array = return_board_that_set_user_array(board_array, event.pos, turn)
                    game("black")
        display_base_objects()
        board_loading()
        screen.blit(temp_user.img,
                    [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                    )
        pygame.display.update()


# 보드 배열관련 함수#####################################################################


def return_board_that_add_wall(temp_board, pos_that_make_wall, type):
    result_board = copy.deepcopy(temp_board)
    array = click_cell(pos_that_make_wall)
    x = array[0]
    y = array[1]
    if x % 2 == 0 and y % 2 == 0:
        if type == "vertical":
            if not (result_board[x, y] == 4 or result_board[x + 1, y] == 4 or result_board[x - 1, y] == 4):
                result_board[array[0], array[1]] = 4
                result_board[array[0] + 1, array[1]] = 4
                result_board[array[0] - 1, array[1]] = 4
                result_board[array[0] + 2, array[1]] = 4
                result_board[array[0] - 2, array[1]] = 4
        elif type == "horizon":
            if not (result_board[x, y] == 4 or result_board[x, y + 1] == 4 or result_board[x, y - 1] == 4):
                result_board[array[0], array[1]] = 4
                result_board[array[0], array[1] + 1] = 4
                result_board[array[0], array[1] - 1] = 4
                result_board[array[0], array[1] + 2] = 4
                result_board[array[0], array[1] - 2] = 4
        return result_board


def return_board_that_set_user_array(temp_board, pos_that_user_go, user):
    user_array = user_cell(user)
    result_board = copy.deepcopy(temp_board)
    array_that_user_go = click_cell(pos_that_user_go)
    result_board[user_array] = 0
    if user == "black":
        result_board[array_that_user_go] = 1
    elif user == "white":
        result_board[array_that_user_go] = 2
    return result_board


def start():
    screen.fill((255, 255, 255))
    title_text = text("QUORIDOR", 70, 0, 0, 0)

    screen.blit(title_text, (275, 140))

    pygame.display.update()
    while True:
        clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board_init()
                game("black")


def win(user):
    screen.fill((255, 255, 255))
    if user == "black":
        msg = text("Black Win", 50, 0, 0, 0)
        screen.blit(msg, (350, 200))
    elif user == "white":
        msg = text("White Win", 50, 0, 0, 0)
        screen.blit(msg, (350, 200))
    pygame.display.update()
    while True:
        clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start()


######################################################################


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board_array = np.zeros((19, 19))
board_init()

board = Object("판.png", [200, 0], (500, 500))
horizon_wall1 = Object("가로벽big.png", [44, 100], (108, 4))
vertical_wall1 = Object("세로벽big.png", [97, 190], (4, 108))
horizon_wall2 = Object("가로벽big.png", [744, 100], (108, 4))
vertical_wall2 = Object("세로벽big.png", [797, 190], (4, 108))
black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))

if __name__ == '__main__':
    start()
