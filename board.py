from tkinter import Canvas

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

        self.last_x = -1
        self.last_y = -1

        for y in range(height):
            line = []
            for x in range(width):
                line.append(None)
            self.grid.append(line)

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

    def convert_world_to_local(self, x, y):
        """
        Convert world position to local position in the grid
        :param x: int
        :param y: int
        :return: int
        """
        return x // self.cellSize, y // self.cellSize

    def get_piece_at_position(self, x, y):
        return self.grid[y][x]

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
        self.last_x = x
        self.last_y = y

        # Don't update the board if the mouse didn't move in another cell
        if x == self.last_x and y == self.last_y:
            return

        piece = self.get_piece_at_position(x, y)

        if piece:
            self.render()

