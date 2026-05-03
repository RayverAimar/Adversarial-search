"""Minimax with alpha-beta pruning for N x N tic-tac-toe.

The previous implementation built an explicit tree of ``Node`` objects, deep-copied
the board at every child, and recomputed winning combos on every access. This
version mutates the board in place (move / unmove), uses iterative-style
recursion, prunes with alpha-beta, and caches the winning combos for a given
board size.
"""

from __future__ import annotations

import random
from functools import lru_cache

INF = 10**9
EMPTY = ""


@lru_cache(maxsize=16)
def winning_combos(size: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return all winning lines for an ``size x size`` board.

    Cached per board size — these never change once computed.
    """
    rows = [tuple((r, c) for c in range(size)) for r in range(size)]
    cols = [tuple((r, c) for r in range(size)) for c in range(size)]
    diag1 = tuple((i, i) for i in range(size))
    diag2 = tuple((i, size - 1 - i) for i in range(size))
    return tuple(rows + cols + [diag1, diag2])


def winner_on(board: list[list[str]]) -> str | None:
    """Return the avatar that wins on this board, or ``None``."""
    size = len(board)
    for combo in winning_combos(size):
        first = board[combo[0][0]][combo[0][1]]
        if first == EMPTY:
            continue
        if all(board[r][c] == first for r, c in combo):
            return first
    return None


def is_full(board: list[list[str]]) -> bool:
    return all(cell != EMPTY for row in board for cell in row)


def empty_cells(board: list[list[str]]) -> list[tuple[int, int]]:
    return [(r, c) for r, row in enumerate(board) for c, cell in enumerate(row) if cell == EMPTY]


def heuristic(board: list[list[str]], me: str, opp: str) -> int:
    """Count of lines still winnable by ``me`` minus those winnable by ``opp``.

    A line is winnable by a player if it contains only that player's marks
    and empty cells (no opposing marks).
    """
    score = 0
    for combo in winning_combos(len(board)):
        cells = [board[r][c] for r, c in combo]
        if opp not in cells:
            score += 1
        if me not in cells:
            score -= 1
    return score


class Minimax:
    """Alpha-beta minimax search.

    ``best_move(board)`` returns the move the AI should play next. The AI plays
    ``self.me``; the opponent plays ``self.opp``. The board is mutated during
    search and restored before each call returns.
    """

    def __init__(self, me: str, opp: str, max_depth: int):
        self.me = me
        self.opp = opp
        self.max_depth = max_depth
        self.nodes_visited = 0

    def best_move(self, board: list[list[str]]) -> tuple[int, int]:
        self.nodes_visited = 0
        best_score = -INF
        best_moves: list[tuple[int, int]] = []

        moves = empty_cells(board)
        random.shuffle(moves)  # break ties randomly so AI doesn't always pick top-left

        for move in moves:
            r, c = move
            board[r][c] = self.me
            score = self._search(board, depth=1, alpha=-INF, beta=INF, maximizing=False)
            board[r][c] = EMPTY

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _search(self, board, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
        self.nodes_visited += 1

        winner = winner_on(board)
        if winner == self.me:
            # Prefer faster wins / slower losses by including remaining capacity.
            return INF - depth
        if winner == self.opp:
            return -INF + depth
        if depth >= self.max_depth or is_full(board):
            return heuristic(board, self.me, self.opp)

        player = self.me if maximizing else self.opp
        if maximizing:
            value = -INF
            for r, c in empty_cells(board):
                board[r][c] = player
                value = max(value, self._search(board, depth + 1, alpha, beta, False))
                board[r][c] = EMPTY
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = INF
            for r, c in empty_cells(board):
                board[r][c] = player
                value = min(value, self._search(board, depth + 1, alpha, beta, True))
                board[r][c] = EMPTY
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value


class MinimaxTree:
    """Backwards-compatible adapter for the GUI code.

    The GUI used to access ``tree.root.children[tree.root.idx_best_child].move_to_get_here``.
    We expose the same shape using a thin wrapper around :class:`Minimax`, so
    the GUI code does not have to change.
    """

    def __init__(self, board, avatar, max_depth):
        opp = "O" if avatar == "X" else "X"
        engine = Minimax(me=avatar, opp=opp, max_depth=max_depth)
        move = engine.best_move(board)
        self.nodes_visited = engine.nodes_visited
        self.root = _RootShim(move)


class _RootShim:
    def __init__(self, move: tuple[int, int]):
        self.idx_best_child = 0
        self.children = [_ChildShim(move)]


class _ChildShim:
    def __init__(self, move: tuple[int, int]):
        self.move_to_get_here = move
