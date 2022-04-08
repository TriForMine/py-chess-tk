from time import time
from tkinter import Event, Canvas, messagebox
from collections import defaultdict
from bot import Bot
from piece import Pawn, Knight, Rook, Bishop, Queen, King, Piece
from utils import enemy_color


class Board:
    w: int
    h: int
    cellSize: int
    grid: defaultdict[tuple[int, int], None | Piece]
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
        # Generate the grid using a defaultdict structure, which is a dict, that default non-existing value to None.
        self.grid = defaultdict(lambda: None)
        self.canvas = canvas

        # Store the currently hovered piece
        self.hoverPosition = None

        # Store the current player
        self.player = "white"

        # Store an instance of the bot class
        # If you make the bot using more than 3 in depth, it will start to be slow!

        # Choose between 1-5
        self.bot = Bot(self, 3)

        # Store the choice of user, playing against a bot or another player
        self.playWithBot = True

        # Store the currently dragged piece and it's position
        self.currentMousePosition = None
        self.draggedPiece = None
        self.draggedPosition = None

        self.last_x = -1
        self.last_y = -1

        self.reset_board()

    def clone_grid(self, grid=None) -> defaultdict[tuple[int, int], None | Piece]:
        """
        Clone a grid into a new one
        """
        if not grid:
            grid = self.grid
        new_grid = defaultdict(lambda: None)

        for (pos, val) in grid.items():
            if val:
                new_grid[pos] = val.clone()
        return new_grid

    def get_color_all_moves(
        self, color: str, grid=None
    ) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        if grid is None:
            grid = self.grid

        # Use set since you don't want to check multiple moves more than once.
        res = set()

        for (x, y), piece in grid.copy().items():
            if piece and piece.color == color:
                capture_moves = piece.get_capture_moves(self, grid, x, y)
                moves = piece.get_moves(self, grid, x, y)

                for pos in capture_moves:
                    (pos_x, pos_y) = pos
                    target = self.get_piece_at_position(pos_x, pos_y, grid)
                    if target and target.color != piece.color:
                        res.add(((x, y), pos))

                for pos in moves:
                    (pos_x, pos_y) = pos
                    if self.is_position_in_bound(
                        pos_x, pos_y
                    ) and not self.check_piece_at_position(pos_x, pos_y, grid):
                        res.add(((x, y), pos))

        return res

    def is_capture_move(self, move, grid):
        if not grid:
            grid = self.grid

        (_, e) = move
        return type(self.get_piece_at_position(e[0], e[1], grid)) is King

    def filter_illegal_moves(
        self, moves: set[tuple[tuple[int, int], tuple[int, int]]], color: str
    ):
        """
        Remove all illegal moves from the given moves.
        """
        is_under_check = self.is_color_in_check(color)

        if not is_under_check:
            return moves
        else:
            new = set()
            for (p1, p2) in moves:
                tmp = self.clone_grid()
                tmp[p2] = tmp[p1]
                tmp.pop(p1)
                if not self.is_color_in_check(color, tmp):
                    new.add((p1, p2))

            return new

    def get_king_piece(self, color: str, grid=None):
        """
        Return the king piece of the given color
        """
        if not grid:
            grid = self.grid

        # Check if the king is not actually dragged.
        if type(self.draggedPiece) is King:
            (x, y) = self.convert_world_to_local(
                self.hoverPosition[0], self.hoverPosition[1]
            )
            return (x, y), self.draggedPiece

        # Search for the king over the whole grid.
        for ((x, y), piece) in grid.items():
            if piece and piece.color == color and type(piece) is King:
                return (x, y), piece

        self.render()
        messagebox.showerror(
            "Warning",
            f"The {color} king was captured.\n{enemy_color(color)} won.\n\nThe game has been reset.",
        )
        self.reset_board()

    def is_color_in_check(self, color: str, grid=None):
        """
        Check if the provided color is in check state.
        """
        if not grid:
            grid = self.grid

        moves = self.get_color_all_moves(enemy_color(color), grid)

        # And check if the king position is included in the movements of the enemy.
        for move in moves:
            if self.is_capture_move(move, grid):
                return True

        return False

    def emulate_check(self, p1: tuple[int, int], p2: tuple[int, int], player: str):
        """
        Simulate a movement, and verify if it provokes a check for the player.
        """
        tmp = self.clone_grid()
        if tmp[p1]:
            tmp[p2] = tmp[p1]
            tmp.pop(p1)
            return self.is_color_in_check(player, tmp)
        elif self.draggedPiece:
            tmp[p2] = self.draggedPiece.clone()
            tmp.pop(p1)
            return self.is_color_in_check(player, tmp)
        else:
            return False

    def verify_counter_check(self, color: str):
        # Test all the possible movements, to verify if the check goes away
        return any(
            not self.emulate_check(p1, p2, color)
            for p1, p2 in self.filter_illegal_moves(
                self.get_color_all_moves(color), color
            )
        )

    def verify_for_checkmate(self):
        # If the white player is in check, verify if the player has a way to avoid the check.
        # If it's the black player turn, the white player has lost.
        if self.player == "white" and self.is_color_in_check("white"):
            if self.verify_counter_check("white"):
                return False
            else:
                return "white"

        # If the black player is in check, verify if the player has a way to avoid the check.
        # If it's the white player turn, the black player has lost.
        if self.player == "black" and self.is_color_in_check("black"):
            if self.verify_counter_check("black"):
                return False
            else:
                return "black"

        return None

    def draw_movements(self, movements, capture_movements, color: str):
        """
        Draw all the movement on the board.
        """
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
                    fill = "#B88B4A"
                else:
                    fill = "#E3C16F"

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
                    piece.get_moves(self, self.grid, x, y),
                    piece.get_capture_moves(self, self.grid, x, y),
                    piece.color,
                )

        # Draw all the pieces
        for ((x, y), piece) in self.grid.items():
            if self.grid[x, y] is not None:
                self.canvas.create_image(
                    x * self.cellSize + self.cellSize // 2,
                    y * self.cellSize + self.cellSize // 2,
                    image=self.grid[x, y].image(self.cellSize),
                )

        # Show the movements of the currently moved piece
        if self.draggedPiece:
            (x, y) = self.draggedPosition[0], self.draggedPosition[1]
            self.draw_movements(
                self.draggedPiece.get_moves(self, self.grid, x, y),
                self.draggedPiece.get_capture_moves(self, self.grid, x, y),
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

    def get_piece_at_position(self, x: int, y: int, grid=None) -> Piece | None:
        """
        Return the piece at the provided position.
        """
        if grid is None:
            grid = self.grid
        if not self.is_position_in_bound(x, y):
            return None
        return grid[x, y]

    def check_piece_at_position(self, x: int, y: int, grid=None) -> bool:
        """
        Check if there is a piece at the given position
        """
        if grid is None:
            grid = self.grid
        if not self.is_position_in_bound(x, y):
            return False
        return grid[x, y] is not None

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
        self.grid.pop((x, y))

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
                (x, y) in self.draggedPiece.get_moves(self, self.grid, pos_x, pos_y)
                and not destination_piece
            ) or (
                (x, y)
                in self.draggedPiece.get_capture_moves(self, self.grid, pos_x, pos_y)
                and destination_piece
                and destination_piece.color != self.draggedPiece.color
            ):
                if not self.emulate_check((pos_x, pos_y), (x, y), self.player):
                    # Move the piece to the new position
                    self.grid[x, y] = self.draggedPiece.clone()
                    self.draggedPiece = None
                    self.draggedPosition = None
                    if self.player == "white":
                        self.player = "black"
                    else:
                        self.player = "white"

                    # After a movement has been made, check if any of the king are under check/checkmate
                    loser = self.verify_for_checkmate()

                    if not loser and self.player == "black" and self.playWithBot:
                        start = time()
                        bot_move = self.bot.play("black", self.grid)
                        print(f"Bot took {time() - start} seconds to play")

                        if bot_move:
                            (s, e) = bot_move

                            self.grid[e] = self.grid[s].clone()
                            self.grid.pop(s)
                            self.player = "white"

                            # After a movement has been made, check if any of the king are under check/checkmate
                            loser = self.verify_for_checkmate()

                            if loser:
                                self.render()
                                # Update the board instantly, as the game ends
                                self.canvas.winfo_toplevel().update()
                        else:
                            loser = "black"

                    if loser:
                        messagebox.showinfo(
                            "Game Ended",
                            f"{enemy_color(loser)} won!\n{loser} has a checkmate!",
                        )
                        self.reset_board()
                        return
                else:
                    self.grid[pos_x, pos_y] = self.draggedPiece.clone()
                    self.draggedPiece = None
                    self.draggedPosition = None

                    self.render()
                    self.canvas.winfo_toplevel().update()

                    messagebox.showerror(
                        "Illegal Move",
                        "You're king is in check!",
                    )
            else:
                # Revert the movement
                self.grid[pos_x, pos_y] = self.draggedPiece.clone()
                self.draggedPiece = None
                self.draggedPosition = None

            self.render()

    def on_mouse_move(self, motion: Event):
        self.currentMousePosition = (motion.x, motion.y)

        if self.draggedPiece is None:
            # Show the movements on the hovered piece, if no piece is being dragged.
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

        # Reset all the variables to default

        self.grid.clear()
        self.hoverPosition = None

        self.currentMousePosition = None
        self.draggedPiece = None
        self.draggedPosition = None

        self.last_x = -1
        self.last_y = -1

        self.player = "white"

        # Reset the position of all the pieces

        for x in range(self.w):
            self.grid[x, 1] = Pawn("black")
            self.grid[x, self.h - 2] = Pawn("white")

            if x in (0, self.w - 1):
                self.grid[x, 0] = Rook("black")
                self.grid[x, self.h - 1] = Rook("white")

            elif x in (1, self.w - 2):
                self.grid[x, 0] = Knight("black")
                self.grid[x, self.h - 1] = Knight("white")

            elif x in (2, self.w - 3):
                self.grid[x, 0] = Bishop("black")
                self.grid[x, self.h - 1] = Bishop("white")

            elif x == 3:
                self.grid[x, 0] = Queen("black")
                self.grid[x, self.h - 1] = Queen("white")

            elif x == 4:
                self.grid[x, 0] = King("black")
                self.grid[x, self.h - 1] = King("white")

        self.render()
