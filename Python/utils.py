class Tile:
    _value = 0
    _opened = False
    _flag = False
        
    def getValue(self):
        return self._value
    
    def isOpened(self):
        return self._opened
    
    def setValue(self, value):
        self._value = value
    
    def open(self):
        self._opened = True
    
    def toggleFlag(self):
        self._flag = not self._flag
    
    def isBomb(self):
        return self._value == -1
    
    def isEmpty(self):
        return self._value == 0
    
    def isFlag(self):
        return self._flag
    
    def reset(self):
        self._flag = False
        self._opened = False



class Board:
    def __init__(self, board:list[list[Tile]], size:tuple[int, int], numBombs:int):
        self._board = board
        self._size = size
        self._numBombs = numBombs
    
    _openedTiles = 0
    _numFlags = 0
    _lose = False
            
    
    def getSize(self):
        return self._size
    
    def getNumRow(self):
        return self._size[0]
    
    def getNumCol(self):
        return self._size[1]
    
    def getBoard(self):
        return self._board
    
    def getNumBombs(self):
        return self._numBombs
    
    def getOpenedTiles(self):
        return self._openedTiles
    
    def getNumTiles(self):
        return self._size[0] * self._size[1]

    def getTile(self, loc) -> Tile:
        row, col = loc
        return self._board[row][col]
    
    def incOpenedTiles(self):
        self._openedTiles += 1
    
    def isComplete(self):
        if self._lose:
            return True
        if self._openedTiles == (self.getNumTiles() - self._numBombs):
            return True
        if self._numFlags == self._numBombs:
            return all(self.getTile(bomb).isFlag() for bomb in self._locBomb)
        else:
            return False
    
    def getLose(self):
        return self._lose()
    
    def setLose(self):
        self._lose = True
        
    def incFlag(self):
        self._numFlags += 1
    
    def decFlag(self):
        self._numFlags -= 1
        
        

def surround(func, board, loc):
    row, col = loc
    
    board = func(board, (row-1, col-1)) # Top-Left Corner
    board = func(board, (row-1, col))   # Top edge
    board = func(board, (row-1, col+1)) # Top-Right Corner
    board = func(board, (row, col-1))   # Left Edge
    board = func(board, (row, col+1))   # Right Edge
    board = func(board, (row+1, col-1)) # Bottom-Left Corner
    board = func(board, (row+1, col))   # Bottom Edge
    board = func(board, (row+1, col+1)) # Bottom-Right Corner
    
    return board