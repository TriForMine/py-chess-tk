from tkinter import Event, Canvas

from piece import Pawn, Knight, Rook, Bishop, Queen, King, Piece


class Board:
    w: int
    h: int
    cellSize: int
    grid: list[list[Piece | None]]
    canvas: Canvas
    hoverPosition: tuple[int, int] | None
    currentMousePosition: tuple[int, int] | None
    draggedPiece: Piece | None
    draggedPosition: tuple[int, int] | None
    last_x: int
    last_y: int

    def __init__(self, canvas, width: int, height: int, cell_size: int):
        self.w = width
        self.h = height
        self.cellSize = cell_size
        # Generate the grid matrix to empty by default
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.canvas = canvas

        # Store the currently hovered piece
        self.hoverPosition = None

        # Store the current player
        self.player = "white"

        # Store the currently dragged piece and it's position
        self.currentMousePosition = None
        self.draggedPiece = None
        self.draggedPosition = None

        self.last_x = -1
        self.last_y = -1

        self.reset_board()

    def draw_movements(self, movements, capture_movements, color: str):
        if color == self.player:
            for pos in movements:
                (x, y) = pos

                # Draw a hollow on cell that doesn't have a piece
                if not self.check_piece_at_position(x, y):
                    self.canvas.create_rectangle(
                        x * self.cellSize + self.cellSize * 0.2,
                        y * self.cellSize + self.cellSize * 0.2,
                        x * self.cellSize + self.cellSize * 0.8,
                        y * self.cellSize + self.cellSize * 0.8,
                        fill="#d4e157",
                        outline="",
                    )

            for pos in capture_movements:
                (x, y) = pos

                # Draw a hollow on cell that doesn't have a piece
                capture_piece = self.get_piece_at_position(x, y)
                if capture_piece and capture_piece.color != color:
                    self.canvas.create_rectangle(
                        x * self.cellSize + self.cellSize * 0.2,
                        y * self.cellSize + self.cellSize * 0.2,
                        x * self.cellSize + self.cellSize * 0.8,
                        y * self.cellSize + self.cellSize * 0.8,
                        fill="#ef5350",
                        outline="",
                    )

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
            if piece:
                self.draw_movements(
                    piece.get_moves(x, y), piece.get_capture_moves(x, y), piece.color
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

        # Show the movements of the currently moved piece
        if self.draggedPiece:
            (x, y) = self.draggedPosition[0], self.draggedPosition[1]
            self.draw_movements(
                self.draggedPiece.get_moves(x, y),
                self.draggedPiece.get_capture_moves(x, y),
                self.draggedPiece.color,
            )

            self.canvas.create_image(
                self.currentMousePosition[0],
                self.currentMousePosition[1],
                image=self.draggedPiece.image(self.cellSize),
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

    def handle_drag_start(self, button_press: Event):
        """
        Handle click event on the board
        """
        (x, y) = self.convert_world_to_local(button_press.x, button_press.y)
        piece = self.get_piece_at_position(x, y)
        # If there is no piece at the clicked position, ignore the left click
        if not piece or piece.color != self.player:
            return

        self.draggedPiece = piece
        self.draggedPosition = (x, y)

        # Remove the piece from the board, so it can be drawn on the mouse position
        self.grid[y][x] = None

        # Render the board again to hide the dragged piece from the grid
        self.render()

    def handle_drag_end(self, button_press: Event):
        """
        Handle click event on the board
        """

        # Be sure that something is being dragged
        if self.draggedPiece and self.draggedPosition:
            (x, y) = self.convert_world_to_local(button_press.x, button_press.y)

            (pos_x, pos_y) = self.draggedPosition[0], self.draggedPosition[1]

            destination_piece = self.get_piece_at_position(x, y)
            # Check if the released position is a valid movement.
            if (
                (x, y) in self.draggedPiece.get_moves(pos_x, pos_y)
                and not destination_piece
            ) or (
                (x, y) in self.draggedPiece.get_capture_moves(pos_x, pos_y)
                and destination_piece.color != self.draggedPiece.color
            ):
                # Move the piece to the new position
                self.grid[y][x] = self.draggedPiece
                self.draggedPiece = None
                self.draggedPosition = None
                if self.player == "white":
                    self.player = "black"
                else:
                    self.player = "white"
            else:
                # Revert the movement
                self.grid[pos_y][pos_x] = self.draggedPiece
                self.draggedPiece = None
                self.draggedPosition = None

            self.render()

    def on_mouse_move(self, motion: Event):
        self.currentMousePosition = (motion.x, motion.y)

        if self.draggedPiece is None:
            self.handle_hover(motion)
        else:
            # If there is a dragged piece, render the moving piece.
            self.render()

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

            if x in (0, self.w - 1):
                self.grid[0][x] = Rook(self, "black")
                self.grid[self.h - 1][x] = Rook(self, "white")

            elif x in (1, self.w - 2):
                self.grid[0][x] = Knight(self, "black")
                self.grid[self.h - 1][x] = Knight(self, "white")

            elif x in (2, self.w - 3):
                self.grid[0][x] = Bishop(self, "black")
                self.grid[self.h - 1][x] = Bishop(self, "white")

            elif x == 3:
                self.grid[0][x] = Queen(self, "black")
                self.grid[self.h - 1][x] = Queen(self, "white")

            elif x == 4:
                self.grid[0][x] = King(self, "black")
                self.grid[self.h - 1][x] = King(self, "white")
