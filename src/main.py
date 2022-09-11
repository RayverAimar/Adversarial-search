from include.tic_tac_toe import TicTacToe
from include.tic_tac_toe_handler import TicTacToeHandler

def main():
    handler = TicTacToeHandler()
    game = TicTacToe(handler)
    game.mainloop()

if __name__ == "__main__":
    main()
