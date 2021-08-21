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
        self.img = src
        self.pos = pos
        self.size = size
