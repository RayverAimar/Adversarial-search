import tkinter as tk
from tkinter import font
from include.minimax_tree import MinimaxTree
from include.tic_tac_toe_handler import TicTacToeHandler
from include.utils import Move


class TicTacToe(tk.Tk):
    def __init__(self, game : TicTacToeHandler, _computer_first = False):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._computer_first = _computer_first
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()
        if self._computer_first:
            self.computer_move()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=2,
                    height=1,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Human won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"Computer's turn"
                self._update_display(msg)
                self.computer_move()
    
    def computer_move(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()

        current_board = [["" for j in range(self._game.board_size)] for i in range(self._game.board_size)]
        
        for i in self._game._current_moves:
            for moves in i:
                current_board[moves.row][moves.col] = moves.label

        minimax = MinimaxTree(current_board, self._game.current_player.label, self._game._max_depth)

        row , col = minimax.root.children[minimax.root.idx_best_child].move_to_get_here
        move = Move(row, col, self._game.current_player.label)
        computer_button : tk.Button

        for key in self._cells.keys():
            values = self._cells[key]
            if(values[0] == row and values[1] == col):
                computer_button = key

        computer_button.invoke()
        self._update_button(computer_button)
        self._game.process_move(move)

        if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
        elif self._game.has_winner():
            self._highlight_cells()
            msg = f'Computer won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            msg = f"Human's turn"
            self._update_display(msg)


    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        self._game.reset_game()
        print("----------------------------------------")
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
        if self._computer_first:
            self.computer_move()