import main
import pygame


def base_objects():
    main.screen.fill((255, 255, 255))
    pygame.draw.rect(main.screen, (0, 0, 0), [33, 40, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [33, 180, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [733, 40, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [733, 180, 130, 130])
    main.screen.blits(
        (
            (main.board.img, main.board.pos),
            (main.horizon_wall1.img, main.horizon_wall1.pos),
            (main.horizon_wall2.img, main.horizon_wall2.pos),
            (main.vertical_wall1.img, main.vertical_wall1.pos),
            (main.vertical_wall2.img, main.vertical_wall2.pos)
        )
    )


def board():
    temp_vertical = main.Object("세로벽.png", [0, 0], (3, 111))
    temp_horizon = main.Object("가로벽.png", [0, 0], (111, 3))
    for y in range(19):
        for x in range(19):
            if main.board_array[y, x] == 4:
                if not (x % 2 == 0 and y % 2 == 0) and not (x == 0 or y == 0) and not (x == 18 or y == 18):
                    if x % 2 == 0:
                        main.screen.blit(temp_vertical.img, [200 + 27.8 * x, 28 * (y - 1)])
                    elif y % 2 == 0:
                        main.screen.blit(temp_horizon.img, [202 + 27.8 * (x - 1), 27.7 * y])
        main.screen.blits(
            (
                (main.black_user.img, main.black_user.pos),
                (main.white_user.img, main.white_user.pos)
            )
        )
