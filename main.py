from numpy import zeros
import pygame
import Scene


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


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board_array = zeros((19, 19))
board_init()

board = Object("판.png", [200, 0], (500, 500))
horizon_wall1 = Object("가로벽big.png", [44, 100], (108, 4))
vertical_wall1 = Object("세로벽big.png", [97, 190], (4, 108))
horizon_wall2 = Object("가로벽big.png", [744, 100], (108, 4))
vertical_wall2 = Object("세로벽big.png", [797, 190], (4, 108))
black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))

if __name__ == '__main__':
    Scene.start()
