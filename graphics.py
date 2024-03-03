from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self._win = Tk()
        self._win.title('Maze')
        self.canvas = Canvas(self._win, bg="white", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self._win.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._win.update_idletasks()
        self._win.update()

    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, color):
        line.draw(self.canvas, color)
    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.x1 = point1.x
        self.x2 = point2.x
        self.y1 = point1.y
        self.y2 = point2.y

    
    def draw(self, canvas, color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)