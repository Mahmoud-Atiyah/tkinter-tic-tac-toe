import tkinter as tk
from tkinter import messagebox
import copy
import random

# --- AI Logic ---
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def is_draw(board):
    return all(cell in ('X', 'O') for row in board for cell in row)

def minimax(board, is_max):
    winner = check_winner(board)
    if winner == 'O': return 1
    if winner == 'X': return -1
    if is_draw(board): return 0

    if is_max:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ('X', 'O'):
                    board[i][j] = 'O'
                    score = minimax(board, False)
                    board[i][j] = 3 * i + j + 1
                    best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ('X', 'O'):
                    board[i][j] = 'X'
                    score = minimax(board, True)
                    board[i][j] = 3 * i + j + 1
                    best = min(score, best)
        return best

def best_move(board, difficulty):
    available = [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ('X', 'O')]

    if difficulty == 'easy':
        return random.choice(available) if available else None

    if difficulty == 'medium' and random.random() < 0.5:
        return random.choice(available) if available else None

    # Hard or minimax path
    best = -float('inf')
    move = None
    for i, j in available:
        board[i][j] = 'O'
        score = minimax(board, False)
        board[i][j] = 3 * i + j + 1
        if score > best:
            best = score
            move = (i, j)
    return move

# --- Game Logic ---
class TicTacToe:
    def __init__(self, root, difficulty):
        self.root = root
        self.difficulty = difficulty
        self.root.title("Tic Tac Toe - Tkinter Edition")
        self.board = [[3*i + j + 1 for j in range(3)] for i in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Helvetica', 24), width=5, height=2,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, i, j):
        if self.board[i][j] in ('X', 'O'):
            return
        self.board[i][j] = 'X'
        self.buttons[i][j].config(text='X', state='disabled')
        if self.end_game(): return

        ai_move = best_move(copy.deepcopy(self.board), self.difficulty)
        if ai_move:
            r, c = ai_move
            self.board[r][c] = 'O'
            self.buttons[r][c].config(text='O', state='disabled')
        self.end_game()

    def end_game(self):
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.reset()
            return True
        if is_draw(self.board):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset()
            return True
        return False

    def reset(self):
        self.board = [[3*i + j + 1 for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state='normal')

# --- Difficulty Selection Menu ---
def show_difficulty_menu():
    def set_difficulty(level):
        menu.destroy()
        root = tk.Tk()
        TicTacToe(root, level)
        root.mainloop()

    menu = tk.Tk()
    menu.title("Select Difficulty")

    label = tk.Label(menu, text="Choose Difficulty", font=('Helvetica', 16))
    label.pack(pady=20)

    for level in ['easy', 'medium', 'hard']:
        btn = tk.Button(menu, text=level.capitalize(), font=('Helvetica', 14),
                        width=10, command=lambda l=level: set_difficulty(l))
        btn.pack(pady=5)

    menu.mainloop()

# --- Launch Menu ---
if __name__ == '__main__':
    show_difficulty_menu()
