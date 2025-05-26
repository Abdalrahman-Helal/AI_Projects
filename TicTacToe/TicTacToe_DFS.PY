import tkinter as tk

# Set up the game window
root = tk.Tk()
root.title("Tic Tac Toe - DFS Algorithm")
root.configure(bg="black")

# Game board
board = [""] * 9
buttons = []

# Winning combinations
WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  
    (0, 3, 6), (1, 4, 7), (2, 5, 8), 
    (0, 4, 8), (2, 4, 6)              
]

def check_winner(player):
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def is_full():
    return all(cell != "" for cell in board)

def dfs_ai():
    best_score = -float('inf')
    best_move = None
    
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = dfs(board, False, 0)
            board[i] = ""
            
            if score > best_score:
                best_score = score
                best_move = i
    
    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(text="O", fg="red")
        check_game_end()

def dfs(board, is_maximizing, depth):
    # Base cases
    if check_winner("O"):
        return 10 - depth
    if check_winner("X"):
        return depth - 10
    if is_full():
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = dfs(board, False, depth + 1)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = dfs(board, True, depth + 1)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def player_turn(i):
    if board[i] == "" and not check_winner("X") and not check_winner("O"):
        board[i] = "X"
        buttons[i].config(text="X", fg="blue")
        check_game_end()
        if not is_full() and not check_winner("X"):
            root.after(100, dfs_ai)  

def check_game_end():
    if check_winner("X"):
        label.config(text="You Win!", fg="green")
        disable_buttons()
    elif check_winner("O"):
        label.config(text="AI Wins!", fg="red")
        disable_buttons()
    elif is_full():
        label.config(text="Draw!", fg="orange")
        disable_buttons()

def disable_buttons():
    for btn in buttons:
        btn.config(state="disabled")

def restart_game():
    global board
    board = [""] * 9
    for btn in buttons:
        btn.config(text="", state="normal")
    label.config(text="Your Turn (X)", fg="black")

# Create UI
frame = tk.Frame(root, bg="black")
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 32), width=5, height=2,
                    bg="white", command=lambda i=i: player_turn(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

label = tk.Label(root, text="Your Turn (X)", font=("Arial", 20), bg="yellow")
label.pack(pady=10)

restart_btn = tk.Button(root, text="Restart Game", font=("Arial", 14),
                        command=restart_game, bg="lightgray")
restart_btn.pack(pady=10)

root.mainloop()