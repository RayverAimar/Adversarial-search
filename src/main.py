from include.tic_tac_toe import TicTacToe
from include.tic_tac_toe_handler import TicTacToeHandler
from include.dimension_getter import DimensionGetter
from include.first_move_getter import FirstMoveGetter
from include.depth_getter import DepthGetter

def main():
    max_depth = 2 #Tk Button
    computer_first = True # Tk Button
    board_size = 3 #Tk Button
    
    depth_getter = DepthGetter()
    depth_getter.mainloop()
    print("Pressed:", depth_getter._pressed)

    first_move_getter = FirstMoveGetter()
    first_move_getter.mainloop()
    print("Pressed:", first_move_getter._pressed)

    
    dimension_getter = DimensionGetter()
    dimension_getter.mainloop()

    print("Pressed:", dimension_getter._pressed)

    
    max_depth = depth_getter._pressed
    computer_first = first_move_getter._pressed == 0
    board_size = dimension_getter._pressed

    if board_size > 5:
        max_depth = 2
    
    print("Max_depth:", max_depth)
    print("Board size:", board_size)

    handler = TicTacToeHandler(max_depth=max_depth, board_size=board_size)
    game = TicTacToe(handler, computer_first)
    game.mainloop()

if __name__ == "__main__":
    main()
