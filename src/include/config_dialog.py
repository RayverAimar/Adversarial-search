"""Single-window configuration dialog. Result is in ``self.result`` after mainloop."""

import tkinter as tk

from include import theme


class ConfigDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe — Configuration")
        self.configure(bg=theme.BG)
        theme.center(self, 480, 600)

        self.result: dict | None = None

        self._build_header()
        self.size_var = tk.IntVar(value=3)
        self._build_choice_section(
            "Board size",
            [("3 × 3", 3), ("4 × 4", 4), ("5 × 5", 5)],
            self.size_var,
        )
        self.first_var = tk.StringVar(value="human")
        self._build_choice_section(
            "Who plays first?",
            [("You (X)", "human"), ("AI (X)", "ai")],
            self.first_var,
        )
        self.depth_var = tk.IntVar(value=4)
        self._build_depth_section()
        self.show_tree_var = tk.BooleanVar(value=False)
        self._build_options_section()
        self._build_start_button()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=theme.BG)
        header.pack(fill="x", pady=(28, 6))
        tk.Label(
            header, text="Tic-Tac-Toe", font=theme.FONT_TITLE, bg=theme.BG, fg=theme.TEXT
        ).pack()
        tk.Label(
            header,
            text="Configure your game",
            font=theme.FONT_BODY,
            bg=theme.BG,
            fg=theme.TEXT_DIM,
        ).pack(pady=(2, 0))

    def _build_choice_section(self, title: str, options: list, var) -> None:
        section = tk.Frame(self, bg=theme.BG)
        section.pack(fill="x", padx=44, pady=(20, 0))
        tk.Label(
            section,
            text=title,
            font=theme.FONT_BODY_BOLD,
            bg=theme.BG,
            fg=theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        row = tk.Frame(section, bg=theme.BG)
        row.pack(fill="x")

        buttons: list[tuple[tk.Button, object]] = []

        def refresh():
            for b, value in buttons:
                if var.get() == value:
                    b.config(bg=theme.PRIMARY, fg=theme.BG, activebackground=theme.PRIMARY_HOVER)
                else:
                    b.config(bg=theme.SURFACE, fg=theme.TEXT, activebackground=theme.SURFACE_LIGHT)

        for label, value in options:
            b = tk.Button(
                row,
                text=label,
                font=theme.FONT_BODY,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=12,
                pady=10,
                command=lambda v=value: (var.set(v), refresh()),
            )
            b.pack(side="left", padx=(0, 8), expand=True, fill="x")
            buttons.append((b, value))
        refresh()

    def _build_depth_section(self) -> None:
        section = tk.Frame(self, bg=theme.BG)
        section.pack(fill="x", padx=44, pady=(20, 0))
        head_row = tk.Frame(section, bg=theme.BG)
        head_row.pack(fill="x")
        tk.Label(
            head_row,
            text="AI search depth",
            font=theme.FONT_BODY_BOLD,
            bg=theme.BG,
            fg=theme.TEXT,
            anchor="w",
        ).pack(side="left")
        self.depth_value_label = tk.Label(
            head_row,
            text="4",
            font=theme.FONT_BODY_BOLD,
            bg=theme.BG,
            fg=theme.PRIMARY,
        )
        self.depth_value_label.pack(side="right")

        slider = tk.Scale(
            section,
            from_=1,
            to=9,
            orient="horizontal",
            variable=self.depth_var,
            bg=theme.BG,
            fg=theme.TEXT,
            troughcolor=theme.SURFACE,
            highlightthickness=0,
            sliderrelief="flat",
            activebackground=theme.PRIMARY,
            showvalue=0,
            command=lambda v: self.depth_value_label.config(text=str(int(float(v)))),
        )
        slider.pack(fill="x")
        tk.Label(
            section,
            text="Higher = stronger AI but slower",
            font=theme.FONT_SMALL,
            bg=theme.BG,
            fg=theme.TEXT_DIM,
        ).pack(anchor="w", pady=(2, 0))

    def _build_options_section(self) -> None:
        section = tk.Frame(self, bg=theme.BG)
        section.pack(fill="x", padx=44, pady=(20, 0))
        tk.Label(
            section,
            text="Options",
            font=theme.FONT_BODY_BOLD,
            bg=theme.BG,
            fg=theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 6))
        cb = tk.Checkbutton(
            section,
            text="Show evaluation tree after each AI move",
            variable=self.show_tree_var,
            bg=theme.BG,
            fg=theme.TEXT,
            activebackground=theme.BG,
            activeforeground=theme.TEXT,
            selectcolor=theme.SURFACE,
            font=theme.FONT_BODY,
            anchor="w",
            highlightthickness=0,
            bd=0,
        )
        cb.pack(fill="x")

    def _build_start_button(self) -> None:
        b = tk.Button(
            self,
            text="Start Game",
            font=theme.FONT_BUTTON,
            bg=theme.PRIMARY,
            fg=theme.BG,
            activebackground=theme.PRIMARY_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=28,
            pady=12,
            command=self._on_start,
        )
        b.pack(pady=(28, 24))

    def _on_start(self) -> None:
        self.result = {
            "board_size": self.size_var.get(),
            "max_depth": self.depth_var.get(),
            "ai_first": self.first_var.get() == "ai",
            "show_tree": self.show_tree_var.get(),
        }
        self.destroy()

    def _on_close(self) -> None:
        self.result = None
        self.destroy()
