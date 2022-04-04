from tkinter import Tk, Frame, Canvas, BOTH

from board import Board

WIDTH = 800
HEIGHT = WIDTH


class MainGUI(Frame):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()
        self.board = Board(self.canvas, 8, 8, WIDTH // 8)
        self.initUI()

    def initUI(self):
        self.master.title("Chess Game")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.master.resizable(0, 0)

        self.master.bind("<Button-1>", self.on_click)
        self.master.bind('<Motion>', self.on_mouse_move)

        self.pack(fill=BOTH, expand=1)
        self.board.render()

        self.canvas.pack(fill=BOTH, expand=1)

    def on_click(self, click_event):
        """

        :type click_event: ClickEvent
        """
        self.board.handle_click(click_event)

    def on_mouse_move(self, motion):
        self.board.handle_hover(motion)



root = Tk()
gui = MainGUI()

root.mainloop()
