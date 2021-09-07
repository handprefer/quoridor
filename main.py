import pygame
from numpy import zeros

import Scene


def board_init(board):
    temp = board[:]
    for i in range(19):
        for j in range(19):
            if i % 2 == 1 and j % 2 == 1:
                temp[i, j] = 0
            else:
                temp[i, j] = 3
    for i in range(19):
        for j in range(19):
            if j == 0 or j == 18 or i == 0 or i == 18:
                temp[i, j] = 4
    temp[9, 1] = 1
    temp[9, 17] = 2
    return temp


def game_reset(board):
    temp = board_init(board)
    black_user.pos = [203, 224]
    white_user.pos = [647, 224]
    return temp


def text(text_value, text_size, c1, c2, c3):
    font = pygame.font.SysFont('malgungothic', text_size)
    letter = font.render(text_value, True, (c1, c2, c3))
    return letter


class Object:
    def __init__(self, src: str, pos: list[int], size: tuple[int, int]):
        self.img = pygame.image.load(src)
        self.pos = pos
        self.size = size


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board_array = zeros((19, 19))
board_array = board_init(board_array)

black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))

if __name__ == '__main__':
    Scene.start()
