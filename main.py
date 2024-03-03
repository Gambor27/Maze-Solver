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

class Cell:
    def __init__(self, point1, point2, win):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self._top_left = point1
        self._top_right = Point(point2.x, point1.y)
        self._bottom_left = Point(point1.x, point2.y)
        self._bottom_right = point2
        self._center = self._get_center()
        self._win = win
    
    def _get_center(self):
        x = (self._top_left.x + self._bottom_right.x) // 2
        y = (self._top_left.y + self._bottom_right.y) // 2
        return Point(x, y)
    
    def draw(self):
        if self.left_wall:
            left_wall = Line(self._top_left, self._bottom_left)
            self._win.draw_line(left_wall, "black")
        if self.right_wall:
            right_wall = Line(self._top_right, self._bottom_right)
            self._win.draw_line(right_wall, "black")
        if self.top_wall:
            top_wall = Line(self._top_left, self._top_right)
            self._win.draw_line(top_wall, "black")
        if self.bottom_wall:
            bottom_wall = Line(self._bottom_left, self._bottom_right)
            self._win.draw_line(bottom_wall, "black")
    
    def draw_move(self, dest, undo=False):
        color = "red"
        if undo:
            color = "gray"
        path = Line(self._center, dest._center)
        self._win.draw_line(path, color)

def main():
    win = Window(800, 600)
    point1 = Point(100, 100)
    point2 = Point(250, 200)
    point3 = Point(250, 100)
    point4 = Point(400, 200)
    cell1 = Cell(point1, point2, win)
    cell2 = Cell(point3, point4, win)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    #cell2.draw_move(cell1, undo=True)
    win.wait_for_close()

main()