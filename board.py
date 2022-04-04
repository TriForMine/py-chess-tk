from piece import Pawn, Knight, Rook, Bishop, Queen, King


class Board:
    def __init__(self, canvas, width, height, cell_size):
        """
        :type width: int
        :type height: int
        :type cell_size: int
        """
        self.w = width
        self.h = height
        self.cellSize = cell_size
        self.grid = []
        self.canvas = canvas
        self.hoverPosition = None

        self.last_x = -1
        self.last_y = -1

        for y in range(height):
            line = []
            for x in range(width):
                line.append(None)
            self.grid.append(line)

        self.reset_board()

    def render(self):
        """
        Render the board by drawing square
        """
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
                    outline=""
                )

        if self.hoverPosition:
            piece = self.get_piece_at_position(self.hoverPosition[0], self.hoverPosition[1])
            movements = piece.possible_moves()

            for offset in movements:
                x = self.hoverPosition[0] + offset[0]
                y = self.hoverPosition[1] + offset[1]

                if not self.get_piece_at_position(x, y):
                    self.canvas.create_rectangle(
                        x * self.cellSize,
                        y * self.cellSize,
                        x * self.cellSize + self.cellSize,
                        y * self.cellSize + self.cellSize,
                        fill="#d4e157",
                        outline=""
                    )

        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] is not None:
                    self.canvas.create_image(
                        x * self.cellSize + self.cellSize // 2,
                        y * self.cellSize + self.cellSize // 2,
                        image=self.grid[y][x].image(self.cellSize)
                    )

    def convert_world_to_local(self, x, y):
        """
        Convert world position to local position in the grid
        :param x: int
        :param y: int
        :return: int
        """
        return x // self.cellSize, y // self.cellSize

    def is_position_in_bound(self, x, y):
        return self.w > x >= 0 and 0 <= y < self.h

    def can_piece_move(self, x, y, movements):
        for offset in movements:
            if self.check_piece_at_position(x + offset[0], y + offset[1]):
                return False
        return True

    def get_piece_at_position(self, x, y):
        if not self.is_position_in_bound(x, y):
            return None
        return self.grid[y][x]

    def check_piece_at_position(self, x, y):
        if not self.is_position_in_bound(x, y):
            return None
        return self.grid[y][x] is not None

    def handle_click(self, button_press):
        """
        Handle click event on the board
        :type button_press: ButtonPress
        """
        (x, y) = self.convert_world_to_local(button_press.x, button_press.y)
        piece = self.get_piece_at_position(x, y)

        print(piece)

    def handle_hover(self, motion):
        (x, y) = self.convert_world_to_local(motion.x, motion.y)

        # Don't update the board if the mouse didn't move in another cell
        if x == self.last_x and y == self.last_y:
            self.hoverPosition = None
            return

        self.last_x = x
        self.last_y = y

        piece = self.get_piece_at_position(x, y)

        if piece:
            self.hoverPosition = (x, y)
            self.render()

    def reset_board(self):
        for x in range(self.w):
            self.grid[1][x] = Pawn('black')
            self.grid[self.h - 2][x] = Pawn('white')

            if x == 0 or x == self.w - 1:
                self.grid[0][x] = Rook('black')
                self.grid[self.h - 1][x] = Rook('white')

            elif x == 1 or x == self.w - 2:
                self.grid[0][x] = Knight('black')
                self.grid[self.h - 1][x] = Knight('white')

            elif x == 2 or x == self.w - 3:
                self.grid[0][x] = Bishop('black')
                self.grid[self.h - 1][x] = Bishop('white')

            elif x == 3:
                self.grid[0][x] = Queen('black')
                self.grid[self.h - 1][x] = Queen('white')

            elif x == 4:
                self.grid[0][x] = King('black')
                self.grid[self.h - 1][x] = King('white')
