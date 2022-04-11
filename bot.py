from collections import defaultdict
from math import inf
from piece import Piece
from utils import calculate_total_score
from typings import Tuple, DefaultDict, Optional


class Bot:
    def __init__(self, board, depth=3):
        self.board = board
        self.depth = depth

    def play(self, color="black", grid=None):
        return self.get_negamax_move(self.depth, color, grid)

    def calculate_movement_score(self, p1, p2, grid=None):
        # If no grid is provided, use the board grid as default
        if not grid:
            grid = self.board.grid

        # Clone the grid, to simulate the movement and calculate the new board score.
        tmp = self.board.clone_grid(grid)
        # Move the piece from p1 to p2
        tmp[p2], tmp[p1] = tmp[p1], None

        return tmp, calculate_total_score(tmp)

    def quiescence_search(self, grid, alpha, beta):
        """
        Quiescence search is required to avoid move that are dangerous.
        As explained here: https://www.chessprogramming.org/Quiescence_Search
        """
        last_score = calculate_total_score(grid)

        if last_score >= beta:
            return beta
        alpha = max(alpha, last_score)

        new_moves = self.board.filter_illegal_moves(
            self.board.get_color_all_moves("black", grid), "black"
        )

        for move in new_moves:
            if self.board.is_capture_move(move, grid):
                tmp = self.board.clone_grid(grid)
                (s, e) = move
                # Move the piece from s to e
                tmp[e] = tmp[s].clone()
                tmp.pop(s)

                score = -self.quiescence_search(grid, -beta, -alpha)

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    def negamax(
        self,
        depth,
        grid: DefaultDict[int, int], Optional[Piece]],
        is_maximizing,
        alpha,
        beta,
    ):
        if depth == 0:
            return -self.quiescence_search(grid, alpha, beta)

        # Get all the moves possible on the new grid.
        new_moves = self.board.filter_illegal_moves(
            self.board.get_color_all_moves("black", grid), "black"
        )

        best_score = -inf
        for (s, e) in new_moves:
            # Clone the grid so movement can be done without impacting the game.
            tmp = self.board.clone_grid(grid)

            # Move the piece from s to e
            tmp[e] = tmp[s].clone()
            tmp.pop(s)

            # Ignore illegal moves
            if self.board.is_color_in_check("black", tmp):
                continue

            score = -self.negamax(depth - 1, tmp, not is_maximizing, -beta, -alpha)

            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score

        return best_score

    def get_negamax_move(self, depth=3, color="black", grid=None):
        if not grid:
            grid = self.board.grid

        best_next_score = -inf
        best_next_node = None

        alpha = -inf
        beta = inf

        # Goes through all the children, and choose the next move that should be done.
        for (s, e) in self.board.filter_illegal_moves(
            self.board.get_color_all_moves("black", grid), "black"
        ):
            tmp = self.board.clone_grid(grid)
            # Move the piece from s to e
            tmp[e] = tmp[s].clone()
            tmp.pop(s)

            # Ignore illegal moves
            if self.board.is_color_in_check("black", tmp):
                continue

            node_minimax = self.negamax(depth - 1, tmp, color == "white", -beta, -alpha)

            if best_next_score < node_minimax:
                best_next_score = node_minimax
                best_next_node = (s, e)

            if node_minimax > alpha:
                alpha = node_minimax

        return best_next_node
