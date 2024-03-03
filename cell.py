from graphics import Point, Line

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