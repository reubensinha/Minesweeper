import random

DEBUG = 1

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
    def __init__(self, board:list[list[Tile]], size:tuple[int, int], numBombs:int, locBomb:list[int]):
        self.board = board
        self.size = size
        self.numBombs = numBombs
        self.locBomb = locBomb
    
    openedTiles = 0
    numFlags = 0
    lose = False
            
    
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
        if self.lose:
            return True
        if self.openedTiles == (self.getNumTiles() - self.numBombs):
            return True
        if self.numFlags == self.numBombs:
            return all(self.getTile(bomb).isFlag() for bomb in self.locBomb)
        else:
            return False
    
    def getLose(self):
        return self.lose()
    
    def setLose(self):
        self.lose = True
                
        

def fillNum(row, col, board:list[list[Tile]], size):
    # Indexes of truthArrray
    #   0   1   2
    #   3   x   4
    #   5   6   7
    if DEBUG:
        print(f"Row: {row}\nCol: {col}\nsize: {size}")
    
    ## Square already visited or a bomb
    if board[row][col].getValue() != 0:
        return board
    
    count = 0
    numCol, numRow = size
    truthArray = [True]*8
    
    if col == 0:
        truthArray[0] = False
        truthArray[3] = False
        truthArray[5] = False
    
    if row == 0:
        truthArray[0] = False
        truthArray[1] = False
        truthArray[2] = False
    
    if col == numCol-1:
        truthArray[2] = False
        truthArray[4] = False
        truthArray[7] = False
    
    if row == numRow-1:
        truthArray[5] = False
        truthArray[6] = False
        truthArray[7] = False
        
        
    ## Top-Left Corner
    if truthArray[0]:
        if board[row-1][col-1].isBomb():
            count+=1
        
    ## Top edge
    if truthArray[1]:
        if board[row-1][col].isBomb():
            count+=1
        
    ## Top-Right Corner
    if truthArray[2]:
        if board[row-1][col+1].isBomb():
            count+=1
        
    ## Right Edge
    if truthArray[4]:
        if board[row][col+1].isBomb():
            count+=1
        
    ## Bottom-Right Corner
    if truthArray[7]:
        if board[row+1][col+1].isBomb():
            count+=1
        
    ## Bottom Edge
    if truthArray[6]:
        if board[row+1][col].isBomb():
            count+=1
        
    ## Bottom-Left Corner
    if truthArray[5]:
        if board[row+1][col-1].isBomb():
            count+=1
    
    ## Left Edge
    if truthArray[3]:
        if board[row][col-1].isBomb():
            count+=1
    
    
    board[row][col].setValue(count)
    
    return board




def createBoard(b, numCol, numRow):
    size = (numCol, numRow)
    board = [[Tile() for i in range(numCol)] for j in range(numRow)]
    
    # if DEBUG:
    #     print("\nEmpty Board:")
    #     print(board)
    numBombs = b
    bombs = []
    while b > 0:
        col = random.randint(0, numCol-1)
        row = random.randint(0, numRow-1)
        
        if board[row][col].isEmpty():
            b-=1
            bombs.append((row, col))
            board[row][col].setValue(-1)
    
    
    # Indexes of truthArrray
    #   0   1   2
    #   3   x   4
    #   5   6   7
    for i, bomb in enumerate(bombs):
        truthArray = [True]*8
        row, col = bomb
    
        if col == 0:
            truthArray[0] = False
            truthArray[3] = False
            truthArray[5] = False
        
        if row == 0:
            truthArray[0] = False
            truthArray[1] = False
            truthArray[2] = False
        
        if col == numCol-1:
            truthArray[2] = False
            truthArray[4] = False
            truthArray[7] = False
        
        if row == numRow-1:
            truthArray[5] = False
            truthArray[6] = False
            truthArray[7] = False
        
        ## Top-Left Corner
        if truthArray[0]:
            board = fillNum(row-1, col-1, board, size)
        ## Top edge
        if truthArray[1]:
            board = fillNum(row-1, col, board, size)
        ## Top-Right Corner
        if truthArray[2]:
            board = fillNum(row-1, col+1, board, size)
        ## Right Edge
        if truthArray[4]:
            board = fillNum(row, col+1, board, size)
        ## Bottom-Right Corner
        if truthArray[7]:
            board = fillNum(row+1, col+1, board, size)
        ## Bottom Edge
        if truthArray[6]:
            board = fillNum(row+1, col, board, size)
        ## Bottom-Left Corner
        if truthArray[5]:
            board = fillNum(row+1, col-1, board, size)
        ## Left Edge
        if truthArray[3]:
            board = fillNum(row, col-1, board, size)
        
    return Board(board, (numRow, numCol), numBombs, bombs)
        
                    
                    
                

def invalidBoard(b, n, m):
    if b == 0:
        return True
    
    if n == 0:
        return True
    
    if m == 0:
        return True
    
    if b > n*m:
        return True
    
    return False


def displayMines(board:Board):
    for i, row in enumerate(board.getBoard()):
        if i==0:
            print("\n" + "+---"*(len(row)-1) + "+---+", sep="")
        for j, col in enumerate(row):
            if j == 0:
                print("|", end="")
            if col.isBomb():
                print(" x |", end="")
            elif col.isEmpty():
                print("   |", end="")
            else:
                print(f" {col.getValue()} |", end="")
                
        print("\n" + "+---"*(len(row)-1) + "+---+", sep="")
        

def main(mine=0):
    if DEBUG:
        board = createBoard(10, 9, 9) ## Beginner
        # board = createBoard(40, 16, 16) ## Intermediate
        # board = createBoard(99, 30, 16) ## Expert
        displayMines(board)
        return board
    
    b, n, m = 0, 0, 0
    while invalidBoard(b, n, m):
        m = int(input("Enter Rows of Board: "))
        n = int(input("Enter Columns of Board: "))
        b = int(input("Enter Number of Bombs: "))
    
    board = createBoard(b, n, m)
    if mine:
        displayMines(board)
    
    
    return board

if __name__ == "__main__":
    main(mine=1)