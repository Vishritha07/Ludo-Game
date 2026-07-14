class Token:

    def __init__(self, canvas, x, y, color,path, home_x, home_y):

        self.canvas = canvas
        self.color = color
        self.path = path
        self.home_x = home_x
        self.home_y = home_y

        self.path_index = -1

        self.finished = False
        self.has_entered = False

        self.id = canvas.create_oval(
            x,
            y,
            x + 30,
            y + 30,
            fill=color,
            outline="black",
            width=2
        )