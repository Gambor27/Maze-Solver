from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__win = Tk()
        self.__win.title = 'Maze'
        self.canvas = Canvas(self.__win, width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.__win.protocol("WM_DELETE_WINDOW", self.close)


    def redraw(self):
        self.__win.update_idletasks()
        self.__win.update()

    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()
    
    def close(self):
        self.running = False

def main():
    win = Window(800, 600)
    win.wait_for_close