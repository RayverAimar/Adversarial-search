"""Drive each Tk screen and save tightly cropped PNGs for the README.

Outputs three files in the repo root:
- gui_config.png       — configuration dialog
- gui_game.png         — game in progress, stats panel + tree viewer side-by-side
- gui_gameover.png     — game-over overlay
"""

import os
import subprocess
import sys
import time
import tkinter as tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))


def _activate_python() -> None:
    subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to set frontmost of first process whose name contains "ython" to true',
        ],
        check=False,
    )


def shoot(out: str, x: int, y: int, w: int, h: int) -> None:
    _activate_python()
    time.sleep(0.5)
    subprocess.run(["screencapture", "-x", "-R", f"{x},{y},{w},{h}", out], check=True)
    print(f"Saved {out}  ({w}x{h} at {x},{y})")


def shoot_window(window: tk.Misc, out: str, pad: int = 10) -> None:
    """Screenshot using the window's actual on-screen rect (handles macOS quirks)."""
    window.update_idletasks()
    window.update()
    x = window.winfo_rootx() - pad
    y = window.winfo_rooty() - 30  # include the title bar
    w = window.winfo_width() + 2 * pad
    h = window.winfo_height() + 30 + pad
    shoot(out, x, y, w, h)


def shoot_rect(windows: list, out: str, pad: int = 10) -> None:
    """Screenshot the bounding box of multiple windows."""
    for w in windows:
        w.update_idletasks()
        w.update()
    xs = [w.winfo_rootx() for w in windows]
    ys = [w.winfo_rooty() - 30 for w in windows]
    rxs = [w.winfo_rootx() + w.winfo_width() for w in windows]
    rys = [w.winfo_rooty() + w.winfo_height() for w in windows]
    x = min(xs) - pad
    y = min(ys) - pad
    w = max(rxs) - x + pad
    h = max(rys) - y + pad
    shoot(out, x, y, w, h)


def position(window, x: int, y: int, w: int, h: int) -> None:
    window.geometry(f"{w}x{h}+{x}+{y}")
    window.update_idletasks()
    window.update()


def pump(window, seconds: float) -> None:
    """Run Tk events for ``seconds`` (time.sleep alone does not pump events)."""
    end = time.time() + seconds
    while time.time() < end:
        window.update()
        time.sleep(0.02)


def shoot_config() -> None:
    from include.config_dialog import ConfigDialog

    dlg = ConfigDialog()
    position(dlg, 100, 100, 480, 600)
    dlg.update()
    dlg.lift()
    dlg.attributes("-topmost", True)
    dlg.update()
    time.sleep(1.0)
    shoot_window(dlg, os.path.join(ROOT, "gui_config.png"))
    dlg.destroy()


def shoot_game_and_tree() -> None:
    from include.tic_tac_toe import TicTacToeGame

    # 4x4 d=3: the heuristic matters here, so candidate scores actually differ.
    config = {"board_size": 4, "max_depth": 3, "ai_first": False, "show_tree": True}
    game = TicTacToeGame(config, on_new_game=lambda: None, on_quit=lambda: None)
    pump(game, 0.4)

    game._human_click(1, 1)
    pump(game, 0.6)
    game._human_click(2, 2)
    pump(game, 0.6)

    game.lift()
    game.attributes("-topmost", True)
    pump(game, 1.0)

    shoot_window(game, os.path.join(ROOT, "gui_game.png"))
    game.destroy()


def shoot_gameover() -> None:
    from include.tic_tac_toe import TicTacToeGame

    config = {"board_size": 3, "max_depth": 9, "ai_first": False, "show_tree": False}
    game = TicTacToeGame(config, on_new_game=lambda: None, on_quit=lambda: None)
    position(game, 200, 100, 640, 540)
    game.update()

    # Force a quick AI win sequence:
    # Human X plays corner; AI O plays optimally.
    sequence = [(0, 0), (2, 2), (0, 2), (1, 1), (1, 0)]
    for r, c in sequence:
        if game.gameover_overlay is not None:
            break
        game._human_click(r, c)
        game.update()
        pump(game, 0.3)
        game.update()

    # If still ongoing (unlikely), force one more AI move
    if game.gameover_overlay is None:
        game._ai_move()
        game.update()
        pump(game, 0.3)

    game.lift()
    game.attributes("-topmost", True)
    game.update()
    time.sleep(1.0)

    shoot_window(game, os.path.join(ROOT, "gui_gameover.png"))
    game.destroy()


if __name__ == "__main__":
    shoot_config()
    shoot_game_and_tree()
    shoot_gameover()
    print("Done.")
