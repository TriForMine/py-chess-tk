from tkinter import PhotoImage


class Piece:
    def __init__(self, color):
        self.color = color
        self.photo = {"black": None, "white": None}

    def name(self):
        raise "Name method need to be overwritten"

    def possible_moves(self):
        pass

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
    def possible_moves(self):
        if self.color == "black":
            return [(0, 1)]
        else:
            return [(0, -1)]

    def image_path(self):
        return f"./images/pawn_{self.color}.png"


class Knight(Piece):
    def possible_moves(self):
        return [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def image_path(self):
        return f"./images/knight_{self.color}.png"


class Rook(Piece):
    def possible_moves(self):
        return [(0, y) for y in range(-8, 8) if y != 0] + [
            (x, 0) for x in range(-8, 8) if x != 0
        ]

    def image_path(self):
        return f"./images/rook_{self.color}.png"


class Bishop(Piece):
    def possible_moves(self):
        return [
            (x, y)
            for x in range(-8, 8)
            for y in range(-8, 8)
            if y != 0 and x != 0 and (x == y or x == -y)
        ]

    def image_path(self):
        return f"./images/bishop_{self.color}.png"


class Queen(Piece):
    def possible_moves(self):
        return (
            [(0, y) for y in range(-8, 8) if y != 0]
            + [(x, 0) for x in range(-8, 8) if x != 0]
            + [
                (x, y)
                for x in range(-8, 8)
                for y in range(-8, 8)
                if y != 0 and x != 0 and (x == y or x == -y)
            ]
        )

    def image_path(self):
        return f"./images/queen_{self.color}.png"


class King(Piece):
    def possible_moves(self):
        return [(-1, -1), (1, 1), (0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, -1)]

    def image_path(self):
        return f"./images/king_{self.color}.png"
