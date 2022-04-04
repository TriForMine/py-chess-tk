from tkinter import Tk


class MainGUI:
    def __init__(self, root):
        self.root = root
        root.title("Chess Game")


root = Tk()
gui = MainGUI(root)

root.mainloop()
