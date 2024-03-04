from tkinter import Tk, BOTH, Canvas
import time, random

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

class Maze:
    def __init__(self, point, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x = point.x
        self.y = point.y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = self._create_cells()

    def _create_cells(self):
        list_of_cells = []
        current_x = self.x
        for i in range(self.num_cols):
            current_y = self.y
            current_col = []
            for j in range(self.num_rows):
                top_left = Point(current_x, current_y)
                bottom_right = Point((current_x + self.cell_size_x), (current_y + self.cell_size_y))
                current_cell = Cell(top_left, bottom_right, self.win)
                current_col.append(current_cell)
                current_y += self.cell_size_y
            current_x += self.cell_size_x
            list_of_cells.append(current_col)
        self._draw_cells(list_of_cells)
        return list_of_cells
    
    def _draw_cells(self, cells):
        for col in cells:
            for cell in col:
                cell.draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(.05)


    
def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    origin = Point(margin, margin)
    maze = Maze(origin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    win.wait_for_close()

main()