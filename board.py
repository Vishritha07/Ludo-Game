from token import Token
tokens = []
CELL_SIZE = 40
GRID_SIZE = 15

RED_PATH = [

    # RED SIDE
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),

    (5, 6),
    (4, 6),
    (3, 6),
    (2, 6),
    (1, 6),
    (0, 6),

    (0, 7),
    (0, 8),

    (1, 8),
    (2, 8),
    (3, 8),
    (4, 8),
    (5, 8),

    # GREEN SIDE
    (6, 9),
    (6, 10),
    (6, 11),
    (6, 12),
    (6, 13),
    (6, 14),

    (7, 14),

    (8, 14),

    (8, 13),
    (8, 12),
    (8, 11),
    (8, 10),
    (8, 9),

    # YELLOW SIDE
    (9, 8),
    (10, 8),
    (11, 8),
    (12, 8),
    (13, 8),
    (14, 8),

    (14, 7),
    (14, 6),

    (13, 6),
    (12, 6),
    (11, 6),
    (10, 6),
    (9, 6),

    # BLUE SIDE
    (8, 5),
    (8, 4),
    (8, 3),
    (8, 2),
    (8, 1),
    (8, 0),

    (7, 0),

    (6, 0),

    # connect back to start smoothly
    (6, 1)
]

GREEN_PATH = RED_PATH[13:] + RED_PATH[:13]

YELLOW_PATH = RED_PATH[26:] + RED_PATH[:26]

BLUE_PATH = RED_PATH[39:] + RED_PATH[:39]

SAFE_CELLS = [

    # Starting safe cells
    RED_PATH[0],
    GREEN_PATH[0],
    YELLOW_PATH[0],
    BLUE_PATH[0],

    # Star safe cells
    RED_PATH[8],
    GREEN_PATH[8],
    YELLOW_PATH[8],
    BLUE_PATH[8]
]

def draw_safe_cells(canvas):

    for row, col in SAFE_CELLS:

        x = col * CELL_SIZE + 20
        y = row * CELL_SIZE + 20

        canvas.create_text(
            x,
            y,
            text="★",
            font=("Arial", 18, "bold"),
            fill="black"
        )

def draw_cell(canvas, row, col, color):

    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE

    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE

    canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=color,
        outline="black"
    )
def draw_home(canvas, start_row, start_col):

    # Draw white inner area
    for row in range(start_row, start_row + 4):

        for col in range(start_col, start_col + 4):

            draw_cell(canvas, row, col, "white")


    # Token circles positions
    positions = [

        (start_row + 1, start_col + 1),
        (start_row + 1, start_col + 2),

        (start_row + 2, start_col + 1),
        (start_row + 2, start_col + 2)
    ]


    # Draw circles
    for row, col in positions:

        x1 = col * CELL_SIZE + 5
        y1 = row * CELL_SIZE + 5

        x2 = x1 + 30
        y2 = y1 + 30

    canvas.create_oval(
        x1,
        y1,
        x2,
        y2,
        fill="white",
        outline="black",
        width=2
    )   

def get_token_position(row, col):

    x = col * CELL_SIZE + 5
    y = row * CELL_SIZE + 5

    return x, y

def draw_board(canvas):

    # Draw white grid first
    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            draw_cell(canvas, row, col, "white")


    # RED HOME
    for row in range(6):
        for col in range(6):

            draw_cell(canvas, row, col, "red")
    

    # GREEN HOME
    for row in range(6):
        for col in range(9, 15):

            draw_cell(canvas, row, col, "green")


    # BLUE HOME
    for row in range(9, 15):
        for col in range(0, 6):

            draw_cell(canvas, row, col, "blue")


    # YELLOW HOME
    for row in range(9, 15):
        for col in range(9, 15):

            draw_cell(canvas, row, col, "yellow")


    # Vertical path
    for row in range(15):
        for col in range(6, 9):

            draw_cell(canvas, row, col, "white")


    # Horizontal path
    for row in range(6, 9):
        for col in range(15):

            draw_cell(canvas, row, col, "white")

    # GREEN final lane (top → downward)
    for row in range(1, 6):

        draw_cell(canvas, row, 7, "green")


    # RED final lane (left → right)
    for col in range(1, 6):

        draw_cell(canvas, 7, col, "red")


    # YELLOW final lane (right → left)
    for col in range(9, 14):

        draw_cell(canvas, 7, col, "yellow")


    # BLUE final lane (bottom → upward)
    for row in range(9, 14):

        draw_cell(canvas, row, 7, "blue")
        # Center win area

    # TOP
    draw_cell(canvas, 6, 7, "green")

    # LEFT
    draw_cell(canvas, 7, 6, "red")

    # RIGHT
    draw_cell(canvas, 7, 8, "yellow")

    # BOTTOM
    draw_cell(canvas, 8, 7, "blue")

    # Draw safe cell stars
    draw_safe_cells(canvas)

    # Center cell
    draw_cell(canvas, 7, 7, "black")
    # Home areas

    # RED
    draw_home(canvas, 1, 1)

    # GREEN
    draw_home(canvas, 1, 10)

    # BLUE
    draw_home(canvas, 10, 1)

    # YELLOW
    draw_home(canvas, 10, 10)


        # RED TOKENS
    red_positions = [

        (1, 1),
        (1, 3),

        (3, 1),
        (3, 3)
    ]

    for row, col in red_positions:

        x, y = get_token_position(row, col)

        tokens.append(
            Token(
                 canvas,
                 x,
                 y,
                 "red",
                 RED_PATH,
                 x,
                 y
            )
        )
    # GREEN TOKENS
    green_positions = [

        (1, 10),
        (1, 12),

        (3, 10),
        (3, 12)
    ]

    for row, col in green_positions:

        x, y = get_token_position(row, col)

        tokens.append(
            Token(
                canvas,
                x,
                y,
                "green",
                GREEN_PATH,
                x,
                y
            )
        )


    # BLUE TOKENS
    blue_positions = [

        (10, 1),
        (10, 3),

        (12, 1),
        (12, 3)
    ]

    for row, col in blue_positions:

        x, y = get_token_position(row, col)

        tokens.append(
            Token(
                canvas,
                x,
                y,
                "blue",
                BLUE_PATH,
                x,
                y
            )
        )


    # YELLOW TOKENS
    yellow_positions = [

        (10, 10),
        (10, 12),

        (12, 10),
        (12, 12)
    ]

    for row, col in yellow_positions:

        x, y = get_token_position(row, col)

        tokens.append(
            Token(
                canvas,
                x,
                y,
                "yellow",
                YELLOW_PATH,
                x,
                y
            )
        )

    return tokens