import pygame
import random

pygame.init()
screen=pygame.display.set_mode((900,500))
pygame.display.set_caption("쿼리도")

case=0
turn=1
image=["판.png","가로벽.png","세로벽.png","흑.png","백.png"]
t_surface = screen.convert_alpha()  

font_title=pygame.font.SysFont('malgungothic',80)
text_title=font_title.render("쿼리도",True,(0,0,0))
font_start=pygame.font.SysFont('malgungothic',30)
text_start=font_start.render("start",True,(0,0,0))

character=[]
for i in range(5):
    character.append(pygame.image.load(image[i]))

clock = pygame.time.Clock()
run = True

# Game Loop
while run:
    # 1) 사용자 입력 처리
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if case==0:
                print(pygame.mouse.get_pos())
    t_surface.fill((255, 255, 255, 200))                    # t_surface 전체를 투명한 검정색으로 지운다
 
    #pygame.draw.rect(screen, (0, 0, 255, 127), (30, 30, 40, 40))  # t_surface에 투명도를 적용하여 그려줌
    
    if(case==0):
        screen.blit(character[0],(200,0))
        screen.blit(character[1],(40,100))
        screen.blit(character[2],(99,270))
        screen.blit(character[1],(740,380))
        screen.blit(character[2],(799,100))
        screen.blit(character[3],(203,224))
        screen.blit(character[4],(647,224))
        screen.blit(t_surface, (0, 0))  
        screen.blit(text_title,(330,150))
        screen.blit(text_start,(420,267))
    pygame.display.flip()
    clock.tick(1000)


 
pygame.quit()

