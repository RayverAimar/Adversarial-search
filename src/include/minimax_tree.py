
avatars = []

class Node(object):

    def __init__(self, board : list, avatar, max_depth, depth = 0):
        self.children = []
        self.board = board
        self.depth = depth
        self.avatar = avatar
        if depth <= max_depth:
            self.spread()
    
    
    def spread(self):
        for row in len(self.board):
            for col in len(row):
                if self.board[row][col] == "":
                    copy = self.board
                    copy[row][col] = self.avatar
                    child = Node(copy, avatars[(self.depth+1)%2], depth=self.depth+1)
                    self.children.append(child)
    
    def draw(self):
        for rows in self.value:
            for cols in rows:
                print(cols, end = " ")
            print()

class MinimaxTree(object):

    def __init__(self, board, avatar, max_depth):
        self.root = Node(board, avatar, max_depth)
        self.avatar = avatar
        self.max_depth = max_depth
        avatars = []
        avatars.append(self.avatar)
        if self.avatar == "X":
            avatars.append("O")
        else:
            avatars.append("X")

    def spread(self):
        pass

    
