"""Benchmark: alpha-beta vs naive minimax.

Runs the AI from the empty board on different board sizes / depths and records
nodes visited and wall-clock time. Saves ``benchmark.png`` in the current dir.

Run from the ``src/`` directory:
    python benchmark.py
"""

from __future__ import annotations

import time

import matplotlib.pyplot as plt

from include.minimax_tree import EMPTY, INF, Minimax, empty_cells, heuristic, is_full, winner_on


class NaiveMinimax(Minimax):
    """Same engine, but with alpha-beta cutoffs disabled."""

    def _search(self, board, depth, alpha, beta, maximizing):
        self.nodes_visited += 1
        winner = winner_on(board)
        if winner == self.me:
            return INF - depth
        if winner == self.opp:
            return -INF + depth
        if depth >= self.max_depth or is_full(board):
            return heuristic(board, self.me, self.opp)

        player = self.me if maximizing else self.opp
        best = -INF if maximizing else INF
        for r, c in empty_cells(board):
            board[r][c] = player
            v = self._search(board, depth + 1, alpha, beta, not maximizing)
            board[r][c] = EMPTY
            best = max(best, v) if maximizing else min(best, v)
        return best


def run_one(engine_cls, size: int, depth: int) -> tuple[int, float]:
    board = [[EMPTY] * size for _ in range(size)]
    engine = engine_cls(me="X", opp="O", max_depth=depth)
    started = time.perf_counter()
    engine.best_move(board)
    elapsed = time.perf_counter() - started
    return engine.nodes_visited, elapsed


def main() -> None:
    cases = [
        ("3x3 d=9", 3, 9),
        ("3x3 d=6", 3, 6),
        ("4x4 d=4", 4, 4),
        ("4x4 d=5", 4, 5),
    ]

    rows = []
    for label, size, depth in cases:
        naive_nodes, naive_t = run_one(NaiveMinimax, size, depth)
        ab_nodes, ab_t = run_one(Minimax, size, depth)
        rows.append((label, naive_nodes, ab_nodes, naive_t, ab_t))
        print(f"{label:>10} | naive {naive_nodes:>10,} ({naive_t:6.2f}s) | α-β {ab_nodes:>10,} ({ab_t:6.2f}s)")

    labels = [r[0] for r in rows]
    naive_nodes = [r[1] for r in rows]
    ab_nodes = [r[2] for r in rows]
    naive_times = [r[3] for r in rows]
    ab_times = [r[4] for r in rows]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Naive minimax vs alpha-beta pruning", fontsize=14, fontweight="bold")

    x = range(len(labels))
    width = 0.38

    ax1.bar([i - width / 2 for i in x], naive_nodes, width, label="naive", color="#d35454")
    ax1.bar([i + width / 2 for i in x], ab_nodes, width, label="alpha-beta", color="#3a8dde")
    ax1.set_yscale("log")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(labels)
    ax1.set_ylabel("Nodes visited (log scale)")
    ax1.set_title("Search-space size")
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    ax2.bar([i - width / 2 for i in x], naive_times, width, label="naive", color="#d35454")
    ax2.bar([i + width / 2 for i in x], ab_times, width, label="alpha-beta", color="#3a8dde")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(labels)
    ax2.set_ylabel("Wall-clock time (seconds)")
    ax2.set_title("Time to choose first move")
    ax2.legend()
    ax2.grid(axis="y", alpha=0.3)

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.savefig("benchmark.png", dpi=140, bbox_inches="tight")
    print("\nSaved benchmark.png")


if __name__ == "__main__":
    main()
