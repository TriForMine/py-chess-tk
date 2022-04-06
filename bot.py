from math import inf
from utils import calculate_total_score


class Bot:
    def __init__(self, board, depth=3):
        self.board = board
        self.depth = depth

    def play(self, color="black"):
        return self.get_minimax_move(self.depth, color)

    def calculate_movement_score(self, p1, p2, grid=None):
        # If no grid is provided, use the board grid as default
        if not grid:
            grid = self.board.grid

        # Clone the grid, to simulate the movement and calculate the new board score.
        tmp = self.board.clone_grid(grid)
        (p1_x, p1_y) = p1
        (p2_x, p2_y) = p2
        # Move the piece from p1 to p2
        tmp[p2_y][p2_x], tmp[p1_y][p1_x] = tmp[p1_y][p1_x], None

        return tmp, calculate_total_score(tmp)

    def minimax(self, depth, grid, is_maximizing, alpha, beta):
        if depth == 0:
            return -calculate_total_score(grid)

        # Get all the moves possible on the new grid.
        new_moves = self.board.get_color_all_moves("black", grid)

        # If the player is the bot, try to get the best score.
        if is_maximizing:
            best_move = -inf
            for (s, e) in new_moves:
                # Clone the grid so movement can be done without impacting the game.
                tmp = self.board.clone_grid(grid)

                (s_x, s_y) = s
                (e_x, e_y) = e
                # Move the piece from s to e
                tmp[e_y][e_x], tmp[s_y][s_x] = tmp[s_y][s_x], None

                # Get the best score you can get from that tree branch
                best_move = max(
                    best_move,
                    self.minimax(depth - 1, tmp, not is_maximizing, alpha, beta),
                )

                alpha = max(alpha, best_move)

                if beta <= alpha:
                    return best_move

            return best_move
        # If the player is not the bot, try to choose the best score for him.
        else:
            best_move = inf
            for (s, e) in new_moves:
                tmp = self.board.clone_grid(grid)

                (s_x, s_y) = s
                (e_x, e_y) = e
                # Move the piece from s to e
                tmp[e_y][e_x], tmp[s_y][s_x] = tmp[s_y][s_x], None

                # Get the best score you can get from that tree branch
                best_move = min(
                    best_move,
                    self.minimax(depth - 1, tmp, not is_maximizing, alpha, beta),
                )

                beta = min(beta, best_move)

                if beta <= alpha:
                    return best_move

            return best_move

    def get_minimax_move(self, depth=3, color="black"):
        best_next_score = 9999
        best_next_node = None

        # Goes through all the children, and choose the next move that should be done.
        for (s, e) in self.board.get_color_all_moves(color, self.board.grid):
            node_minimax = self.minimax(
                depth - 1, self.board.grid, color == "white", -10000, 10000
            )
            if best_next_score >= node_minimax:
                best_next_score = node_minimax
                best_next_node = (s, e)

        return best_next_node
