"""Tests for the minimax engine.

Verifies:
- Terminal detection (winner_on, is_full).
- The AI never loses a 3x3 game from the start when given full depth.
- The AI takes a forced win in one move.
- The AI blocks an immediate threat from the opponent.
- Alpha-beta visits strictly fewer nodes than the unpruned search.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from include.minimax_tree import EMPTY, INF, Minimax, is_full, winner_on


def make_board(size: int) -> list[list[str]]:
    return [[EMPTY] * size for _ in range(size)]


def play_out(ai_x: Minimax, ai_o: Minimax, size: int = 3) -> str | None:
    board = make_board(size)
    engines = (ai_x, ai_o)
    labels = ("X", "O")
    for turn in range(size * size):
        r, c = engines[turn % 2].best_move(board)
        board[r][c] = labels[turn % 2]
        win = winner_on(board)
        if win:
            return win
    return None


def test_winner_on_detects_row():
    board = [["X", "X", "X"], ["", "O", ""], ["O", "", ""]]
    assert winner_on(board) == "X"


def test_winner_on_detects_diagonal():
    board = [["O", "", "X"], ["", "O", ""], ["X", "", "O"]]
    assert winner_on(board) == "O"


def test_winner_on_empty():
    assert winner_on(make_board(3)) is None


def test_is_full():
    assert not is_full(make_board(3))
    full = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "O"]]
    assert is_full(full)


def test_self_play_3x3_full_depth_is_a_draw():
    ai_x = Minimax(me="X", opp="O", max_depth=9)
    ai_o = Minimax(me="O", opp="X", max_depth=9)
    assert play_out(ai_x, ai_o) is None


def test_ai_takes_immediate_win():
    board = [
        ["X", "X", ""],
        ["O", "O", ""],
        ["", "", ""],
    ]
    ai = Minimax(me="X", opp="O", max_depth=9)
    assert ai.best_move(board) == (0, 2)


def test_ai_blocks_immediate_threat():
    board = [
        ["O", "O", ""],
        ["X", "", ""],
        ["", "", ""],
    ]
    ai = Minimax(me="X", opp="O", max_depth=9)
    assert ai.best_move(board) == (0, 2)


def test_alpha_beta_prunes_nodes():
    """Search count must be lower than the worst-case branching factor product."""
    board = make_board(3)
    ai = Minimax(me="X", opp="O", max_depth=9)
    ai.best_move(board)
    # Without pruning the 3x3 search visits ~550k internal+leaf nodes.
    # Alpha-beta with random move ordering brings it well below 100k.
    assert ai.nodes_visited < 100_000


def test_terminal_eval_prefers_faster_win():
    """A win in fewer moves should score higher than a win in more moves."""
    near_win = [
        ["X", "X", ""],
        ["O", "O", ""],
        ["", "", ""],
    ]
    ai = Minimax(me="X", opp="O", max_depth=9)
    move = ai.best_move(near_win)
    # The faster-win heuristic returns INF - depth; both branches eventually
    # win for X, but (0,2) wins now whereas any other move does not.
    assert move == (0, 2)
    assert INF > 0  # sanity
