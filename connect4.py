import tkinter as tk
from tkinter import messagebox
import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER1_COLOR = "red"
PLAYER2_COLOR = "yellow"
EMPTY_COLOR = "white"

class Connect4:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        self.title_label = tk.Label(self.master, text="Connect 4", font=("Arial", 30))
        self.title_label.pack(pady=20)

        self.play_pvp_button = tk.Button(self.master, text="Player vs Player", font=("Arial", 20), command=self.start_pvp)
        self.play_pvp_button.pack(pady=10)

        self.play_ai_button = tk.Button(self.master, text="Player vs AI", font=("Arial", 20), command=self.start_ai)
        self.play_ai_button.pack(pady=10)

        self.how_to_play_button = tk.Button(self.master, text="How to Play", font=("Arial", 20), command=self.show_instructions)
        self.how_to_play_button.pack(pady=10)

        self.leaderboard_button = tk.Button(self.master, text="Leaderboard", font=("Arial", 20), command=self.show_leaderboard)
        self.leaderboard_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", font=("Arial", 20), command=self.master.quit)
        self.quit_button.pack(pady=10)

    def start_pvp(self):
        self.mode = "pvp"
        self.setup_game()

    def start_ai(self):
        self.mode = "ai"
        self.setup_game()

    def show_instructions(self):
        self.clear_window()
        instructions = (
            "How to Play Connect 4:\n\n"
            "1. Players take turns dropping their counters (red/yellow) into any column.\n"
            "2. The counter will fall to the lowest available slot.\n"
            "3. First to connect 4 counters horizontally, vertically, or diagonally wins!\n"
            "4. In Player vs AI mode, you play against a smart bot.\n"
            "5. Press 'Back to Menu' anytime to return."
        )
        self.instruction_label = tk.Label(self.master, text=instructions, font=("Arial", 16), justify="left")
        self.instruction_label.pack(padx=20, pady=20)
        self.back_button = tk.Button(self.master, text="Back to Menu", font=("Arial", 20), command=self.main_menu)
        self.back_button.pack(pady=20)

    def show_leaderboard(self):
        self.clear_window()
        self.leaderboard_label = tk.Label(self.master, text="Leaderboard", font=("Arial", 30))
        self.leaderboard_label.pack(pady=20)

        self.scores_text = tk.Text(self.master, width=30, height=10, font=("Arial", 16))
        self.scores_text.pack(pady=10)

        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as file:
                self.scores_text.insert(tk.END, file.read())
        else:
            self.scores_text.insert(tk.END, "No games played yet!")

        self.back_button = tk.Button(self.master, text="Back to Menu", font=("Arial", 20), command=self.main_menu)
        self.back_button.pack(pady=20)

    def setup_game(self):
        self.clear_window()
        self.board = [[EMPTY_COLOR for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = PLAYER1_COLOR
        self.buttons = []
        self.frames = []

        top_frame = tk.Frame(self.master)
        top_frame.pack()

        for col in range(COLUMNS):
            # Center-align each pointer in the grid
            btn = tk.Button(top_frame, text=f"↓", font=("Arial", 20), command=lambda c=col: self.make_move(c))
            btn.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")  # Adjusted sticky to center it properly
            self.buttons.append(btn)

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack()

        for row in range(ROWS):
            row_frames = []
            for col in range(COLUMNS):
                cell = tk.Canvas(self.canvas_frame, width=60, height=60, bg="blue", highlightthickness=0)
                cell.create_oval(5, 5, 55, 55, fill=EMPTY_COLOR)
                cell.grid(row=row, column=col, padx=2, pady=2)
                row_frames.append(cell)
            self.frames.append(row_frames)

        self.status_label = tk.Label(self.master, text="Player 1's Turn (Red)", font=("Arial", 20))
        self.status_label.pack(pady=10)

        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(pady=10)

        self.reset_button = tk.Button(bottom_frame, text="Reset Game", font=("Arial", 16), command=self.setup_game)
        self.reset_button.grid(row=0, column=0, padx=10)

        self.back_menu_button = tk.Button(bottom_frame, text="Back to Menu", font=("Arial", 16), command=self.main_menu)
        self.back_menu_button.grid(row=0, column=1, padx=10)

    def make_move(self, col):
        row = self.get_available_row(col)
        if row is not None:
            self.board[row][col] = self.current_player
            self.frames[row][col].create_oval(5, 5, 55, 55, fill=self.current_player)

            if self.check_win(self.current_player):
                self.update_leaderboard(self.current_player)
                winner = "Player 1 (Red)" if self.current_player == PLAYER1_COLOR else ("Player 2 (Yellow)" if self.mode == "pvp" else "AI (Yellow)")
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.setup_game()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.setup_game()
            else:
                self.switch_player()
                if self.mode == "ai" and self.current_player == PLAYER2_COLOR:
                    self.master.after(500, self.ai_move)

    def ai_move(self):
        # Try to win first
        for col in range(COLUMNS):
            row = self.get_available_row(col)
            if row is not None:
                temp_board = [r.copy() for r in self.board]
                temp_board[row][col] = PLAYER2_COLOR
                if self.check_win_simulation(temp_board, PLAYER2_COLOR):
                    self.make_move(col)
                    return

        # Try to block player
        for col in range(COLUMNS):
            row = self.get_available_row(col)
            if row is not None:
                temp_board = [r.copy() for r in self.board]
                temp_board[row][col] = PLAYER1_COLOR
                if self.check_win_simulation(temp_board, PLAYER1_COLOR):
                    self.make_move(col)
                    return

        # Otherwise random
        valid_cols = [c for c in range(COLUMNS) if self.get_available_row(c) is not None]
        if valid_cols:
            self.make_move(random.choice(valid_cols))

    def get_available_row(self, col):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == EMPTY_COLOR:
                return row
        return None

    def switch_player(self):
        if self.current_player == PLAYER1_COLOR:
            self.current_player = PLAYER2_COLOR
            self.status_label.config(text="Player 2's Turn (Yellow)" if self.mode == "pvp" else "AI's Turn (Yellow)")
        else:
            self.current_player = PLAYER1_COLOR
            self.status_label.config(text="Player 1's Turn (Red)")

    def check_win(self, color):
        return self.check_win_simulation(self.board, color)

    def check_win_simulation(self, board, color):
        # Horizontal
        for row in range(ROWS):
            for col in range(COLUMNS-3):
                if all(board[row][col+i] == color for i in range(4)):
                    return True
        # Vertical
        for row in range(ROWS-3):
            for col in range(COLUMNS):
                if all(board[row+i][col] == color for i in range(4)):
                    return True
        # Positive diagonal
        for row in range(ROWS-3):
            for col in range(COLUMNS-3):
                if all(board[row+i][col+i] == color for i in range(4)):
                    return True
        # Negative diagonal
        for row in range(3, ROWS):
            for col in range(COLUMNS-3):
                if all(board[row-i][col+i] == color for i in range(4)):
                    return True
        return False

    def check_draw(self):
        return all(self.board[0][col] != EMPTY_COLOR for col in range(COLUMNS))

    def update_leaderboard(self, winner_color):
        if not os.path.exists("scores.txt"):
            with open("scores.txt", "w") as f:
                f.write("Player 1 (Red): 0\nPlayer 2 (Yellow): 0\nAI (Yellow): 0\n")

        with open("scores.txt", "r") as f:
            lines = f.readlines()

        scores = {}
        for line in lines:
            if ":" in line:
                name, score = line.strip().split(":")
                scores[name] = int(score)

        if winner_color == PLAYER1_COLOR:
            scores["Player 1 (Red)"] += 1
        elif winner_color == PLAYER2_COLOR:
            if self.mode == "pvp":
                scores["Player 2 (Yellow)"] += 1
            else:
                scores["AI (Yellow)"] += 1

        with open("scores.txt", "w") as f:
            for player, score in scores.items():
                f.write(f"{player}: {score}\n")

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
