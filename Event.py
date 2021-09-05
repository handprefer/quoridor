import main
import Cell
import copy
import Board


class Click:
    @classmethod
    def user(cls, user, click_pos):
        if user == "black":
            if main.black_user.pos[0] < click_pos[0] < main.black_user.pos[0] + 55 and \
                    main.black_user.pos[1] < click_pos[1] < main.black_user.pos[1] + 55:
                return True
        if user == "white":
            if main.white_user.pos[0] < click_pos[0] < main.white_user.pos[0] + 55 and \
                    main.white_user.pos[1] < click_pos[1] < main.white_user.pos[1] + 55:
                return True
        return False

    @classmethod
    def wall(cls, user, wall, click_pos):
        if user == "black":
            if wall == "horizon":
                if 33 <= click_pos[0] <= 167 and 40 <= click_pos[1] <= 170:
                    return True
            elif wall == "vertical":
                if 33 <= click_pos[0] <= 167 and 180 <= click_pos[1] <= 310:
                    return True
        elif user == "white":
            if wall == "vertical":
                if 733 <= click_pos[0] <= 863 and 180 <= click_pos[1] <= 310:
                    return True
            if wall == "horizon":
                if 733 <= click_pos[0] <= 863 and 40 <= click_pos[1] <= 170:
                    return True
        return False


class Check:
    @classmethod
    def wall(cls, graph, start, end):
        if not graph:
            return False
        queue = [start]  # idx 0: 노드, idx 1: 이동 거리
        visit = {start, }  # 방문한 노드 저장 공간

        while queue:
            node = queue.pop(0)
            for near_node in graph[node]:
                if near_node not in visit:
                    if near_node[1] == end:
                        return True

                    visit.add(near_node)
                    queue.append(near_node)
        return False

    @classmethod
    def user(cls, turn, pos):  # 클릭한곳에 돌 이동 가능여부 판단
        location = Cell.click(pos)
        x = Cell.user(turn)[0]
        y = Cell.user(turn)[1]
        click_x = location[0]
        click_y = location[1]

        if click_x == x and click_y == y - 4:  # 뛰어넘기 왼쪽
            if main.board_array[x, y - 1] == 3 and main.board_array[x, y - 2] != 0 and main.board_array[x, y - 3] == 3:
                return True
        elif click_x == x and click_y == y + 4:  # 뛰어넘기 오른쪽
            if main.board_array[x, y + 1] == 3 and main.board_array[x, y + 2] != 0 and main.board_array[x, y + 3] == 3:
                return True
        elif click_x == x - 4 and click_y == y:  # 뛰어넘기 위쪽
            if main.board_array[x - 1, y] == 3 and main.board_array[x - 2, y] != 0 and main.board_array[x - 3, y] == 3:
                return True
        elif click_x == x + 4 and click_y == y:  # 뛰어넘기 아래쪽
            if main.board_array[x + 1, y] == 3 and main.board_array[x + 2, y] != 0 and main.board_array[x + 3, y] == 3:
                return True
        elif click_x == x + 2 and click_y == y - 2:  # 왼쪽 아래
            if (main.board_array[x + 1, y] == 3 and main.board_array[x + 2, y] != 0 and main.board_array[
                x + 3, y] == 4 and main.board_array[
                    x + 2, y - 1] == 3) or \
                    (main.board_array[x, y - 1] == 3 and main.board_array[x, y - 2] != 0 and main.board_array[
                        x, y - 3] == 4 and
                     main.board_array[x + 1, y - 2] == 3):
                return True
        elif click_x == x - 2 and click_y == y - 2:  # 오른쪽 아래

            if (main.board_array[x - 1, y] == 3 and main.board_array[x - 2, y] != 0 and main.board_array[
                x - 3, y] == 4 and main.board_array[
                    x - 2, y - 1] == 3) or \
                    (main.board_array[x, y - 1] == 3 and main.board_array[x, y - 2] != 0 and main.board_array[
                        x, y - 3] == 4 and
                     main.board_array[x - 1, y - 2] == 3):
                return True
        elif click_x == x + 2 and click_y == y + 2:  # 왼쪽 위
            if (main.board_array[x + 1, y] == 3 and main.board_array[x + 2, y] != 0 and main.board_array[
                x + 3, y] == 4 and main.board_array[
                    x + 2, y + 1] == 3) or \
                    (main.board_array[x, y + 1] == 3 and main.board_array[x, y + 2] != 0 and main.board_array[
                        x, y + 3] == 4 and
                     main.board_array[x + 1, y + 2] == 3):
                return True
        elif click_x == x - 2 and click_y == y + 2:  # 오른쪽 위
            if (main.board_array[x - 1, y] == 3 and main.board_array[x - 2, y] != 0 and main.board_array[
                x - 3, y] == 4 and main.board_array[
                    x - 2, y + 1] == 3) or \
                    (main.board_array[x, y + 1] == 3 and main.board_array[x, y + 2] != 0 and main.board_array[
                        x, y + 3] == 4 and
                     main.board_array[x - 1, y + 2] == 3):
                return True
        elif click_x == x and click_y == y - 2:  # 왼쪽
            if main.board_array[x, y - 1] == 3 and main.board_array[x, y - 2] == 0:
                return True
        elif click_x == x and click_y == y + 2:  # 오른쪽
            if main.board_array[x, y + 1] == 3 and main.board_array[x, y + 2] == 0:
                return True
        elif click_x == x - 2 and click_y == y:  # 위쪽
            if main.board_array[x - 1, y] == 3 and main.board_array[x - 2, y] == 0:
                return True
        elif click_x == x + 2 and click_y == y:  # 아래쪽
            if main.board_array[x + 1, y] == 3 and main.board_array[x + 2, y] == 0:
                return True
        return False


def make_graph(temp_board, pos_that_make_wall, user):
    result_board = copy.deepcopy(temp_board)
    result_board = Board.Add.wall(result_board, pos_that_make_wall, user)
    if result_board is None:
        return False
    graph = {}
    for x in range(19):
        for y in range(19):
            if not (x == 0 or x == 18 or y == 0 or y == 18):
                if result_board[x, y] == 0 or result_board[x, y] == 1 or result_board[x, y] == 2:
                    graph[(x, y)] = []
                    try:
                        # 아래쪽으로 갈 수 있는 경우
                        if result_board[x + 2, y] == 0 and result_board[x + 1, y] == 3:
                            graph[(x, y)].append((x + 2, y))
                        # 돌에 막힌 경우
                        elif (result_board[x + 2, y] == 1 or 2) and result_board[x + 1, y] == 3:
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x + 2, y - 2] == 0 and result_board[x + 2, y - 1] == 3:
                                graph[(x, y)].append((x + 2, y - 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x + 2, y + 2] == 0 and result_board[x + 2, y + 1] == 3:
                                graph[(x, y)].append((x + 2, y + 2))
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 4, y] == 0 and result_board[x + 3, y] == 3:
                                graph[(x, y)].append((x + 4, y))
                    except IndexError:
                        ...
                    try:
                        # 위쪽으로 갈 수 있는 경우
                        if result_board[x - 2, y] == 0 and result_board[x - 1, y] == 3:
                            graph[(x, y)].append((x - 2, y))
                        # 돌에 막힌 경우
                        elif (result_board[x - 2, y] == 1 or 2) and result_board[x - 1, y] == 3:
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x - 2, y - 2] == 0 and result_board[x - 2, y - 1] == 3:
                                graph[(x, y)].append((x - 2, y - 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x - 2, y + 2] == 0 and result_board[x - 2, y + 1] == 3:
                                graph[(x, y)].append((x - 2, y + 2))
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 4, y] == 0 and result_board[x - 3, y] == 3:
                                graph[(x, y)].append((x - 4, y))
                    except IndexError:
                        ...
                    try:
                        # 오른쪽으로 갈 수 있는 경우
                        if result_board[x, y + 2] == 0 and result_board[x, y + 1] == 3:
                            graph[(x, y)].append((x, y + 2))
                            # 돌에 막힌 경우
                        elif (result_board[x, y + 2] == 1 or 2) and result_board[x, y + 1] == 3:
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 2, y + 2] == 0 and result_board[x - 1, y + 2] == 3:
                                graph[(x, y)].append((x - 2, y + 2))
                            # 돌의 오른쪽이 뚫린 경우
                            if result_board[x, y + 4] == 0 and result_board[x, y + 3] == 3:
                                graph[(x, y)].append((x, y + 4))
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 2, y + 2] == 0 and result_board[x + 1, y + 2] == 3:
                                graph[(x, y)].append((x + 2, y + 2))
                    except IndexError:
                        ...
                    try:
                        # 왼쪽으로 갈 수 있는 경우
                        if result_board[x, y - 2] == 0 and result_board[x, y - 1] == 3:
                            graph[(x, y)].append((x, y - 2))
                        # 돌에 막힌 경우
                        elif (result_board[x, y - 2] == 1 or 2) and result_board[x, y - 1] == 3:
                            # 돌의 아래쪽이 뚫린 경우
                            if result_board[x + 2, y - 2] == 0 and result_board[x + 1, y - 2] == 3:
                                graph[(x, y)].append((x + 2, y - 2))
                            # 돌의 위쪽이 뚫린 경우
                            if result_board[x - 2, y - 2] == 0 and result_board[x - 1, y - 2] == 3:
                                graph[(x, y)].append((x - 2, y - 2))
                            # 돌의 왼쪽이 뚫린 경우
                            if result_board[x, y - 4] == 0 and result_board[x, y - 3] == 3:
                                graph[(x, y)].append((x, y - 4))
                    except IndexError:
                        ...
    return graph
