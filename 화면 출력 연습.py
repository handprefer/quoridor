import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((900,500))
clock=pygame.time.Clock()

def text(text_value, text_size, c1, c2, c3):
    font = pygame.font.SysFont('malgungothic', text_size)
    letter = font.render(text_value, True, (c1, c2, c3))
    return letter

def start():
    clock.tick(3)
    screen.fill((255,255,255))
    title=text("QUORIDOR", 70, 0, 0,0)
    start=text("Start", 40, 0, 0, 0)
    screen.blit(title,(275,140))
    screen.blit(start, (412, 240))

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            pos=pygame.mouse.get_pos()
            if 413 <= pos[0] <= 497 and 254 <= pos[1] <=287:
                #game("black")
                print("go")

while True:

    start()

