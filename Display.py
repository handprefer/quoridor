import pygame

board_img = pygame.image.load("판.png")
horizon_wall_img = pygame.image.load("가로벽big.png")
vertical_wall_img = pygame.image.load("세로벽big.png")


def base_objects():
    import main
    main.screen.fill((255, 255, 255))
    pygame.draw.rect(main.screen, (0, 0, 0), [33, 40, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [33, 180, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [733, 40, 130, 130])
    pygame.draw.rect(main.screen, (0, 0, 0), [733, 180, 130, 130])
    main.screen.blits(
        (
            (board_img, [200, 0]),
            (horizon_wall_img, [44, 100]),
            (horizon_wall_img, [744, 100]),
            (vertical_wall_img, [97, 190]),
            (vertical_wall_img, [797, 190])
        )
    )


def board():
    import main
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


def base(func):
    def wrapper(*args, **kwargs):
        base_objects()
        board()
        pygame.display.update()
        func(*args, **kwargs)

    return wrapper
