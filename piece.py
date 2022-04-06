from tkinter import PhotoImage

from consts import (
    pawnEvalBlack,
    pawnEvalWhite,
    knightEval,
    rookEvalWhite,
    rookEvalBlack,
    bishopEvalWhite,
    bishopEvalBlack,
    evalQueen,
    kingEvalBlack,
    kingEvalWhite,
)

photo = {}


class Piece:
    def __init__(self, color: str):
        self.color = color

    def get_score(self, x, y):
        raise Exception("get_score() method need to be overwritten")

    @staticmethod
    def name():
        raise Exception("Name method need to be overwritten")

    @staticmethod
    def possible_moves(board, x: int, y: int, capture: bool):
        raise Exception("The piece doesn't implement any movements")

    @staticmethod
    def clone():
        raise Exception("The piece doesn't implement clone()")

    def get_moves(self, board, x: int, y: int):
        return self.possible_moves(board, x, y, False)

    # That function will only be overwritten by the pawn.
    def get_capture_moves(self, board, x: int, y: int):
        return self.possible_moves(board, x, y, True)

    @staticmethod
    def horizontal(board, x: int, y: int, distance: int, capture: bool):
        """
        Check for horizontal movement
        """
        res = []

        # Right
        for offset_x in range(1, distance + 1):
            (pos_x, pos_y) = (x + offset_x, y)
            if not board.is_position_in_bound(
                pos_x, pos_y
            ) or board.check_piece_at_position(pos_x, pos_y):
                if capture:
                    res.append((pos_x, pos_y))
                break
            res.append((pos_x, pos_y))

        # Left
        for offset_x in range(1, distance + 1):
            (pos_x, pos_y) = (x - offset_x, y)
            if not board.is_position_in_bound(
                pos_x, pos_y
            ) or board.check_piece_at_position(pos_x, pos_y):
                if capture:
                    res.append((pos_x, pos_y))
                break
            res.append((pos_x, pos_y))

        return res

    def vertical(
        self, board, x: int, y: int, distance: int, both_direction: bool, capture: bool
    ):
        """
        Check for vertical movement
        """
        res = []

        # Down
        if self.color == "black" or both_direction:
            for offset_y in range(1, distance + 1):
                (pos_x, pos_y) = (x, y + offset_y)
                if not board.is_position_in_bound(
                    pos_x, pos_y
                ) or board.check_piece_at_position(pos_x, pos_y):
                    if capture:
                        res.append((pos_x, pos_y))
                    break
                res.append((pos_x, pos_y))

        # Up
        if self.color == "white" or both_direction:
            for offset_y in range(1, distance + 1):
                (pos_x, pos_y) = (x, y - offset_y)
                if not board.is_position_in_bound(
                    pos_x, pos_y
                ) or board.check_piece_at_position(pos_x, pos_y):
                    if capture:
                        res.append((pos_x, pos_y))
                    break
                res.append((pos_x, pos_y))

        return res

    def diagonal(
        self, board, x: int, y: int, distance: int, both_direction: bool, capture: bool
    ):
        """
        Check for diagonal movement
        """
        res = []

        if self.color == "black" or both_direction:
            for i in range(2):
                for offset in range(1, distance + 1):
                    if i == 0:
                        (pos_x, pos_y) = (x + offset, y + offset)
                    else:
                        (pos_x, pos_y) = (x - offset, y + offset)

                    if not board.is_position_in_bound(
                        pos_x, pos_y
                    ) or board.check_piece_at_position(pos_x, pos_y):
                        if capture:
                            res.append((pos_x, pos_y))
                        break
                    res.append((pos_x, pos_y))

        if self.color == "white" or both_direction:
            for i in range(2):
                for offset in range(1, distance + 1):
                    if i == 0:
                        (pos_x, pos_y) = (x - offset, y - offset)
                    else:
                        (pos_x, pos_y) = (x + offset, y - offset)

                    if not board.is_position_in_bound(
                        pos_x, pos_y
                    ) or board.check_piece_at_position(pos_x, pos_y):
                        if capture:
                            res.append((pos_x, pos_y))
                        break
                    res.append((pos_x, pos_y))

        return res

    @staticmethod
    def image_path() -> str:
        raise Exception("The piece doesn't implement image_path")

    def image(self, cell_size: int):
        # Check if image is in cache, if not load it
        if type(self).__name__ not in photo:
            photo[type(self).__name__] = {"black": None, "white": None}
        if photo[type(self).__name__][self.color] is None:
            # Load image from file
            photo[type(self).__name__][self.color] = PhotoImage(file=self.image_path())

            # Resize image to the correct scale
            photo[type(self).__name__][self.color] = photo[type(self).__name__][
                self.color
            ].subsample(
                photo[type(self).__name__][self.color].width() // cell_size,
                photo[type(self).__name__][self.color].height() // cell_size,
            )

        return photo[type(self).__name__][self.color]


class Pawn(Piece):
    def get_score(self, x, y):
        return (
            10 + pawnEvalWhite[y][x] if self.color == "white" else pawnEvalBlack[y][x]
        )

    def possible_moves(self, board, x: int, y: int, capture: bool):
        if self.color == "white" and y == 6 or self.color == "black" and y == 1:
            return self.vertical(board, x, y, 2, False, capture)
        else:
            return self.vertical(board, x, y, 1, False, capture)

    def get_capture_moves(self, board, x: int, y: int):
        if self.color == "white" and y == 6 or self.color == "black" and y == 1:
            return self.diagonal(board, x, y, 1, False, True)
        else:
            return self.diagonal(board, x, y, 1, False, True)

    def image_path(self):
        return f"./images/pawn_{self.color}.png"

    def clone(self):
        return Pawn(self.color)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_score(self, x, y):
        return 30 + knightEval[y][x]

    # Knight has custom movements, it doesn't uses horizontal/vertical/diagonal
    def possible_moves(self, board, x: int, y: int, capture: bool):
        res = []
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for offset in offsets:
            res.append((x + offset[0], y + offset[1]))
        return res

    def image_path(self):
        return f"./images/knight_{self.color}.png"

    def clone(self):
        return Knight(self.color)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_score(self, x, y):
        return (
            50 + rookEvalWhite[y][x] if self.color == "white" else rookEvalBlack[y][x]
        )

    def possible_moves(self, board, x: int, y: int, capture: bool):
        return self.horizontal(board, x, y, 8, capture) + self.vertical(
            board, x, y, 8, True, capture
        )

    def image_path(self):
        return f"./images/rook_{self.color}.png"

    def clone(self):
        return Rook(self.color)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_score(self, x, y):
        return (
            30 + bishopEvalWhite[y][x]
            if self.color == "white"
            else bishopEvalBlack[y][x]
        )

    def possible_moves(self, board, x: int, y: int, capture: bool):
        return self.diagonal(board, x, y, 8, True, capture)

    def image_path(self):
        return f"./images/bishop_{self.color}.png"

    def clone(self):
        return Bishop(self.color)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_score(self, x, y):
        return 90 + evalQueen[y][x]

    def possible_moves(self, board, x: int, y: int, capture: bool):
        return (
            self.horizontal(board, x, y, 8, capture)
            + self.vertical(board, x, y, 8, True, capture)
            + self.diagonal(board, x, y, 8, True, capture)
        )

    def image_path(self):
        return f"./images/queen_{self.color}.png"

    def clone(self):
        return Queen(self.color)


class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_score(self, x, y):
        return (
            900 + kingEvalWhite[y][x] if self.color == "white" else kingEvalBlack[y][x]
        )

    def possible_moves(self, board, x: int, y: int, capture: bool):
        return (
            self.horizontal(board, x, y, 1, capture)
            + self.vertical(board, x, y, 1, True, capture)
            + self.diagonal(board, x, y, 1, True, capture)
        )

    def image_path(self):
        return f"./images/king_{self.color}.png"

    def clone(self):
        return King(self.color)
