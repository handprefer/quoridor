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
    pygame.draw.polygon(screen,(150,150,150),[(30,63),(50,43),(150,43),(170,63),(170,163),(150,183),(50,183),(30,163)])
    pygame.draw.polygon(screen,(150,150,150),[(50,243),(170,243),(170,383),(30,383),(30,263)])
    pygame.draw.polygon(screen,(150,150,150),[(750,43),(870,43),(870,183),(730,183),(730,63)])
    pygame.draw.polygon(screen,(150,150,150),[(750,243),(870,243),(870,383),(730,383),(730,263)])

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

  
def user_cell(turn):   #ex) location=click_cell(pygame.mouse.get_pos()))
    if turn=="black":
        position=black_user.pos
    else:
        position=white_user.pos
    wall_size=0;
    
    first_x=position[0]-198-56*((position[0]-198)//56)    #0~55
    i=0
    if first_x//28>0:
        mid_x=(first_x-56)*(-1)
    else:
        mid_x=first_x
    if mid_x<=wall_size:
        if first_x//28>0:
            i=(((position[0]-198)//56)+1)*2
        else:
            i=((position[0]-198)//56)*2
    else:
        i=((position[0]-198)//56)*2+1
    if (position[0]-198)%56==0:
        i=((position[0]-198)//56)*2
    
    first_y=position[1]+2-56*((position[1]+2)//56)    #0~55
    j=0
    if first_y//28>0:
        mid_y=(first_y-56)*(-1)
    else:
        mid_y=first_y
    if mid_y<=wall_size:
        if first_y//28>0:
            j=(((position[1]+2)//56)+1)*2
        else:
            j=((position[1]+2)//56)*2
    else:
        j=((position[1]+2)//56)*2+1
    if (position[1]+2)%56==0:
        j=((position[1]+2)//56)*2
    return (i,j)

def user_checker(turn): #클릭한곳에 돌 이동 가능여부 판단
    location=click_cell(pygame.mouse.get_pos())
    x=user_cell(turn)[0]
    y=user_cell(turn)[1]
    click_x=location[0]
    click_y=location[1]
    if click_x==x and click_y==y-4: #뛰어넘기 위쪽
        if board_array[x][y-1]==3 and board_array[x][y-2]!=0 and board_array[x][y-3]==3:
            return True
    elif click_x==x and click_y==y+4: #뛰어넘기 아래쪽
        if board_array[x][y+1]==3 and board_array[x][y+2]!=0 and board_array[x][y+3]==3:
            return True
    elif click_x==x-4 and click_y==y: #뛰어넘기 오른쪽
        if board_array[x-1][y]==3 and board_array[x-2][y]!=0 and board_array[x-3][y]==3:
            return True
    elif click_x==x+4 and click_y==y: #뛰어넘기 오른쪽
        if board_array[x+1][y]==3 and board_array[x+2][y]!=0 and board_array[x+3][y]==3:
            return True
    elif click_x==x+2 and click_y==y-2: #오른쪽 위
        if (board_array[x+1][y]==3 and board_array[x+2][y]!=0 and board_array[x+3][y]==4 and board_array[x+2][y-1]==3) or \
                (board_array[x][y-1]==3 and board_array[x][y-2]!=0 and board_array[x][y-3]==4 and board_array[x+1][y-2]==3):
            return True
    elif click_x==x-2 and click_y==y-2: #왼쪽 위
        if (board_array[x-1][y]==3 and board_array[x-2][y]!=0 and board_array[x-3][y]==4 and board_array[x-2][y-1]==3) or \
                (board_array[x][y-1]==3 and board_array[x][y-2]!=0 and board_array[x][y-3]==4 and board_array[x-1][y-2]==3):
            return True
    elif click_x==x+2 and click_y==y+2: #오른쪽 아래
        if (board_array[x+1][y]==3 and board_array[x+2][y]!=0 and board_array[x+3][y]==4 and board_array[x+2][y+1]==3) or \
                (board_array[x][y+1]==3 and board_array[x][y+2]!=0 and board_array[x][y+3]==4 and board_array[x+1][y+2]==3):
            return True
    elif click_x==x-2 and click_y==y+2: #왼쪽 아래
        if (board_array[x-1][y]==3 and board_array[x-2][y]!=0 and board_array[x-3][y]==4 and board_array[x-2][y+1]==3) or \
                (board_array[x][y+1]==3 and board_array[x][y+2]!=0 and board_array[x][y+3]==4 and board_array[x-1][y+2]==3):
            return True
    elif click_x==x and click_y==y-2: #위쪽
        if board_array[x][y-1]==3:
            return True
    elif click_x==x and click_y==y+2: #아래쪽
        if board_array[x][y+1]==3:
            return True
    elif click_x==x-2 and click_y==y: #위쪽
        if board_array[x-1][y]==3:
            return True
    elif click_x==x+2 and click_y==y: #아래쪽
        if board_array[x+1][y]==3:
            return True
    
    return False


def click_cell(position):   #ex) location=click_cell(pygame.mouse.get_pos()))
    wall_size=3;
    
    first_x=position[0]-198-56*((position[0]-198)//56)    #0~55
    i=0
    if first_x//28>0:
        mid_x=(first_x-56)*(-1)
    else:
        mid_x=first_x
    if mid_x<=wall_size:
        if(first_x//28>0):
            i=(((position[0]-198)//56)+1)*2
        else:
            i=((position[0]-198)//56)*2
    else:
        i=((position[0]-198)//56)*2+1
    if (position[0]-198)%56==0:
        i=((position[0]-198)//56)*2
    
    first_y=position[1]+2-56*((position[1]+2)//56)    #0~55
    j=0
    if first_y//28>0:
        mid_y=(first_y-56)*(-1)
    else:
        mid_y=first_y
    if mid_y<=wall_size:
        if(first_y//28>0):
            j=(((position[1]+2)//56)+1)*2
        else:
            j=((position[1]+2)//56)*2
    else:
        j=((position[1]+2)//56)*2+1
    if (position[1]+2)%56==0:
        j=((position[1]+2)//56)*2
    return (i,j)


# 게임룰에 맞는 행동인지 체크하는 함수#####################################################################


def user_checker(turn):
    location = click_cell(pygame.mouse.get_pos())
    print(board_array[location[0], location[1]])
    print(location)
    print(pygame.mouse.get_pos())


black_user_can_go = False
white_user_can_go = False


def wall_checker():
    ...


# 게임을 진행할때 작동하는 함수들#####################################################################


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
                        game_black(turn)
                        user_checker(turn)
                    elif turn == "white":
                        game_white(turn)
                elif wall_click_event(turn, "vertical"):
                    game_vertical(turn)
                elif wall_click_event(turn, "horizon"):
                    game_horizon(turn)


def game_vertical(turn):
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_wall = Object("세로벽.png", [0, 0], (4, 52))
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


def game_horizon(turn):
    display_base_objects()
    board_loading()
    pygame.display.update()
    temp_wall = Object("가로벽.png", [0, 0], (52, 3))
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
                elif wall_click_event(turn, "vertical"):
                    game_vertical(turn)
                # 벽을 설치하는 로직
                elif True:  # board_check(pygame.mouse.get_pos())
                    make_wall(pygame.mouse.get_pos(), "horizon")
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
                elif wall_click_event(turn, "horizon"):
                    game_horizon(turn)
                elif wall_click_event(turn, "vertical"):
                    game_vertical(turn)
                # User Check
                elif True:
                    ...
        display_base_objects()
        board_loading()
        screen.blit(temp_user.img,
                    [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                    )
        pygame.display.update()


def game_white(turn):
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
                elif wall_click_event(turn, "horizon"):
                    game_horizon(turn)
                elif wall_click_event(turn, "vertical"):
                    game_vertical(turn)
                # User Check
                elif True:
                    ...
        display_base_objects()
        board_loading()
        screen.blit(temp_user.img,
                    [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                    )
        pygame.display.update()


# 보드 배열관련 함수#####################################################################


def make_wall(pos_that_make_wall, type):
    for j in range(8):
        if 246 + j * 55 <= pos_that_make_wall[0] <= 266 + j * 55:
            for i in range(8):
                if 45 + i * 55 <= pos_that_make_wall[1] <= 65 + i * 55:
                    if type == "vertical":
                        board_array[(2 + 2 * i) - 1, (2 + 2 * j)] = 4
                        board_array[2 + 2 * i, 2 + 2 * j] = 4
                        board_array[(2 + 2 * i) + 1, (2 + 2 * j)] = 4
                    elif type == "horizon":
                        board_array[(2 + 2 * i), (2 + 2 * j) - 1] = 4
                        board_array[2 + 2 * i, 2 + 2 * j] = 4
                        board_array[(2 + 2 * i), (2 + 2 * j) + 1] = 4


def modify_user(pos_that_user_go, user):
    ...


######################################################################


pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("쿼리도")
clock = pygame.time.Clock()

board_array = np.zeros((19, 19))
board_init()

board = Object("판.png", [200, 0], (500, 500))
horizon_wall1 = Object("가로벽.png", [44, 100], (111, 3))
vertical_wall1 = Object("세로벽.png", [99, 247], (3, 111))
horizon_wall2 = Object("가로벽.png", [744, 300], (111, 3))
vertical_wall2 = Object("세로벽.png", [799, 47], (3, 111))
black_user = Object("흑.png", [203, 224], (55, 55))
white_user = Object("백.png", [647, 224], (55, 55))

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    game("black")