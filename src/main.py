from include.tic_tac_toe import TicTacToe
from include.tic_tac_toe_handler import TicTacToeHandler
from include.dimension_getter import DimensionGetter
from include.first_move_getter import FirstMoveGetter
from include.depth_getter import DepthGetter

def main():
       
    depth_getter = DepthGetter()
    depth_getter.mainloop()

    first_move_getter = FirstMoveGetter()
    first_move_getter.mainloop()

    dimension_getter = DimensionGetter()
    dimension_getter.mainloop()

    max_depth = depth_getter._pressed
    computer_first = first_move_getter._pressed == 0
    board_size = dimension_getter._pressed

    print(max_depth)
    print(board_size)

    if board_size > 5:
        max_depth = 2
    
    handler = TicTacToeHandler(max_depth=max_depth, board_size=board_size)
    game = TicTacToe(handler, computer_first)
    game.mainloop()

if __name__ == "__main__":
    main()
