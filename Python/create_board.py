import random
from utils import *

DEBUG = 1

def incValue(board:Board, loc):
    row, col = loc
    if row < 0 or row >= board.getNumRow() or col < 0 or col >= board.getNumCol():
        return board
    
    tile = board.getTile(loc)
    tile.setValue(tile.getValue()+1)
    
    return board
    

def fillNum(board:Board, loc):
    row, col = loc
    
    if row < 0 or row >= board.getNumRow() or col < 0 or col >= board.getNumCol():
        return board
    
    # Square already visited or a bomb
    if board[row][col].getValue() != 0:
        return board
    
    board = surround(incValue, board, loc)
    
    return board




def createBoard(b, numCol, numRow):
    boardArray = [[Tile() for _ in range(numCol)] for _ in range(numRow)]

    board = Board(boardArray, (numRow, numCol), numBombs)

    numBombs = b
    bombs = []
    while b > 0:
        col = random.randint(0, numCol-1)
        row = random.randint(0, numRow-1)

        if board.getTile(row, col).isEmpty():
            b-=1
            bombs.append((row, col))
            board.getTile(row, col).setValue(-1)



        board = surround(fillNum, board, (row, col))

    return board
        
                    
                    
                

def invalidBoard(numBombs, numRows, numCol):
    if numBombs == 0:
        return True
    
    if numRows == 0:
        return True
    
    if numCol == 0:
        return True
    
    if numBombs > numRows*numCol:
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
        

def main(show_board=0):
    if DEBUG:
        board = createBoard(10, 9, 9)   ## Beginner
        # board = createBoard(40, 16, 16)               ## Intermediate
        # board = createBoard(99, 30, 16)               ## Expert
        displayMines(board)
        return board
    
    numRows, numBombs, numCol = 0, 0, 0
    while invalidBoard(numBombs, numCol, numRows):
        numRows = int(input("Enter Rows of Board: "))
        numCol = int(input("Enter Columns of Board: "))
        numBombs = int(input("Enter Number of Bombs: "))
    
    board = createBoard(numBombs, numCol, numRows)
    if show_board:
        displayMines(board)
    
    
    return board

if __name__ == "__main__":
    main(show_board=1)