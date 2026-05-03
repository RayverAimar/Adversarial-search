"""Embedded tree-viewer widget: chart of root candidates + click-to-inspect panel."""

from __future__ import annotations

import copy
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from include import theme
from include.minimax_tree import INF, heuristic_breakdown


class TreeViewer(tk.Frame):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent, bg=theme.BG)

        self._board: list[list[str]] | None = None
        self._ai_label: str | None = None
        self._opp_label: str | None = None
        self._chosen: tuple[int, int] | None = None
        self._candidates: list[tuple[tuple[int, int], int]] = []
        self._node_artists: list = []
        self._node_to_move: list[tuple[int, int]] = []

        self._build_ui()
        self._draw_placeholder()

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=theme.BG)
        header.pack(fill="x", pady=(0, 8))
        tk.Label(
            header,
            text="Evaluation tree",
            font=theme.FONT_HEADING,
            bg=theme.BG,
            fg=theme.TEXT,
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Click any candidate to see the resulting position and heuristic.",
            font=theme.FONT_SMALL,
            bg=theme.BG,
            fg=theme.TEXT_DIM,
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        body = tk.Frame(self, bg=theme.BG)
        body.pack(fill="both", expand=True)

        # Inspection panel packed first so it reserves its width before the
        # canvas claims the remaining space with expand=True.
        panel = tk.Frame(body, bg=theme.SURFACE, padx=16, pady=16, width=300)
        panel.pack(side="right", fill="y", padx=(12, 0))
        panel.pack_propagate(False)

        self.figure, self.ax = plt.subplots(figsize=(6.4, 4.4))
        self.figure.patch.set_facecolor(theme.BG)
        self.canvas = FigureCanvasTkAgg(self.figure, master=body)
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        self.canvas.mpl_connect("pick_event", self._on_pick)

        tk.Label(
            panel,
            text="Inspect a candidate",
            font=theme.FONT_HEADING,
            bg=theme.SURFACE,
            fg=theme.TEXT,
            anchor="w",
        ).pack(fill="x")
        self.panel_subtitle = tk.Label(
            panel,
            text="Click a node in the chart →",
            font=theme.FONT_SMALL,
            bg=theme.SURFACE,
            fg=theme.TEXT_DIM,
            anchor="w",
            wraplength=260,
            justify="left",
        )
        self.panel_subtitle.pack(fill="x", pady=(2, 12))

        self.mini_canvas = tk.Canvas(
            panel,
            width=220,
            height=220,
            bg=theme.BG,
            highlightthickness=0,
        )
        self.mini_canvas.pack(pady=(0, 12))

        self.minimax_label = tk.Label(
            panel,
            text="—",
            font=theme.FONT_BODY_BOLD,
            bg=theme.SURFACE,
            fg=theme.TEXT,
            anchor="w",
            justify="left",
        )
        self.minimax_label.pack(fill="x")

        self.heuristic_label = tk.Label(
            panel,
            text="",
            font=theme.FONT_SMALL,
            bg=theme.SURFACE,
            fg=theme.TEXT_DIM,
            anchor="w",
            justify="left",
            wraplength=260,
        )
        self.heuristic_label.pack(fill="x", pady=(4, 8))

        self.breakdown_label = tk.Label(
            panel,
            text="",
            font=theme.FONT_MONO,
            bg=theme.SURFACE,
            fg=theme.TEXT,
            anchor="nw",
            justify="left",
            wraplength=260,
        )
        self.breakdown_label.pack(fill="both", expand=True)

    def update_tree(
        self,
        candidates: list[tuple[tuple[int, int], int]],
        ai_label: str,
        chosen: tuple[int, int],
        board_before_ai: list[list[str]],
    ) -> None:
        self._board = copy.deepcopy(board_before_ai)
        self._ai_label = ai_label
        self._opp_label = "O" if ai_label == "X" else "X"
        self._chosen = chosen
        self._candidates = sorted(candidates, key=lambda c: -c[1])
        self._draw_chart()
        self._select_move(chosen)

    def _draw_placeholder(self) -> None:
        self.ax.clear()
        self.ax.set_facecolor(theme.BG)
        self.ax.text(
            0.5,
            0.5,
            "Waiting for the first AI move…",
            ha="center",
            va="center",
            color=theme.TEXT_DIM,
            fontsize=13,
        )
        self.ax.axis("off")
        self.canvas.draw()

    def _draw_chart(self) -> None:
        self.ax.clear()
        self.ax.set_facecolor(theme.BG)
        self._node_artists = []
        self._node_to_move = []

        cands = self._candidates
        n = len(cands)
        if n == 0:
            self._draw_placeholder()
            return

        scores = [s for _, s in cands]
        smin, smax = min(scores), max(scores)
        srange = max(smax - smin, 1)

        root_x = (n - 1) / 2.0
        self.ax.set_xlim(-0.7, n - 0.3)
        self.ax.set_ylim(-0.55, 1.55)

        for i, (move, _) in enumerate(cands):
            is_chosen = move == self._chosen
            self.ax.plot(
                [root_x, i],
                [1.0, 0.0],
                color=theme.SUCCESS if is_chosen else theme.BORDER,
                linewidth=2.4 if is_chosen else 1.0,
                zorder=1,
            )

        self.ax.scatter([root_x], [1.0], s=900, color=theme.PRIMARY, zorder=3, edgecolors="white", linewidths=1.5)
        self.ax.text(root_x, 1.0, "root", ha="center", va="center", fontsize=10, color=theme.BG, fontweight="bold", zorder=4)
        self.ax.text(root_x, 1.22, f"AI plays '{self._ai_label}'", ha="center", color=theme.TEXT, fontsize=10)

        for i, (move, score) in enumerate(cands):
            t = (score - smin) / srange
            color = self._score_color(t)
            is_chosen = move == self._chosen
            artist = self.ax.scatter(
                [i],
                [0.0],
                s=1100 if is_chosen else 700,
                color=color,
                zorder=3,
                edgecolors=theme.SUCCESS if is_chosen else theme.BORDER,
                linewidths=2.4 if is_chosen else 0.8,
                picker=True,
            )
            self._node_artists.append(artist)
            self._node_to_move.append(move)
            self.ax.text(i, 0.0, f"{move[0]},{move[1]}", ha="center", va="center", fontsize=10, color=theme.BG, fontweight="bold", zorder=4)
            self.ax.text(i, -0.22, _format_score(score), ha="center", va="top", color=theme.TEXT, fontsize=10)

        self.ax.text(-0.65, -0.45, "● higher score = better for AI", color=theme.TEXT_DIM, fontsize=9)
        self.ax.axis("off")
        self.figure.tight_layout()
        self.canvas.draw()

    @staticmethod
    def _score_color(t: float):
        if t < 0.5:
            return (0.95, 0.45 + t * 0.9, 0.40)
        return (1.0 - (t - 0.5) * 1.4, 0.95, 0.45)

    def _on_pick(self, event) -> None:
        for artist, move in zip(self._node_artists, self._node_to_move):
            if event.artist is artist:
                self._select_move(move)
                return

    def _select_move(self, move: tuple[int, int]) -> None:
        if self._board is None or self._ai_label is None or self._opp_label is None:
            return

        board_after = copy.deepcopy(self._board)
        board_after[move[0]][move[1]] = self._ai_label

        score = next((s for m, s in self._candidates if m == move), 0)
        breakdown = heuristic_breakdown(board_after, self._ai_label, self._opp_label)
        static_score = breakdown["total"]

        self._draw_mini_board(board_after, highlight=move)

        is_chosen = move == self._chosen
        self.panel_subtitle.config(
            text=f"Move ({move[0]}, {move[1]})" + ("  •  chosen by AI" if is_chosen else "")
        )
        self.minimax_label.config(text=f"Minimax score:  {_format_score(score)}")
        self.heuristic_label.config(
            text=(
                f"Static heuristic: {static_score:+d}\n"
                f"(score if the search stopped here)"
            )
        )
        self.breakdown_label.config(text=_format_breakdown(breakdown, self._ai_label, self._opp_label))

    def _draw_mini_board(self, board: list[list[str]], highlight: tuple[int, int] | None) -> None:
        self.mini_canvas.delete("all")
        size = len(board)
        cell = 220 // size
        for r in range(size):
            for c in range(size):
                x0, y0 = c * cell + 4, r * cell + 4
                x1, y1 = (c + 1) * cell - 4, (r + 1) * cell - 4
                bg = theme.SURFACE_LIGHT
                if highlight is not None and (r, c) == highlight:
                    bg = theme.SUCCESS
                self.mini_canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline=theme.BORDER)
                v = board[r][c]
                if v:
                    color = theme.ACCENT_X if v == "X" else theme.ACCENT_O
                    if highlight is not None and (r, c) == highlight:
                        color = theme.BG
                    self.mini_canvas.create_text(
                        (x0 + x1) / 2,
                        (y0 + y1) / 2,
                        text=v,
                        fill=color,
                        font=("Helvetica", max(14, cell // 2), "bold"),
                    )


def _format_score(s: int) -> str:
    if s > INF // 2:
        return "WIN"
    if s < -INF // 2:
        return "LOSE"
    return f"{s:+d}"


def _format_breakdown(b: dict, me: str, opp: str) -> str:
    lines = [
        "Heuristic = Σ(my marks)² − Σ(opp marks)²",
        "",
        f"AI ({me}) lines:  +{b['me_score']}",
    ]
    if b["me_lines"]:
        for combo, count in b["me_lines"][:3]:
            lines.append(f"  {_combo_str(combo)} → {count}² = +{count * count}")
        if len(b["me_lines"]) > 3:
            lines.append(f"  …and {len(b['me_lines']) - 3} more")
    else:
        lines.append("  (no winning lines available)")

    lines.extend(["", f"Opp ({opp}) lines: −{b['opp_score']}"])
    if b["opp_lines"]:
        for combo, count in b["opp_lines"][:3]:
            lines.append(f"  {_combo_str(combo)} → −{count}² = −{count * count}")
        if len(b["opp_lines"]) > 3:
            lines.append(f"  …and {len(b['opp_lines']) - 3} more")
    else:
        lines.append("  (no opp threats)")

    lines.extend(["", f"Dead lines: {len(b['dead_lines'])} (mixed)"])
    return "\n".join(lines)


def _combo_str(combo: tuple[tuple[int, int], ...]) -> str:
    return " ".join(f"({r},{c})" for r, c in combo)
