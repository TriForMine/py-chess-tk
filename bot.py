from tree import Node
from utils import calculate_total_score, enemy_color


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

    def generate_minimax_subtree(self, tree, depth=0, grid=None, player="black"):
        # Stop when the tree has been fully traversed
        if depth == 0:
            return None

        # Goes through all the possible capture movements
        for (s, e) in self.board.get_color_captures_moves(player, grid):

            piece = self.board.get_piece_at_position(s[0], s[1], grid)

            # Be sure that the provided movement is valid
            if piece and self.board.is_position_in_bound(e[0], e[1]):
                target = self.board.get_piece_at_position(e[0], e[1], grid)

                # Be sure that the target isn't an ally
                if target and target.color != player:
                    # Simulate the score after a movement
                    (new_grid, score) = self.calculate_movement_score(s, e, grid)
                    # Make a new node containing the movement information and the score
                    node = Node((s, e, score))

                    # Recursively generate all the possible movements, after the previous movement was made
                    self.generate_minimax_subtree(
                        node, depth - 1, new_grid, enemy_color(player)
                    )

                    # Add the node the root
                    tree.add_node(node)

        # Goes through all the possible movements
        for (s, e) in self.board.get_color_moves(player, grid):

            piece = self.board.get_piece_at_position(s[0], s[1], grid)

            # Be sure that the provided movement is valid
            if piece and self.board.is_position_in_bound(e[0], e[1]):
                # Be sure that the movement doesn't go over a piece
                if not self.board.check_piece_at_position(e[0], e[1], grid):
                    # Simulate the score after a movement
                    (new_grid, score) = self.calculate_movement_score(s, e, grid)
                    # Make a new node containing the movement information and the score
                    node = Node((s, e, score))

                    # Recursively generate all the possible movements, after the previous movement was made
                    self.generate_minimax_subtree(
                        node, depth - 1, new_grid, enemy_color(player)
                    )

                    # Add the node the root
                    tree.add_node(node)

    def generate_minimax_tree(self, depth=2, player="black"):
        # Generate the root, and set the data to the initial score.
        new_tree = Node(calculate_total_score(self.board.grid))

        # Generate all the nodes of that tree.
        self.generate_minimax_subtree(new_tree, depth, self.board.grid, player)

        return new_tree

    def minimax(self, tree, is_maximizing):
        if not tree.children:
            return tree.data[2]

        # If the player is the bot, try to get the best score.
        if is_maximizing:
            best_move = -9999
            for node in tree.children:
                # Get the best score you can get from that tree branch
                best_move = max(best_move, self.minimax(node, False))
            return best_move
        # If the player is not the bot, try to choose the best score for him.
        else:
            best_move = 9999
            for node in tree.children:
                # Get the best score you can get from that tree branch
                best_move = min(best_move, self.minimax(node, False))
            return best_move

    def get_minimax_move(self, depth=3, color="black"):
        # Generate the top root of the tree, and goes through the first layer
        tree = self.generate_minimax_tree(depth, color)
        best_next_score = 9999
        best_next_node = None

        # Goes through all the children, and choose the next move that should be done.
        for node in tree.children:
            node_minimax = self.minimax(node, color == "white")
            if best_next_score > node_minimax:
                best_next_score = node_minimax
                best_next_node = node.data
        return best_next_node
