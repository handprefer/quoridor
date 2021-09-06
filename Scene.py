import sys

import pygame

import Board
import Cell
import Display
import Event
import Pos
import main


def game(turn):
    Display.base_objects()
    Display.board()
    if Cell.user("black")[1] == 17:
        win("black")
        return 0
    elif Cell.user("white")[1] == 1:
        win("white")
        return 0
    else:
        if turn == "black":
            text = main.text("Black", 30, 0, 0, 0)
            main.screen.blit(text, (70, 400))
        else:
            text = main.text("White", 30, 0, 0, 0)
            main.screen.blit(text, (770, 400))
        pygame.display.update()
        while True:
            main.clock.tick(3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if Event.Click.user(turn, event.pos):
                        if turn == "black":
                            black(turn)
                        elif turn == "white":
                            white(turn)
                    elif Event.Click.wall(turn, "vertical", event.pos):
                        vertical(turn)
                    elif Event.Click.wall(turn, "horizon", event.pos):
                        horizon(turn)


def white(turn):
    text = main.text("White", 30, 0, 0, 0)
    Display.base_objects()
    Display.board()
    pygame.display.update()
    temp_user = main.Object("백.png", list(pygame.mouse.get_pos()), (55, 55))
    while True:
        main.clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_user.pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Event.Click.wall(turn, "horizon", event.pos):
                    horizon(turn)
                elif Event.Click.wall(turn, "vertical", event.pos):
                    vertical(turn)
                elif Event.Check.user(turn, event.pos):
                    main.board_array = Board.Modify.user(main.board_array, event.pos, turn)
                    main.white_user.pos = Pos.white()
                    game("black")
        Display.base_objects()
        Display.board()
        main.screen.blit(text, (770, 400))
        main.screen.blit(temp_user.img,
                         [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                         )
        pygame.display.update()


def black(turn):
    text = main.text("Black", 30, 0, 0, 0)
    Display.base_objects()
    Display.board()
    pygame.display.update()
    temp_user = main.Object("흑.png", list(pygame.mouse.get_pos()), (55, 55))
    while True:
        main.clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_user.pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Event.Click.wall(turn, "horizon", event.pos):
                    horizon(turn)
                elif Event.Click.wall(turn, "vertical", event.pos):
                    vertical(turn)
                # User Check
                elif Event.Check.user(turn, event.pos):
                    main.board_array = Board.Modify.user(main.board_array, event.pos, "black")
                    main.black_user.pos = Pos.black()
                    game("white")
        Display.base_objects()
        Display.board()
        main.screen.blit(text, (70, 400))
        main.screen.blit(temp_user.img,
                         [temp_user.pos[0] - temp_user.size[0] // 2, temp_user.pos[1] - temp_user.size[1] // 2]
                         )
        pygame.display.update()


def horizon(turn):
    Display.base_objects()
    Display.board()
    pygame.display.update()
    temp_wall = main.Object("가로벽big.png", [0, 0], (108, 4))
    if turn == "black":
        text = main.text("Black", 30, 0, 0, 0)
        main.screen.blit(text, (70, 400))
    else:
        text = main.text("White", 30, 0, 0, 0)
        main.screen.blit(text, (770, 400))
    while True:
        main.clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_wall.pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Event.Click.user(turn, event.pos):
                    if turn == "black":
                        black(turn)
                    elif turn == "white":
                        white(turn)
                elif Event.Click.wall(turn, "vertical", event.pos):
                    vertical(turn)
                # 벽을 설치하는 로직
                # 보드판 안을 클릭했는지 확인
                elif 200 <= event.pos[0] <= 700:
                    graph = Event.make_graph(event.pos, "horizon")
                    if Event.Check.wall(
                            graph,
                            Cell.user("black"),
                            17,
                            Cell.click(event.pos),
                            "horizon"
                    ) is True and \
                            Event.Check.wall(
                                graph,
                                Cell.user("white"),
                                1,
                                Cell.click(event.pos),
                                "horizon"
                            ) is True:
                        main.board_array = Board.Add.wall(Cell.click(event.pos), "horizon")
                        if turn == "black":
                            game("white")
                        elif turn == "white":
                            game("black")
        Display.base_objects()
        Display.board()
        if turn == "black":
            main.screen.blit(text, (70, 400))
        else:
            main.screen.blit(text, (770, 400))
        main.screen.blit(temp_wall.img,
                         [temp_wall.pos[0] - temp_wall.size[0] // 2, temp_wall.pos[1] - temp_wall.size[1] // 2]
                         )
        pygame.display.update()


def vertical(turn):
    Display.base_objects()
    Display.board()
    pygame.display.update()
    temp_wall = main.Object("세로벽big.png", [0, 0], (4, 108))
    if turn == "black":
        text = main.text("Black", 30, 0, 0, 0)
        main.screen.blit(text, (70, 400))
    else:
        text = main.text("White", 30, 0, 0, 0)
        main.screen.blit(text, (770, 400))
    while True:
        main.clock.tick(59)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                temp_wall.pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 돌을 클릭한 경우
                if Event.Click.user(turn, event.pos):
                    if turn == "black":
                        black(turn)
                    elif turn == "white":
                        white(turn)
                # 벽을 클릭한 경우
                elif Event.Click.wall(turn, "horizon", event.pos):
                    horizon(turn)
                # 벽을 설치하는 로직
                elif 200 <= event.pos[0] <= 700:
                    if Event.Check.wall(
                            Event.make_graph(event.pos, "vertical"),
                            Cell.user("black"),
                            17,
                            Cell.click(event.pos),
                            "vertical"
                    ) is True and \
                            Event.Check.wall(
                                Event.make_graph(event.pos, "vertical"),
                                Cell.user("white"),
                                1,
                                Cell.click(event.pos),
                                "vertical"
                            ) is True:
                        print(1)
                        main.board_array = Board.Add.wall(Cell.click(event.pos), "vertical")
                        if Cell.user(turn)[1] == 17:
                            print("win")
                        if turn == "black":
                            game("white")
                        elif turn == "white":
                            game("black")
        Display.base_objects()
        Display.board()
        if turn == "black":
            main.screen.blit(text, (70, 400))
        else:
            main.screen.blit(text, (770, 400))
        main.screen.blit(temp_wall.img,
                         [temp_wall.pos[0] - temp_wall.size[0] // 2, temp_wall.pos[1] - temp_wall.size[1] // 2]
                         )
        pygame.display.update()


def win(user):
    main.screen.fill((255, 255, 255))
    if user == "black":
        msg = main.text("Black Win", 50, 0, 0, 0)
        main.screen.blit(msg, (350, 200))
    elif user == "white":
        msg = main.text("White Win", 50, 0, 0, 0)
        main.screen.blit(msg, (350, 200))
    pygame.display.update()
    while True:
        main.clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start()


def start():
    main.screen.fill((255, 255, 255))
    title_text = main.text("QUORIDOR", 70, 0, 0, 0)

    main.screen.blit(title_text, (275, 140))

    pygame.display.update()
    while True:
        main.clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                main.board_init()
                game("black")
