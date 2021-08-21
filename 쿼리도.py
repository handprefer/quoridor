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
