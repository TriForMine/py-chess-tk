from tkinter import Tk, Frame, Canvas, BOTH, Event, messagebox, Menu
from board import Board
from consts import WIDTH, HEIGHT


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

        # Create a menu
        menubar = Menu(root)
        settings_menu = Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Restart", command=self.restart_dialog)
        settings_menu.add_command(label="Enable Bot", command=self.bot_dialog)

        levels = Menu(menubar, tearoff=0)
        levels.add_command(
            label="Level 2 (0.01s)", command=lambda: self.select_bot_difficulty(2)
        )
        levels.add_command(
            label="Level 3 (0.1s)", command=lambda: self.select_bot_difficulty(3)
        )
        levels.add_command(
            label="Level 4 (1s)", command=lambda: self.select_bot_difficulty(4)
        )
        levels.add_command(
            label="Level 5 (60s)", command=lambda: self.select_bot_difficulty(5)
        )
        settings_menu.add_cascade(label="Bot Difficulty", menu=levels)

        settings_menu.add_separator()
        settings_menu.add_command(label="Exit", command=self.winfo_toplevel().quit)

        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", command=self.open_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.winfo_toplevel().config(menu=menubar)

        # Detect left mouse button down
        self.master.bind("<ButtonPress-1>", self.on_mouse_down)
        # Detect left mouse button up
        self.master.bind("<ButtonRelease-1>", self.on_mouse_up)
        # Detect mouse movement
        self.master.bind("<Motion>", self.on_mouse_move)

        # Render the board
        self.board.render()

        self.canvas.pack(fill=BOTH, expand=1)

    def restart_dialog(self):
        if messagebox.askokcancel(
            "Confirmation", "Are you sure that you want to restart the game?"
        ):
            self.board.reset_board()

    def bot_dialog(self):
        self.board.playWithBot = messagebox.askyesno(
            "Game Mode", "Do you want to play with a bot?"
        )

    def open_about(self):
        self.board.playWithBot = messagebox.showinfo(
            "Info",
            "Made by TriForMine\nhttps://www.triformine.dev/\n"
            "\nPowered by Python and Tkinter\n\nSource Code "
            "available "
            "at:\nhttps://github.com/TriForMine/py-chess-tk\nUnder "
            "Apache-2.0 License",
        )

    def select_bot_difficulty(self, difficulty: int):
        self.board.bot.depth = difficulty

    def on_mouse_down(self, click_event: Event):
        self.board.handle_drag_start(click_event)

    def on_mouse_up(self, click_event: Event):
        self.board.handle_drag_end(click_event)

    def on_mouse_move(self, motion: Event):
        self.board.on_mouse_move(motion)


root = Tk()
gui = MainGUI()

root.mainloop()
