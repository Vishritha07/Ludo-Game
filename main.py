import tkinter as tk

from board import (
    draw_board,
    CELL_SIZE,
    GRID_SIZE,
    SAFE_CELLS
)
from dice import Dice


root = tk.Tk()
root.title("Ludo Game")


canvas_size = CELL_SIZE * GRID_SIZE


canvas = tk.Canvas(
    root,
    width=canvas_size,
    height=canvas_size,
    bg="white"
)

selected_token = None
players = ["red", "green", "yellow", "blue"]

current_player_index = 0

attempt_count = 0

current_dice_value = None

canvas.pack(side="left")


# Draw board
tokens = draw_board(canvas)


# Dice object
dice = Dice()


# Dice label
dice_label = tk.Label(
    root,
    text="Dice: 1",
    font=("Arial", 20)
)

dice_label.pack(pady=20)

turn_label = tk.Label(
    root,
    text="Turn: RED",
    font=("Arial", 18)
)

turn_label.pack(pady=10)


def player_has_open_token(color):

    for token in tokens:

        if (
            token.color == color
            and token.path_index != -1
            and token.finished == False
        ):

            return True

    return False


def can_move(token, dice_value):

    # Finished token cannot move
    if token.finished:

        return False

    # Token inside home
    if token.path_index == -1:

        # Can enter only on 6
        return dice_value == 6

    # Exact movement required
    next_position = token.path_index + dice_value

    # Token must reach finish exactly
    if next_position >= len(token.path):

        return False

    return True

def update_token_position(token, index, total):

    row, col = token.path[token.path_index]

    x = col * CELL_SIZE + 5
    y = row * CELL_SIZE + 5

    offsets = [
        (0, 0),
        (12, 0),
        (0, 12),
        (12, 12)
    ]

    dx, dy = offsets[index % 4]

    canvas.coords(
        token.id,
        x + dx,
        y + dy,
        x + dx + 30,
        y + dy + 30
    )

def refresh_cell_tokens(position):

    overlapping_tokens = []

    # Find all tokens in same board cell
    for token in tokens:

        if token.path_index == -1:

            continue

        token_position = token.path[token.path_index]

        if token_position == position:

            overlapping_tokens.append(token)

    # Re-arrange all overlapping tokens
    for index, token in enumerate(overlapping_tokens):

        update_token_position(
            token,
            index,
            len(overlapping_tokens)
        )


def send_token_home(token):

    token.path_index = -1

    canvas.coords(
        token.id,
        token.home_x,
        token.home_y,
        token.home_x + 30,
        token.home_y + 30
    )

def check_kill(moved_token):

    global extra_turn

    # Ignore home tokens
    if moved_token.path_index == -1:

        return

    moved_position = moved_token.path[moved_token.path_index]

    for token in tokens:

        # Don't compare with itself
        if token == moved_token:

            continue

        # Ignore same color
        if token.color == moved_token.color:

            continue

        # Ignore home tokens
        if token.path_index == -1:

            continue

        token_position = token.path[token.path_index]

        # Safe cells cannot be killed
        if moved_position in SAFE_CELLS:

             return

        # Same board cell
        if token_position == moved_position:

            print(f"{moved_token.color} killed {token.color}")

            send_token_home(token)
            
            extra_turn = True


def move_token(token, steps):

    # Token inside home
    if token.path_index == -1:

        # Enter only on 6
        if steps == 6:

            token.path_index = 0

        else:

            return

    else:

        # Normal movement
        token.path_index += steps


        # Reached exact final cell
        if token.path_index == len(token.path) - 1:
            
            token.finished = True

            print(token.color, "finished!")

            update_token_position(token, 0, 1)

            return

    position = token.path[token.path_index]

    refresh_cell_tokens(position)
    
    check_kill(token)

def select_token(event):

    global selected_token
    global current_dice_value
    global current_player_index
    global extra_turn

    clicked = canvas.find_closest(event.x, event.y)

    for token in tokens:

        if token.id == clicked[0]:

            # Wrong player click
            if token.color != players[current_player_index]:

                print("Not your turn")

                return
            
            # Finished token cannot be selected
            if token.finished:

                 print("Token already finished")

                 return
            
            selected_token = token

            print("Selected:", token.color)

            # Move only after dice roll
            if current_dice_value is not None:

                dice_value = current_dice_value

                if can_move(selected_token, current_dice_value):
              
                    
                    move_token(selected_token, current_dice_value)

                else:
                    
                    print("Invalid move")

                    current_dice_value = None

                    current_player_index += 1

                    if current_player_index >= len(players):

                        current_player_index = 0

                    turn_label.config(
                        text=f"Turn: {players[current_player_index].upper()}"
                    )

                    return
                
                current_dice_value = None


                dice_label.config(text="Dice: -")

                # Change turn only if no bonus turn
                if dice_value != 6 and extra_turn == False:
                     
                     current_player_index += 1

                     if current_player_index >= len(players):
                          current_player_index = 0
                
                
                turn_label.config(
                    text=f"Turn: {players[current_player_index].upper()}"
                )

                extra_turn = False
            return
        

canvas.bind("<Button-1>", select_token)

# Roll function
def roll_dice():

    global current_dice_value
    global current_player_index
    global attempt_count

    # Prevent rolling again before moving
    if current_dice_value is not None:

         print("Move a token first")

         return
    current_dice_value = dice.roll()

    dice_label.config(
        text=f"Dice: {current_dice_value}"
    )

    print("Rolled:", current_dice_value)
    current_color = players[current_player_index]

    # Check if player has any open token
    if not player_has_open_token(current_color):

         if current_dice_value != 6:

             attempt_count += 1

             print("Attempt:", attempt_count)

             # No move possible
             current_dice_value = None


             # 3 failed attempts
             if attempt_count >= 3:

                 print("Turn skipped")

                 attempt_count = 0

                 current_player_index += 1

                 if current_player_index >= len(players):

                     current_player_index = 0

                 turn_label.config(
                     text=f"Turn: {players[current_player_index].upper()}"
                 )

    else:

        # Reset after successful 6
        attempt_count = 0


# Roll button
roll_button = tk.Button(
    root,
    text="Roll Dice",
    font=("Arial", 16),
    command=roll_dice
)

roll_button.pack(pady=20)


root.mainloop()

