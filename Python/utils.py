class Tile:
    __value = 0
    __opened = False
    __flag = False
        
    def getValue(self):
        return self.__value
    
    def getOpened(self):
        return self.__opened
    
    def setValue(self, value):
        self.__value = value
    
    def open(self):
        self.__opened = True
    
    def toggleFlag(self):
        self.__flag = not self.__flag
    
    def isBomb(self):
        return self.__value == -1
    
    def isEmpty(self):
        return self.__value == 0
    
    def isFlag(self):
        return self.__flag
    
    def reset(self):
        self.__flag = False
        self.__opened = False



class Board:
    def __init__(self, board:list[list[Tile]], size:tuple[int, int], numBombs:int, locBomb:int):
        self.board = board
        self.size = size
        self.numBombs = numBombs
        self.locBomb = locBomb
    
    openedTiles = 0
    numFlags = 0
    lose = 0
            
    
    def getSize(self):
        return self.size
    
    def getNumRow(self):
        return self.size[0]
    
    def getNumCol(self):
        return self.size[1]
    
    def getBoard(self):
        return self.board
    
    def getNumBombs(self):
        return self.numBombs
    
    def getOpenedTiles(self):
        return self.openedTiles
    
    def getNumTiles(self):
        return self.size[0] * self.size[1]

    def getTile(self, loc) -> Tile:
        row, col = loc
        return self.board[row][col]
    
    def incOpenedTiles(self):
        self.openedTiles += 1
    
    def isComplete(self):
        if self.lose():
            return True
        if self.openedTiles == (self.numTiles - self.numBombs):
            return True
        if self.numFlags == self.numBombs:
            return all(self.getTile(bomb).isFlag() for bomb in self.locBomb)
        else:
            return False
    
    def getLose(self):
        return self.lose()
    
    def setLose(self):
        self.lose = 1

def surround(func, game, loc):
    row, col = loc
    
    game = func(game, (row-1, col))
    game = func(game, (row-1, col+1))
    game = func(game, (row-1, col-1))
    game = func(game, (row, col+1))
    game = func(game, (row, col-1))
    game = func(game, (row+1, col+1))
    game = func(game, (row+1, col))
    game = func(game, (row+1, col-1))
    
    return game