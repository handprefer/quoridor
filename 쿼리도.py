import sys

import numpy as np
import pygame

pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board = np.zeros((19, 19))

# 홀수, 홀수 돌을 둘 수 있는 곳이고 나머지는 벽을 둘 수 있는 곳
for i in range(19):
    for j in range(19):
        if i % 2 == 1 and j % 2 == 1:
            board[i, j] = 0
        else:
            board[i, j] = 2

for i in range(19):
    for j in range(19):
        if j == 0 or j == 18 or i == 0 or i == 18:
            board[i, j] = 3


# 객체 생성 예시 a = Object("d", [1, 2], (1, 2)) 2번째는 대괄호, 3번째는 소괄호여야 함.
# 대괄호로 만든건 값을 변경할 수 있지만 소괄호로 만든건 값을 변경할 수 없음
# 좌표는 계속 변하지만 크기는 변하지 않으므로 이렇게 설정함
class Object:
    def __init__(self, src: str, pos: list[int], size: tuple[int, int]):
        self.img = pygame.image.load(src)
        self.pos = pos
        self.size = size


board = Object("판.png", [200, 0], (500, 500))
horizon_wall1 = Object("가로벽.png", [44, 100], (111, 3))
vertical_wall1 = Object("세로벽.png", [99, 247], (3, 111))
horizon_wall2 = Object("가로벽.png", [744, 300], (111, 3))
vertical_wall2 = Object("세로벽.png", [799, 47], (3, 111))
black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))


def display_base_objects():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), [30, 43, 140, 140])
    pygame.draw.rect(screen, (0, 0, 0), [30, 243, 140, 140])
    pygame.draw.rect(screen, (0, 0, 0), [730, 43, 140, 140])
    pygame.draw.rect(screen, (0, 0, 0), [730, 243, 140, 140])
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
    if user == "white:":
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
    if user == "white":
        if wall == "vertical":
            if vertical_wall2.pos[0] <= pygame.mouse.get_pos()[0] <= vertical_wall2.pos[0] + 140 and \
                    vertical_wall2[1] <= pygame.mouse.get_pos()[1] <= vertical_wall2.pos[1] + 140:
                return True
        if wall == "horizon":
            if horizon_wall2[0] <= pygame.mouse.get_pos()[0] <= horizon_wall2.pos[0] + 140 and \
                    horizon_wall2[1] <= pygame.mouse.get_pos()[1] <= horizon_wall2.pos[1] + 140:
                return True
    return False


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
                if user_click_event(turn):
                    if turn == "black":
                        game_black()
                    elif turn == "white":
                        game_white()
                elif wall_click_event(turn, "vertical"):
                    game_vertical()
                elif wall_click_event(turn, "horizon"):
                    game_horizon()
