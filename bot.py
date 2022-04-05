from tree import Node
from utils import calculate_total_score, enemy_color


class Bot:
    def __init__(self, board, depth=3):
        self.board = board
        self.depth = depth

    def play(self, color="black"):
        return self.get_minimax_move(self.depth, color)

    def calculate_movement_score(self, p1, p2, grid=None):
        if not grid:
            grid = self.board.grid
        tmp = self.board.clone_grid(grid)
        (p1_x, p1_y) = p1
        (p2_x, p2_y) = p2
        tmp[p2_y][p2_x], tmp[p1_y][p1_x] = tmp[p1_y][p1_x], None
        return tmp, calculate_total_score(tmp)

    def generate_minimax_subtree(self, tree, depth=0, grid=None, player="black"):
        if depth == 0:
            return None

        for (s, e) in self.board.get_color_captures_moves(player, grid):
            piece = self.board.get_piece_at_position(s[0], s[1], grid)
            if piece and self.board.is_position_in_bound(e[0], e[1]):
                target = self.board.get_piece_at_position(e[0], e[1], grid)
                if target and target.color != player:
                    (new_grid, score) = self.calculate_movement_score(s, e, grid)
                    node = Node((s, e, score))

                    self.generate_minimax_subtree(
                        node, depth - 1, new_grid, enemy_color(player)
                    )

                    tree.add_node(node)

        for (s, e) in self.board.get_color_moves(player, grid):
            piece = self.board.get_piece_at_position(s[0], s[1], grid)
            if piece and self.board.is_position_in_bound(e[0], e[1]):
                if not self.board.check_piece_at_position(e[0], e[1], grid):
                    (new_grid, score) = self.calculate_movement_score(s, e, grid)

                    node = Node((s, e, score))

                    self.generate_minimax_subtree(
                        node, depth - 1, new_grid, enemy_color(player)
                    )

                    tree.add_node(node)

    def generate_minimax_tree(self, depth=2, grid=None, player="black"):
        if not grid:
            grid = self.board.grid

        new_tree = Node(calculate_total_score(grid))

        self.generate_minimax_subtree(new_tree, depth, grid, player)

        return new_tree

    def minimax(self, tree, is_maximizing):
        if not tree.children:
            return tree.data[2]

        if is_maximizing:
            best_move = -9999
            for node in tree.children:
                best_move = max(best_move, self.minimax(node, False))
            return best_move
        else:
            best_move = 9999
            for node in tree.children:
                best_move = min(best_move, self.minimax(node, False))
            return best_move

    def get_minimax_move(self, depth=3, color="black"):
        tree = self.generate_minimax_tree(depth)
        best_next_score = 9999
        best_next_node = None
        for node in tree.children:
            node_minimax = self.minimax(node, False)
            if best_next_score > node_minimax:
                best_next_score = node_minimax
                best_next_node = node.data
        return best_next_node
