import sys

import numpy as np
import pygame


# text("글자",글자크기,컬러1,컬러2,컬러3)
# 예시 : screen.blit(text("hi",50,255,255,255),self_pos)
def text(text_value, text_size, c1, c2, c3):
    font = pygame.font.SysFont('malgungothic', text_size)
    text = font.render(text_value, True, (c1, c2, c3))
    return text


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board_array = np.zeros((19, 19))

# 홀수, 홀수 돌을 둘 수 있는 곳이고 나머지는 벽을 둘 수 있는 곳
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


# 객체 생성 예시 a = Object("d", [1, 2], (1, 2)) 2번째는 대괄호, 3번째는 소괄호여야 함.
# 대괄호로 만든건 값을 변경할 수 있지만 소괄호로 만든건 값을 변경할 수 없음
# 좌표는 계속 변하지만 크기는 변하지 않으므로 이렇게 설정함
class Object:
    def __init__(self, src: str, pos: list[int], size: tuple[int, int]):
        self.img = pygame.image.load(src).convert_alpha()
        self.pos = pos
        self.size = size


board = Object("판.png", [200, 0], (500, 500))
horizon_wall1 = Object("가로벽.png", [44, 110], (111, 3))
vertical_wall1 = Object("세로벽.png", [99, 257], (3, 111))
horizon_wall2 = Object("가로벽.png", [744, 310], (111, 3))
vertical_wall2 = Object("세로벽.png", [799, 57], (3, 111))
black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))


def display_base_objects():
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (150, 150, 150),
                        [(30, 63), (50, 43), (150, 43), (170, 63), (170, 163), (150, 183), (50, 183), (30, 163)])
    pygame.draw.polygon(screen, (150, 150, 150), [(50, 243), (170, 243), (170, 383), (30, 383), (30, 263)])
    pygame.draw.polygon(screen, (150, 150, 150), [(750, 43), (870, 43), (870, 183), (730, 183), (730, 63)])
    pygame.draw.polygon(screen, (150, 150, 150), [(750, 243), (870, 243), (870, 383), (730, 383), (730, 263)])
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
                        screen.blit(temp_horizon.img, [200 + 27.8 * x, 28 * y])
    screen.blits(
        (
            (black_user.img, black_user.pos),
            (white_user.img, white_user.pos)
        )
    )


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


def wall_click_event(user, wall):
    if user == "black":
        if wall == "vertical":
            if vertical_wall1.pos[0] <= pygame.mouse.get_pos()[0] <= vertical_wall1.pos[0] + 140 and \
                    vertical_wall1.pos[1] <= pygame.mouse.get_pos()[1] <= vertical_wall1.pos[1] + 140:
                return True
        elif wall == "horizon":
            if horizon_wall1.pos[0] <= pygame.mouse.get_pos()[0] <= horizon_wall1.pos[0] + 140 and \
                    horizon_wall1.pos[1] <= pygame.mouse.get_pos()[1] <= horizon_wall1.pos[1] + 140:
                return True
    elif user == "white":
        if wall == "vertical":
            if vertical_wall2.pos[0] <= pygame.mouse.get_pos()[0] <= vertical_wall2.pos[0] + 140 and \
                    vertical_wall2.pos[1] <= pygame.mouse.get_pos()[1] <= vertical_wall2.pos[1] + 140:
                return True
        if wall == "horizon":
            if horizon_wall2.pos[0] <= pygame.mouse.get_pos()[0] <= horizon_wall2.pos[0] + 140 and \
                    horizon_wall2.pos[1] <= pygame.mouse.get_pos()[1] <= horizon_wall2.pos[1] + 140:
                return True
    return False


click_location = [0, 0]


def click_cell(position):  # ex) click_cell(pygame.mouse.get_pos()) \n print(click_location)
    if 0 <= (position[0] - 200) % 56 <= 53:
        click_location[0] = ((position[0] - 200) // 56) * 2 + 1
    else:
        click_location[0] = ((position[0] - 200) // 56) * 2 + 2

    if 0 <= (position[1]) % 56 <= 53:
        click_location[1] = ((position[1]) // 56) * 2 + 1
    else:
        click_location[1] = ((position[1]) // 56) * 2 + 2
    print(click_location)


# turn 매개변수의 타입은 Str, 값은 black, white 가질 수 있음
def game(turn):
    display_base_objects()
    board_loading()
    pygame.display.update()
    while True:
        clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_cell(pygame.mouse.get_pos())
                if user_click_event(turn):
                    if turn == "black":
                        game_black(turn)
                    elif turn == "white":
                        game_white(turn)
                elif wall_click_event(turn, "vertical"):
                    game_vertical(turn)
                elif wall_click_event(turn, "horizon"):
                    game_horizon(turn)


# turn 매개변수의 타입은 Str, 값은 black, white 가질 수 있음
def game_vertical(turn):
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_wall = Object("세로벽.png", [99, 247], (3, 111))
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
                        game_black()
                    elif turn == "white":
                        game_white()
                elif wall_click_event(turn, "horizon"):
                    game_horizon(turn)
                # 벽을 설치하는 로직
                elif True:  # board_check(pygame.mouse.get_pos())
                    make_wall(pygame.mouse.get_pos(), "vertical")
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


def make_wall(pos, type):
    for j in range(8):
        if 246 + j * 55 <= pos[0] <= 266 + j * 55:
            for i in range(8):
                if 45 + i * 55 <= pos[1] <= 65 + i * 55:
                    if type == "vertical":
                        board_array[(2 + 2 * i) - 1, (2 + 2 * j)] = 4
                        board_array[2 + 2 * i, 2 + 2 * j] = 4
                        board_array[(2 + 2 * i) + 1, (2 + 2 * j)] = 4
                    elif type == "horizon":
                        board_array[(2 + 2 * i), (2 + 2 * j) - 1] = 4
                        board_array[2 + 2 * i, 2 + 2 * j] = 4
                        board_array[(2 + 2 * i), (2 + 2 * j) + 1] = 4


game("black")
