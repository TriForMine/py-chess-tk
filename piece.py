from tkinter import PhotoImage


class Piece:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.photo = {"black": None, "white": None}

    def name(self):
        raise "Name method need to be overwritten"

    def possible_moves(self, x, y):
        raise "The piece doesn't implement any movements"

    def get_moves(self, x, y):
        return self.possible_moves(x, y)

    def horizontal(self, x, y, distance):
        res = []
        for offset_x in range(1, distance + 1):
            (pos_x, pos_y) = (x + offset_x, y)
            if not self.board.is_position_in_bound(pos_x, pos_y) or self.board.check_piece_at_position(pos_x, pos_y):
                break
            res.append((pos_x, pos_y))

        for offset_x in range(1, distance + 1):
            (pos_x, pos_y) = (x - offset_x, y)
            if not self.board.is_position_in_bound(pos_x, pos_y) or self.board.check_piece_at_position(pos_x, pos_y):
                break
            res.append((pos_x, pos_y))

        return res

    def vertical(self, x, y, distance, both_direction):
        res = []

        if self.color == "black" or both_direction:
            for offset_y in range(1, distance + 1):
                (pos_x, pos_y) = (x, y + offset_y)
                if not self.board.is_position_in_bound(pos_x, pos_y) or self.board.check_piece_at_position(pos_x, pos_y):
                    break
                res.append((pos_x, pos_y))

        if self.color == "white" or both_direction:
            for offset_y in range(1, distance + 1):
                (pos_x, pos_y) = (x, y - offset_y)
                if not self.board.is_position_in_bound(pos_x, pos_y) or self.board.check_piece_at_position(pos_x, pos_y):
                    break
                res.append((pos_x, pos_y))

        return res

    def diagonal(self, x, y, distance):
        res = []

        for i in range(4):
            for offset in range(1, distance + 1):
                if i == 0:
                    (pos_x, pos_y) = (x + offset, y + offset)
                elif i == 1:
                    (pos_x, pos_y) = (x - offset, y + offset)
                elif i == 2:
                    (pos_x, pos_y) = (x - offset, y - offset)
                else:
                    (pos_x, pos_y) = (x + offset, y - offset)

                if not self.board.is_position_in_bound(pos_x, pos_y) or self.board.check_piece_at_position(pos_x, pos_y):
                     break
                res.append((pos_x, pos_y))

        return res

    def image(self, cell_size):
        if self.photo[self.color] is None:
            # Load image from file
            self.photo[self.color] = PhotoImage(file=self.image_path())
            # Resize image to the correct scale
            self.photo[self.color] = self.photo[self.color].subsample(
                1024 // cell_size, 1024 // cell_size
            )

        return self.photo[self.color]


class Pawn(Piece):
    def possible_moves(self, x, y):
        if self.color == "white" and y == 6 or self.color == "black" and y == 1:
            return self.vertical(x, y, 2, False)
        else:
            return self.vertical(x, y, 1, False)

    def image_path(self):
        return f"./images/pawn_{self.color}.png"


class Knight(Piece):
    # Knight has custom movements, collisions isn't important
    def get_moves(self, x, y):
        res = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for offset in offsets:
            res.append((x + offset[0], y + offset[1]))
        return res

    def image_path(self):
        return f"./images/knight_{self.color}.png"


class Rook(Piece):
    def possible_moves(self, x, y):
        return self.horizontal(x, y, 8) + self.vertical(x, y, 8, True)

    def image_path(self):
        return f"./images/rook_{self.color}.png"


class Bishop(Piece):
    def possible_moves(self, x, y):
        return self.diagonal(x, y, 8)

    def image_path(self):
        return f"./images/bishop_{self.color}.png"


class Queen(Piece):
    def possible_moves(self, x, y):
        return self.horizontal(x, y, 8) + self.vertical(x, y, 8, True) + self.diagonal(x, y, 8)

    def image_path(self):
        return f"./images/queen_{self.color}.png"


class King(Piece):
    def possible_moves(self, x, y):
        return self.horizontal(x, y, 1) + self.vertical(x, y, 1, True) + self.diagonal(x, y, 1)

    def image_path(self):
        return f"./images/king_{self.color}.png"
