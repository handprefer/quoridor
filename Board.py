import copy
import Cell


class Add:
    @classmethod
    def wall(cls, temp_board, pos_that_add_wall, turn):
        result_board = copy.deepcopy(temp_board)
        array = Cell.click(pos_that_add_wall)
        x, y = array
        if x % 2 == 0 and y % 2 == 0:
            if turn == "vertical":
                if not (result_board[x, y] == 4 or result_board[x + 1, y] == 4 or result_board[x - 1, y] == 4):
                    result_board[array[0], array[1]] = 4
                    result_board[array[0] + 1, array[1]] = 4
                    result_board[array[0] - 1, array[1]] = 4
                    result_board[array[0] + 2, array[1]] = 4
                    result_board[array[0] - 2, array[1]] = 4
            elif turn == "horizon":
                if not (result_board[x, y] == 4 or result_board[x, y + 1] == 4 or result_board[x, y - 1] == 4):
                    result_board[array[0], array[1]] = 4
                    result_board[array[0], array[1] + 1] = 4
                    result_board[array[0], array[1] - 1] = 4
                    result_board[array[0], array[1] + 2] = 4
                    result_board[array[0], array[1] - 2] = 4
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
