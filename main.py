from tkinter import Tk, Frame, Canvas, BOTH, Event

from board import Board

WIDTH = 800
HEIGHT = WIDTH


class MainGUI(Frame):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()
        self.board = Board(self.canvas, 8, 8, WIDTH // 8)
        self.init_ui()

    def init_ui(self):
        self.winfo_toplevel().title("Chess Game")
        self.winfo_toplevel().geometry(f"{WIDTH}x{HEIGHT}")
        # Make the window not resizable
        self.winfo_toplevel().resizable(False, False)

        # Detect left click
        self.master.bind("<Button-1>", self.on_click)
        # Detect mouse movement
        self.master.bind("<Motion>", self.on_mouse_move)

        # Render the board
        self.board.render()

        self.canvas.pack(fill=BOTH, expand=1)

    def on_click(self, click_event: Event):
        self.board.handle_click(click_event)

    def on_mouse_move(self, motion: Event):
        self.board.handle_hover(motion)


root = Tk()
gui = MainGUI()

root.mainloop()
