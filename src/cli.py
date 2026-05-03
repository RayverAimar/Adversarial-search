"""Headless CLI to play tic-tac-toe vs the minimax AI.

Useful for:
- Playing without a display (servers, CI, screenshots).
- Benchmarking and testing the search engine.

Usage:
    python cli.py                  # 3x3, depth 9 (perfect play), AI second
    python cli.py --size 4         # 4x4 board
    python cli.py --depth 3        # cap search depth
    python cli.py --ai-first       # AI plays first
    python cli.py --self-play      # AI vs AI
"""

from __future__ import annotations

import argparse
import sys
import time

from include.minimax_tree import EMPTY, Minimax, is_full, winner_on


def render(board: list[list[str]]) -> str:
    size = len(board)
    cell_w = 3
    sep = "\n" + "+".join(["-" * cell_w] * size) + "\n"
    rows = []
    for row in board:
        rows.append("|".join(f" {cell or ' '} " for cell in row))
    return sep.join(rows)


def parse_move(raw: str, size: int) -> tuple[int, int] | None:
    try:
        r, c = (int(x) for x in raw.replace(",", " ").split())
    except ValueError:
        return None
    if not (0 <= r < size and 0 <= c < size):
        return None
    return r, c


def play_human(board, mark: str) -> tuple[int, int]:
    while True:
        raw = input(f"Your move ({mark}) as 'row col' [0-{len(board) - 1}]: ").strip()
        move = parse_move(raw, len(board))
        if move and board[move[0]][move[1]] == EMPTY:
            return move
        print("  invalid — try again")


def play_ai(board, ai: Minimax, label: str) -> tuple[int, int]:
    started = time.perf_counter()
    move = ai.best_move(board)
    elapsed = time.perf_counter() - started
    print(f"AI ({label}) → {move}  [nodes={ai.nodes_visited:,}  time={elapsed * 1000:.1f} ms]")
    return move


def play_one_game(args) -> None:
    size = args.size
    board = [[EMPTY] * size for _ in range(size)]

    labels = ("X", "O")
    if args.self_play:
        engines = (
            Minimax(me="X", opp="O", max_depth=args.depth),
            Minimax(me="O", opp="X", max_depth=args.depth),
        )
    else:
        ai_label = "X" if args.ai_first else "O"
        human_label = "O" if args.ai_first else "X"
        ai = Minimax(me=ai_label, opp=human_label, max_depth=args.depth)

    print(render(board))
    print()

    turn = 0
    while True:
        mark = labels[turn % 2]
        if args.self_play:
            move = play_ai(board, engines[turn % 2], mark)
        elif mark == ai_label:
            move = play_ai(board, ai, mark)
        else:
            move = play_human(board, mark)
        board[move[0]][move[1]] = mark

        print(render(board))
        print()

        win = winner_on(board)
        if win:
            print(f"{win} wins!")
            return
        if is_full(board):
            print("Tied game.")
            return
        turn += 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tic-tac-toe vs minimax AI (CLI)")
    parser.add_argument("--size", type=int, default=3, help="Board size N x N (default: 3)")
    parser.add_argument("--depth", type=int, default=9, help="Max search depth (default: 9)")
    parser.add_argument("--ai-first", action="store_true", help="AI plays first")
    parser.add_argument("--self-play", action="store_true", help="AI vs AI")
    parser.add_argument("--no-replay", action="store_true", help="Exit after one game (default: ask to replay)")
    args = parser.parse_args(argv)

    while True:
        play_one_game(args)
        if args.no_replay:
            return 0
        try:
            again = input("\nPlay again? [y/N]: ").strip().lower()
        except EOFError:
            return 0
        if again not in {"y", "yes"}:
            return 0
        print()


if __name__ == "__main__":
    sys.exit(main())
