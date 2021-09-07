import copy

import Cell
import main


class Add:
    @classmethod
    def wall(cls, cell, turn):
        import copy
        # cell 벽을 추가할 좌표
        result_board = copy.deepcopy(main.board_array)
        x, y = cell
        if turn == "vertical":
            result_board[x, y] = 4
            result_board[x + 1, y] = 4
            result_board[x - 1, y] = 4
        elif turn == "horizon":
            result_board[x, y] = 4
            result_board[x, y + 1] = 4
            result_board[x, y - 1] = 4
        return result_board


class Modify:
    @classmethod
    def user(cls, temp_board, pos_that_user_go, user):
        user_array = Cell.user(user)
        result_board = copy.deepcopy(temp_board)
        array_that_user_go = Cell.click(pos_that_user_go)
        result_board[user_array] = 0
        if user == "black":
            result_board[array_that_user_go] = 1
        elif user == "white":
            result_board[array_that_user_go] = 2
        return result_board
