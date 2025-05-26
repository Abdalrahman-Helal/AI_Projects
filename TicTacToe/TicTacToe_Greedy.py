import tkinter as tk

# Set up the game window
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="Black")

# Set up the board and game buttons
board = [""] * 9
buttons = []

# Check for a winner
def check_winner(player):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

# Check if the board is full
def is_full():
    return all(cell != "" for cell in board)

# Greedy AI algorithm
def ai_turn():
    # 1. Check if AI can win
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner("O"):
                buttons[i].config(text="O", fg="red")
                check_game_end()
                return
            board[i] = ""

    # 2. Check if player can win in the next move and block them
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner("X"):
                board[i] = "O"
                buttons[i].config(text="O", fg="red")
                check_game_end()
                return
            board[i] = ""

    # 3. If no winning or blocking move, AI picks the first empty square
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            buttons[i].config(text="O", fg="red")
            check_game_end()
            return

# When the player clicks a button
def player_turn(i):
    if board[i] == "" and not check_winner("X") and not check_winner("O"):
        board[i] = "X"
        buttons[i].config(text="X", fg="blue")
        check_game_end()
        if not is_full() and not check_winner("X"):
            root.after(0, ai_turn)  

# Check if the game has ended
def check_game_end():
    if check_winner("X"):
        label.config(text="You Win! ")
        disable_buttons()
        root.after(2000, restart_game)  
    elif check_winner("O"):
        label.config(text="AI Wins! ")
        disable_buttons()
        root.after(2000, restart_game)  
    elif is_full():
        label.config(text="Draw! ")
        disable_buttons()
        root.after(2000, restart_game)  # Restart the game after 2 seconds

# Disable buttons after the game ends
def disable_buttons():
    for btn in buttons:
        btn.config(state="disabled")

# Restart the game
def restart_game():
    global board
    board = [""] * 9 
    for btn in buttons:
        btn.config(text="", state="normal") 
    label.config(text="Your Turn (X)")  

# Draw the buttons on the screen
frame = tk.Frame(root, bg="Black")
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 32), width=5, height=2,
                    bg="white", command=lambda i=i: player_turn(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Label to display the result
label = tk.Label(root, text="Your Turn (X)", font=("Arial", 20), bg="yellow")
label.pack(pady=10)

# Start the game
root.mainloop()
