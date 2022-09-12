
from multiprocessing.sharedctypes import Value
from include.utils import Move

avatars = []

class Node(object):

    def __init__(self, board : list, avatar, max_depth, moves_played, depth = 0):
        self.children = []
        self.board = board
        self.depth = depth
        self.max_depth = max_depth
        self.avatar = avatar
        self.moves_played = moves_played
        self.move : tuple
        self.value : int
        self._winning_combos = self._get_winning_combos()
        self.winning_combo = self._get_actual_combos()
        self.max_moves_played = len(self.board)*len(self.board)

        self.is_leaf = self.winning_combo or (self.moves_played == self.max_moves_played) or self.depth == self.max_depth

        #See if the board has already a winning combo, then return its value and the position of its best child

        if (not self.is_leaf):
            self.spread()
        else:
            self.value = self.get_node_value()
        #See the child with most-least value and return its moved position
        


    def get_node_value(self):
        value : int

        if(self.winning_combo):
            value = self.max_moves_played + (self.max_moves_played - self.moves_played)
            if self.depth % 2:
                return value
            else:
                return value * -1
        else:
        ##Aritmetica combos player - combos computer
            value = self.arimetica()
        return value
        

    def _get_winning_combos(self):
        rows = [
            [(row, col) for col in len(self.board)]
            for row in len(self.board)
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
        
    def _get_actual_combos(self, avatar):
        combos = 0
        for combo in self._winning_combos:
            results = set(self.board[n][m] for n, m in combo)
            is_win = (len(results) == 1) and (' ' in results)
            is_win2 = (len(results) == 2) and (' ' in results) and (avatar in results)
            #print(results, " " , is_win, " ", is_win2);
            if is_win or is_win2:
                combos+=1
        return combos

    def arimetica(self):
        _winning_combos  = self._get_winning_combos(self.board)
        computer_options = self._get_actual_combos(_winning_combos, self.avatar)
        human_avatar:str
        if avatars[0] != self.avatar:
            human_avatar = avatars[0]
        else:
            human_avatar = avatars[1]
        human_options    = self._get_actual_combos(_winning_combos, human_avatar) 
        print(computer_options, "-", human_options)
        return computer_options - human_options

    def spread(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == "":
                    copy_board = self.board.copy()
                    copy_board[row][col] = self.avatar
                    self.move = (row, col)
                    child = Node(copy_board, avatars[(self.depth+1)%2], depth=self.depth+1)
                    self.children.append(child)
    
    def draw(self):
        for rows in self.board:
            for cols in rows:
                print(cols, end = " ")
            print()

class MinimaxTree(object):

    def __init__(self, board : list, avatar, max_depth):
        self.avatar = avatar
        self.max_depth = max_depth
        self.board = board
        avatars.clear()
        avatars.append(self.avatar)
        if self.avatar == "X":
            avatars.append("O")
        else:
            avatars.append("X")
        
        self.moves_played = self.get_moves_played()
        

        self.root = Node(self.board, avatar, self.moves_played ,max_depth)

    def get_moves_played(self):
        moves_played = 0
        for rows in self.board:
            for cols in rows:
                if cols != "":
                    moves_played += 1
        return moves_played

    
