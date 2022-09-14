import copy

avatars = []

class Node(object):

    def __init__(self, board, max_depth, avatar, move_to_get_here = None, depth = 0):
        self.board = board
        self.max_depth = max_depth
        self.avatar = avatar
        self.move_to_get_here = move_to_get_here
        self.depth = depth
        self.children = []
        self.value : int
        self.idx_best_child : int

        if not self.is_leaf:
            self.spread()
            if (self.depth % 2) == 0:
                self.value = -99
                for i in range(len(self.children)):
                    if self.children[i].value > self.value:
                        self.value = self.children[i].value
                        self.idx_best_child = i
            else:
                self.value = 99
                for i in range(len(self.children)):
                    if self.children[i].value < self.value:
                        self.value = self.children[i].value
                        self.idx_best_child = i    

        else:
            self.value = self.get_value()
    
    @property
    def _winning_combos(self):
        rows = [
            [(row, col) for col in range(len(self.board))]
            for row in range(len(self.board))
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    
    @property
    def moves_played(self):
        counter = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != "":
                    counter += 1
        return counter

    @property
    def max_possible_moves(self):
        return len(self.board) * len(self.board)

    @property
    def is_winner(self):
        for combo in self._winning_combos:
            results = set(self.board[n][m] for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                return True

    @property
    def is_leaf(self):
        if self.moves_played >= self.max_possible_moves or self.depth >= self.max_depth or self.is_winner:
            return True
        return False

    def spread(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == "":
                    copy_board = copy.deepcopy(self.board)
                    copy_board[i][j] = self.avatar
                    prox_move = (i,j)
                    child = Node(copy_board, self.max_depth, avatars[(self.depth + 1) % 2], prox_move, self.depth + 1)
                    self.children.append(child)
    
    def _get_possible_combos(self, avatar):
        combos = 0
        for combo in self._winning_combos:
            results = set(self.board[n][m] for n, m in combo)
            is_win = (len(results) == 1) and ("" in results)
            is_win2 = (len(results) == 2) and ("" in results) and (avatar in results)
            if is_win or is_win2:
                combos+=1
        return combos

    def combos_substraction(self):
        computer_avatar = avatars[0]
        human_avatar = avatars[1]
        computer_options = self._get_possible_combos(computer_avatar)
        human_options    = self._get_possible_combos(human_avatar)
        return computer_options - human_options

    def get_value(self):
        return self.combos_substraction()
        
class MinimaxTree(object):
    def __init__(self, board, avatar, max_depth):
        self.board = board
        self.avatar = avatar
        self.max_depth = max_depth

        avatars.clear()
        avatars.append(self.avatar)

        if self.avatar == "X":
            avatars.append("O")
        else:
            avatars.append("X")
        
        self.root = Node(self.board, self.max_depth, self.avatar)
        print("Best move: ", self.root.children[self.root.idx_best_child].move_to_get_here)