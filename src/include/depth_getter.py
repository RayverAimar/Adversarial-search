import tkinter as tk
from tkinter import font

class DepthGetter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Depth Getter")
        self._cells = {}
        self._pressed : int
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()
    
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Minimax Depth: ",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()
    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text=str(((row) * 3) + (col + 1)),
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row * 3) + col
                button.bind("<ButtonPress-1>", self.pressed)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def pressed(self, event):
        
        clicked_btn = event.widget
        self._pressed = self._cells[clicked_btn] + 1
        self.after(50, lambda:self.destroy())
