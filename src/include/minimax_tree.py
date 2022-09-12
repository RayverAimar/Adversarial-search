
from multiprocessing.sharedctypes import Value
from include.utils import Move

avatars = []

class Node(object):

    def __init__(self, board : list, avatar, max_depth, moves_played, depth = 0):
        self.children = []
        self.board = board
        self.depth = depth
        self.avatar = avatar
        self.moves_played = moves_played
        self.move : tuple
        self.value : int
        self._winning_combos = self._get_winning_combos()
        self.winning_combo = self._get_actual_combos()
        self.max_moves_played = len(self.board)*len(self.board)

        #See if the board has already a winning combo, then return its value and the position of its best child

        if (depth < max_depth) and (self.moves_played < self.max_moves_played ) and (not self.winning_combo):
            self.spread()

        #See the child with most-least value and return its moved position
        


    def get_node_value(self):
        value : int

        if(self.winning_combo):
            value = self.max_moves_played + (self.max_moves_played - self.moves_played)
            if self.depth % 2:
                return value
            else:
                return value * -1
    
        ##Aritmetica combos player - combos computer
        

    def _get_winning_combos(self):
        rows = [
            [(row, col) for col in len(self.board)]
            for row in len(self.board)
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
        
    def _get_actual_combos(self):
        combos = 0
        for combo in self._winning_combos:
            results = set(self.board[n][m] for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results) and (self.avatar in results)
            if is_win:
                combos+=1

        return combos
    
    

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

    
