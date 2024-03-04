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
    def __init__(self, point1, point2, win=None):
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
        self.visited = False
        self.exit = False
    
    def _get_center(self):
        x = (self._top_left.x + self._bottom_right.x) // 2
        y = (self._top_left.y + self._bottom_right.y) // 2
        return Point(x, y)
    
    def draw(self):
        if self.left_wall:
            left_wall = Line(self._top_left, self._bottom_left)
            self._win.draw_line(left_wall, "black")
        else:
            left_wall = Line(self._top_left, self._bottom_left)
            self._win.draw_line(left_wall, "white")
        if self.right_wall:
            right_wall = Line(self._top_right, self._bottom_right)
            self._win.draw_line(right_wall, "black")
        else:
            right_wall = Line(self._top_right, self._bottom_right)
            self._win.draw_line(right_wall, "white")
        if self.top_wall:
            top_wall = Line(self._top_left, self._top_right)
            self._win.draw_line(top_wall, "black")
        else:
            top_wall = Line(self._top_left, self._top_right)
            self._win.draw_line(top_wall, "white")
        if self.bottom_wall:
            bottom_wall = Line(self._bottom_left, self._bottom_right)
            self._win.draw_line(bottom_wall, "black")
        else:
            bottom_wall = Line(self._bottom_left, self._bottom_right)
            self._win.draw_line(bottom_wall, "white")
    
    def draw_move(self, dest, undo=False):
        color = "red"
        if undo:
            color = "gray"
        path = Line(self._center, dest._center)
        self._win.draw_line(path, color)

class Maze:
    def __init__(self, point, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x = point.x
        self.y = point.y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = self._create_cells()
        self.seed = random.seed(seed)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_visited(self._cells)



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

    def _break_entrance_and_exit(self):
        self._cells[0][0].left_wall = False
        self._cells[0][0].draw()
        self._cells[self.num_cols - 1][self.num_rows - 1].right_wall = False
        self._cells[self.num_cols - 1][self.num_rows - 1].exit = True
        self._cells[self.num_cols - 1][self.num_rows - 1].draw()
    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while 1 > 0:
            cells_to_visit = []
            self.win.redraw()
            if i > 0: 
                if self._cells[i - 1][j].visited == False:
                    cells_to_visit.append('left')
            if i < self.num_cols - 1:
                if self._cells[i + 1][j].visited == False:
                    cells_to_visit.append('right')
            if j > 0:
                if self._cells[i][j - 1].visited == False:
                    cells_to_visit.append('up')
            if j < self.num_rows - 1:
                if self._cells[i][j + 1].visited == False:
                    cells_to_visit.append('down')
            if len(cells_to_visit) == 0:
                self._cells[i][j].draw()
                break
            else:
                index = random.randint(0, len(cells_to_visit) - 1)
                print(i, j, cells_to_visit[index])
                if cells_to_visit[index] == 'left':
                    self._cells[i][j].left_wall = False
                    self._cells[i - 1][j].right_wall = False
                    self._break_walls_r(i - 1, j)
                if cells_to_visit[index] == 'right':
                    self._cells[i][j].right_wall = False
                    self._cells[i + 1][j].left_wall = False
                    self._break_walls_r(i + 1, j)
                if cells_to_visit[index] == 'up':
                    self._cells[i][j].top_wall = False
                    self._cells[i][j - 1].bottom_wall = False
                    self._break_walls_r(i, j - 1)
                if cells_to_visit[index] == 'down':
                    self._cells[i][j].bottom_wall = False
                    self._cells[i][j + 1].top_wall = False
                    self._break_walls_r(i, j + 1)
    
    def _reset_visited(self, cells):
        for col in cells:
            for cell in col:
                cell.visited = False
    
    def _solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if current_cell.exit:
            return True
        if (i > 0) and (self._cells[i - 1][j].visited == False) and (current_cell.left_wall == False):
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i - 1][j], True)
        if (i < self.num_cols - 1) and (self._cells[i + 1][j].visited == False) and (current_cell.right_wall == False):            
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], True)
        if (j > 0) and (self._cells[i][j - 1].visited == False) and (current_cell.top_wall == False):
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], True)
        if (j < self.num_rows - 1) and (self._cells[i][j + 1].visited == False) and (current_cell.bottom_wall == False):
            current_cell.draw_move(self._cells[i][j + 1])
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], True)
        return False



            
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
    maze._solve()
    win.wait_for_close()

main()