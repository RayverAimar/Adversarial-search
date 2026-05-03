"""Game window: board, stats panel, optional embedded evaluation tree."""

from __future__ import annotations

import time
import tkinter as tk
from typing import Callable

from include import theme
from include.minimax_tree import EMPTY, Minimax
from include.tic_tac_toe_handler import TicTacToeHandler
from include.tree_viewer import TreeViewer
from include.utils import Move


BOARD_CELL_SIZE = 88
STATS_PANEL_WIDTH = 240
TREE_PANEL_WIDTH = 1040
WINDOW_PADDING = 22


class TicTacToeGame(tk.Tk):
    def __init__(
        self,
        config: dict,
        on_new_game: Callable[[], None],
        on_quit: Callable[[], None],
    ):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.configure(bg=theme.BG)

        self._on_new_game = on_new_game
        self._on_quit = on_quit

        self.board_size: int = config["board_size"]
        self.max_depth: int = config["max_depth"]
        self.ai_first: bool = config["ai_first"]
        self.tree_visible: bool = config["show_tree"]

        # X always plays first; ai_first decides whether X is the AI or human.
        self.human_label = "O" if self.ai_first else "X"
        self.ai_label = "X" if self.ai_first else "O"

        self.handler = TicTacToeHandler(max_depth=self.max_depth, board_size=self.board_size)
        self.engine = Minimax(me=self.ai_label, opp=self.human_label, max_depth=self.max_depth)

        self._reset_stats()
        self.cells: dict[tuple[int, int], tk.Button] = {}
        self.gameover_overlay: tk.Frame | None = None
        self.last_ai_move: tuple[int, int] | None = None
        self._last_ai_snapshot: tuple[list, list, tuple] | None = None

        self._build_ui()
        self._sync_window_size()

        self.protocol("WM_DELETE_WINDOW", self._handle_quit)

        if self.ai_first:
            self.after(400, self._ai_move)

    def _reset_stats(self) -> None:
        self.stats = {
            "ai_moves": 0,
            "total_nodes": 0,
            "last_nodes": 0,
            "last_time_ms": 0.0,
        }

    def _sync_window_size(self) -> None:
        cell = BOARD_CELL_SIZE
        board_w = cell * self.board_size + 60
        h = max(560, cell * self.board_size + 200)
        w = board_w + STATS_PANEL_WIDTH + WINDOW_PADDING * 3
        if self.tree_visible:
            w += TREE_PANEL_WIDTH + WINDOW_PADDING
        theme.center(self, w, h)

    def _build_ui(self) -> None:
        self.outer = tk.Frame(self, bg=theme.BG)
        self.outer.pack(fill="both", expand=True, padx=WINDOW_PADDING, pady=WINDOW_PADDING)

        self._build_board_column()
        self._build_stats_panel()
        self._build_tree_panel()
        self._refresh_stats()

    def _build_board_column(self) -> None:
        column = tk.Frame(self.outer, bg=theme.BG)
        column.pack(side="left", fill="both", expand=True)

        self.status = tk.Label(
            column,
            text=self._initial_status(),
            font=theme.FONT_STATUS,
            bg=theme.BG,
            fg=theme.TEXT,
        )
        self.status.pack(pady=(0, 18))

        board_frame = tk.Frame(column, bg=theme.BG)
        board_frame.pack(expand=True)

        for r in range(self.board_size):
            for c in range(self.board_size):
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=theme.FONT_BOARD,
                    bg=theme.SURFACE,
                    fg=theme.TEXT,
                    activebackground=theme.SURFACE_LIGHT,
                    relief="flat",
                    bd=0,
                    width=2,
                    height=1,
                    cursor="hand2",
                    command=lambda rr=r, cc=c: self._cell_click(rr, cc),
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                self.cells[(r, c)] = btn

    def _build_stats_panel(self) -> None:
        panel = tk.Frame(self.outer, bg=theme.SURFACE, padx=18, pady=18, width=STATS_PANEL_WIDTH)
        panel.pack(side="left", fill="y", padx=(WINDOW_PADDING, 0))
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="Game Stats",
            font=theme.FONT_HEADING,
            bg=theme.SURFACE,
            fg=theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 14))

        self.stat_labels: dict[str, tk.Label] = {}
        for key, label in [
            ("config", "Configuration"),
            ("turn", "Current turn"),
            ("ai_moves", "AI moves"),
            ("last_nodes", "Last AI nodes"),
            ("last_time", "Last AI time"),
            ("total_nodes", "Total AI nodes"),
        ]:
            row = tk.Frame(panel, bg=theme.SURFACE)
            row.pack(fill="x", pady=5)
            tk.Label(
                row,
                text=label,
                font=theme.FONT_SMALL,
                bg=theme.SURFACE,
                fg=theme.TEXT_DIM,
                anchor="w",
            ).pack(anchor="w")
            v = tk.Label(
                row,
                text="—",
                font=theme.FONT_MONO,
                bg=theme.SURFACE,
                fg=theme.TEXT,
                anchor="w",
            )
            v.pack(anchor="w")
            self.stat_labels[key] = v

        bottom = tk.Frame(panel, bg=theme.SURFACE)
        bottom.pack(side="bottom", fill="x", pady=(20, 0))

        self.tree_toggle_button = self._action_button(
            bottom, self._tree_toggle_label(), self._toggle_tree, theme.PRIMARY
        )
        self.tree_toggle_button.pack(fill="x", pady=(0, 6))
        self.tree_toggle_button.config(state="disabled")

        self._action_button(bottom, "New Game", self._handle_new_game, theme.PRIMARY).pack(
            fill="x", pady=(0, 6)
        )
        self._action_button(bottom, "Quit", self._handle_quit, theme.ERROR).pack(fill="x")

    def _build_tree_panel(self) -> None:
        self.tree_viewer = TreeViewer(self.outer)
        if self.tree_visible:
            self.tree_viewer.pack(side="left", fill="both", expand=True, padx=(WINDOW_PADDING, 0))

    def _tree_toggle_label(self) -> str:
        return "Hide AI reasoning" if self.tree_visible else "Show AI reasoning"

    @staticmethod
    def _action_button(parent: tk.Frame, label: str, cmd: Callable, color: str) -> tk.Button:
        return tk.Button(
            parent,
            text=label,
            font=theme.FONT_BODY_BOLD,
            bg=color,
            fg=theme.BG,
            activebackground=theme.PRIMARY_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=9,
            command=cmd,
        )

    def _initial_status(self) -> str:
        return "AI is thinking…" if self.ai_first else "Your turn"

    def _refresh_stats(self) -> None:
        n = self.board_size
        self.stat_labels["config"].config(text=f"{n}×{n}, depth = {self.max_depth}")
        if self.gameover_overlay is not None:
            turn_text = "—"
        else:
            label = self.handler.current_player.label
            turn_text = "You" if label == self.human_label else "AI"
        self.stat_labels["turn"].config(text=turn_text)
        self.stat_labels["ai_moves"].config(text=str(self.stats["ai_moves"]))
        ln = self.stats["last_nodes"]
        self.stat_labels["last_nodes"].config(text=f"{ln:,}" if ln else "—")
        lt = self.stats["last_time_ms"]
        self.stat_labels["last_time"].config(text=f"{lt:.1f} ms" if lt else "—")
        tn = self.stats["total_nodes"]
        self.stat_labels["total_nodes"].config(text=f"{tn:,}" if tn else "—")

    def _cell_click(self, row: int, col: int) -> None:
        # AI cells stay clickable: clicking the AI's last move opens the tree.
        if self.last_ai_move == (row, col):
            self._show_tree()
            return
        self._human_click(row, col)

    def _human_click(self, row: int, col: int) -> None:
        if self.gameover_overlay is not None:
            return
        if self.handler.current_player.label != self.human_label:
            return
        move = Move(row, col, self.human_label)
        if not self.handler.is_valid_move(move):
            return
        self._apply_move(row, col, self.human_label)
        self.handler.process_move(move)
        if self._handle_terminal():
            return
        self.handler.toggle_player()
        self.status.config(text="AI is thinking…", fg=theme.ACCENT_O)
        self._refresh_stats()
        self.after(80, self._ai_move)

    def _ai_move(self) -> None:
        if self.gameover_overlay is not None:
            return

        board = [[EMPTY] * self.board_size for _ in range(self.board_size)]
        for row in self.handler._current_moves:
            for m in row:
                board[m.row][m.col] = m.label

        started = time.perf_counter()
        chosen = self.engine.best_move(board)
        elapsed_ms = (time.perf_counter() - started) * 1000

        self.stats["ai_moves"] += 1
        self.stats["last_nodes"] = self.engine.nodes_visited
        self.stats["last_time_ms"] = elapsed_ms
        self.stats["total_nodes"] += self.engine.nodes_visited
        self.last_ai_move = chosen
        self._last_ai_snapshot = (
            list(self.engine.candidates),
            [row[:] for row in board],
            chosen,
        )

        self.tree_viewer.update_tree(self.engine.candidates, self.ai_label, chosen, board)
        self.tree_toggle_button.config(state="normal")

        r, c = chosen
        self._apply_move(r, c, self.ai_label, ai=True)
        self.handler.process_move(Move(r, c, self.ai_label))

        if self._handle_terminal():
            return
        self.handler.toggle_player()
        self.status.config(text="Your turn", fg=theme.ACCENT_X)
        self._refresh_stats()

    def _apply_move(self, row: int, col: int, label: str, ai: bool = False) -> None:
        btn = self.cells[(row, col)]
        color = theme.ACCENT_X if label == "X" else theme.ACCENT_O
        # AI cells stay state="normal" so they remain clickable for tree
        # inspection. _cell_click filters out invalid plays.
        btn.config(text=label, fg=color)
        if ai:
            # Subtle outline on the AI cell hints that it's interactive.
            btn.config(highlightthickness=0)

    def _handle_terminal(self) -> bool:
        if self.handler.has_winner():
            winner = self.handler.current_player.label
            human_won = winner == self.human_label
            self._highlight_winning_cells()
            self._show_gameover(
                "You won!" if human_won else "AI won.",
                theme.SUCCESS if human_won else theme.ACCENT_O,
            )
            self._refresh_stats()
            return True
        if self.handler.is_tied():
            self._show_gameover("Tied game.", theme.WARNING)
            self._refresh_stats()
            return True
        return False

    def _highlight_winning_cells(self) -> None:
        for r, c in self.handler.winner_combo:
            self.cells[(r, c)].config(bg=theme.SUCCESS, fg=theme.BG)

    def _show_gameover(self, message: str, accent: str) -> None:
        self.status.config(text=message, fg=accent)

        overlay = tk.Frame(
            self,
            bg=theme.SURFACE,
            padx=28,
            pady=20,
            highlightbackground=accent,
            highlightthickness=2,
        )
        overlay.place(relx=0.5, rely=0.04, anchor="n")

        tk.Label(
            overlay,
            text=message,
            font=theme.FONT_HEADING,
            bg=theme.SURFACE,
            fg=accent,
        ).pack()

        btns = tk.Frame(overlay, bg=theme.SURFACE)
        btns.pack(pady=(12, 0))

        for label, cmd, bg in [
            ("Play Again", self._play_again, theme.PRIMARY),
            ("New Game", self._handle_new_game, theme.SURFACE_LIGHT),
            ("Quit", self._handle_quit, theme.ERROR),
        ]:
            tk.Button(
                btns,
                text=label,
                font=theme.FONT_BODY_BOLD,
                bg=bg,
                fg=theme.TEXT if bg == theme.SURFACE_LIGHT else theme.BG,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=7,
                command=cmd,
            ).pack(side="left", padx=4)

        self.gameover_overlay = overlay

    def _toggle_tree(self) -> None:
        if self.tree_visible:
            self.tree_viewer.pack_forget()
        else:
            self.tree_viewer.pack(side="left", fill="both", expand=True, padx=(WINDOW_PADDING, 0))
        self.tree_visible = not self.tree_visible
        self.tree_toggle_button.config(text=self._tree_toggle_label())
        self._sync_window_size()

    def _show_tree(self) -> None:
        if not self.tree_visible:
            self._toggle_tree()
        # Re-show last AI snapshot in case the user previously inspected another move.
        if self._last_ai_snapshot is not None:
            cands, board_snapshot, chosen = self._last_ai_snapshot
            self.tree_viewer.update_tree(cands, self.ai_label, chosen, board_snapshot)

    def _play_again(self) -> None:
        if self.gameover_overlay is not None:
            self.gameover_overlay.destroy()
            self.gameover_overlay = None

        self.handler.reset_game()
        for btn in self.cells.values():
            btn.config(text="", bg=theme.SURFACE, fg=theme.TEXT, state="normal")
        self._reset_stats()
        self.last_ai_move = None
        self._last_ai_snapshot = None
        self.tree_toggle_button.config(state="disabled")
        self.status.config(text=self._initial_status(), fg=theme.TEXT)
        self._refresh_stats()

        if self.ai_first:
            self.after(400, self._ai_move)

    def _handle_new_game(self) -> None:
        self.destroy()
        self._on_new_game()

    def _handle_quit(self) -> None:
        self.destroy()
        self._on_quit()
