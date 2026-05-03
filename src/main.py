"""Tk GUI entry point — loops between the config dialog and the game window."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from include.config_dialog import ConfigDialog
from include.tic_tac_toe import TicTacToeGame


def run() -> None:
    while True:
        dialog = ConfigDialog()
        dialog.mainloop()
        config = dialog.result
        if config is None:
            return

        wants_new_config = {"value": False}

        def on_new_game():
            wants_new_config["value"] = True

        def on_quit():
            wants_new_config["value"] = False

        game = TicTacToeGame(config, on_new_game=on_new_game, on_quit=on_quit)
        game.mainloop()

        if not wants_new_config["value"]:
            return


if __name__ == "__main__":
    run()
