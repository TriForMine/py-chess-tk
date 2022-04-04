from tkinter import Event

from piece import Pawn, Knight, Rook, Bishop, Queen, King, Piece


class Board:
    grid: list[list[Piece | None]]

    def __init__(self, canvas, width: int, height: int, cell_size: int):
        self.w = width
        self.h = height
        self.cellSize = cell_size
        self.grid = []
        self.canvas = canvas
        self.hoverPosition = None

        self.last_x = -1
        self.last_y = -1

        # Generate the grid matrix to empty by default
        for y in range(height):
            line = []
            for x in range(width):
                line.append(None)
            self.grid.append(line)

        self.reset_board()

    def render(self):
        """
        Render the board
        """

        # Clear existing canvas, as we will redraw everything.
        self.canvas.delete("all")

        # Draw the grid
        for y in range(self.h):
            for x in range(self.w):
                if (y - x) % 2 == 0:
                    fill = "#E3C16F"
                else:
                    fill = "#B88B4A"

                self.canvas.create_rectangle(
                    x * self.cellSize,
                    y * self.cellSize,
                    x * self.cellSize + self.cellSize,
                    y * self.cellSize + self.cellSize,
                    fill=fill,
                    outline="",
                )

        # Show possible movements if the user hover a piece
        if self.hoverPosition:
            (x, y) = self.hoverPosition[0], self.hoverPosition[1]
            piece = self.get_piece_at_position(x, y)
            movements = piece.get_moves(x, y)

            for offset in movements:
                x = offset[0]
                y = offset[1]

                if not self.get_piece_at_position(x, y):
                    self.canvas.create_rectangle(
                        x * self.cellSize,
                        y * self.cellSize,
                        x * self.cellSize + self.cellSize,
                        y * self.cellSize + self.cellSize,
                        fill="#d4e157",
                        outline="",
                    )

        # Draw all the pieces
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] is not None:
                    self.canvas.create_image(
                        x * self.cellSize + self.cellSize // 2,
                        y * self.cellSize + self.cellSize // 2,
                        image=self.grid[y][x].image(self.cellSize),
                    )

    def convert_world_to_local(self, x: int, y: int) -> tuple[int, int]:
        """
        Convert world position to local position in the grid
        """
        return x // self.cellSize, y // self.cellSize

    def is_position_in_bound(self, x: int, y: int) -> bool:
        """
        Check if the given position, is inside the grid
        """
        return self.w > x >= 0 and 0 <= y < self.h

    def get_piece_at_position(self, x: int, y: int) -> Piece | None:
        if not self.is_position_in_bound(x, y):
            return None
        return self.grid[y][x]

    def check_piece_at_position(self, x: int, y: int) -> bool:
        """
        Check if there is a piece at the given position
        """
        if not self.is_position_in_bound(x, y):
            return False
        return self.grid[y][x] is not None

    def handle_click(self, button_press: Event):
        """
        Handle click event on the board
        """
        (x, y) = self.convert_world_to_local(button_press.x, button_press.y)
        if self.check_piece_at_position(x, y):
            self.start_move(x, y)

        self.grid[y][x] = None

    def handle_hover(self, motion: Event):
        """
        Handle mouse over
        """
        (x, y) = self.convert_world_to_local(motion.x, motion.y)

        # Don't update the board if the mouse didn't move in another cell
        if x == self.last_x and y == self.last_y:
            return

        # Set last position to the new one
        self.last_x = x
        self.last_y = y

        # Check if the hovered cell contains a piece, set the hover position if it it does.
        if self.check_piece_at_position(x, y):
            self.hoverPosition = (x, y)
            self.render()
        elif self.hoverPosition:
            self.hoverPosition = None
            self.render()

    def reset_board(self):
        """
        Reset the board to the initial state
        """
        for x in range(self.w):
            self.grid[1][x] = Pawn(self, "black")
            self.grid[self.h - 2][x] = Pawn(self, "white")

            if x == 0 or x == self.w - 1:
                self.grid[0][x] = Rook(self, "black")
                self.grid[self.h - 1][x] = Rook(self, "white")

            elif x == 1 or x == self.w - 2:
                self.grid[0][x] = Knight(self, "black")
                self.grid[self.h - 1][x] = Knight(self, "white")

            elif x == 2 or x == self.w - 3:
                self.grid[0][x] = Bishop(self, "black")
                self.grid[self.h - 1][x] = Bishop(self, "white")

            elif x == 3:
                self.grid[0][x] = Queen(self, "black")
                self.grid[self.h - 1][x] = Queen(self, "white")

            elif x == 4:
                self.grid[0][x] = King(self, "black")
                self.grid[self.h - 1][x] = King(self, "white")

    def start_move(self, x: int, y: int):
        pass
