import random
import tkinter as tk
from tkinter import font
from include.tic_tac_toe_handler import TicTacToeHandler
from include.utils import Move


class TicTacToe(tk.Tk):
    def __init__(self, game : TicTacToeHandler):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    #Tkinter stuff
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
                    width=3,
                    height=2,
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
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
                self.computer_move()


    def computer_move(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        upper_value = (self._game.board_size * self._game.board_size) - 1
        
        while True:
            position = random.randint(0, upper_value)
            row = position // self._game.board_size
            col = position % self._game.board_size
            print("Current position is: {}, row : {} col: {}".format(position, position // self._game.board_size, position % self._game.board_size))
            move = Move(row, col, self._game.current_player.label)
            if self._game.is_valid_move(move):
                break
        
        print()

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
            msg = f'Player "{self._game.current_player.label}" won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            msg = f"{self._game.current_player.label}'s turn"
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


