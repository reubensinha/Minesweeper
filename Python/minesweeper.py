import create_board
from utils import *

DEBUG = 0

def displayBoard(game:"create_board.Board"):
    for i, row in enumerate(game.getBoard()):
        if i==0:
            print("\n" + "+---"*(len(row)-1) + "+---+", sep="")
        for j, col in enumerate(row):
            if j == 0:
                print("|", end="")
            
            if col.isFlag():
                print(" F |", end="") 
            elif not col.getOpened():
                print(" O |", end="")
            elif col.getOpened():
                if col.isBomb():
                    print(" x |", end="")
                elif col.isEmpty():
                    print("   |", end="")
                else:
                    print(f" {col.getValue()} |", end="")
            else:
                print("E")
                
        print("\n" + "+---"*(len(row)-1) + "+---+", sep="")


def play_turn(game:create_board.Board):
    # TODO Placeholder
    notInt = True
    wrongArgNum = True
    while notInt or wrongArgNum:
        coord = input("Enter action Coords as [O/F row col]: ").split()
        if len(coord) == 3:
            wrongArgNum = False
            action, row, col = coord
            if action != "O" and action != "F":
                wrongArgNum = True
                print("Not Valid Action")
            try:
                row = int(row)
                col = int(col)
            except ValueError:
                print("Enter 2 integers in form [row col]")
            else:
                notInt = False
        else:
            print("Wrong num arguments")
            
    return action, (row, col)


def revealTile(game:create_board.Board, loc):
    row, col = loc
    if row < 0 or row >= game.getNumRow() or col < 0 or col >= game.getNumCol():
        return game
    
    if game.getTile(loc).getOpened():
        return game
    
    game.incOpenedTiles()
    game.getTile(loc).open()
    if not game.getTile(loc).isEmpty():
        # TODO cleanup
        return game
    
    # game = revealTile(game, (row-1, col-1))
    # game = revealTile(game, (row-1, col))
    # game = revealTile(game, (row-1, col+1))
    # game = revealTile(game, (row, col+1))
    # game = revealTile(game, (row, col-1))
    # game = revealTile(game, (row+1, col+1))
    # game = revealTile(game, (row+1, col))
    # game = revealTile(game, (row+1, col-1))
    game = surround(revealTile, game, loc)
    
    return game


def nextMove(game:create_board.Board):
    print("Next Turn")
    action, loc = play_turn(game)
    tile = game.getTile(loc)

    # Check if already opened
    if tile.getOpened():
        # Do nothing
        return game

    # Check if Bomb -> Set lose to 1 -> Reveal board
    if action == "O" and tile.isBomb():
        game.setLose()
        return game

    if action == "O":
        if tile.isFlag():
            ## Do nothing
            return game
        game = revealTile(game, loc)
        return game

    if action == "F":
        if tile.isFlag():
            game.numFlags -= 1
        else:
            game.numFlags += 1
        tile.toggleFlag()
        return game


def endGame(game:create_board.Board):
    # TODO
    create_board.displayMines(game)
    if game.lose:
        print("You Lose")
    else:
        print("You Win!")

def main():
    complete = False
    game = create_board.main()
    while not complete:
        displayBoard(game)
        game = nextMove(game)
        if DEBUG:
            print(f"lose = {game.lose}")
            print(f"isComplete = {game.isComplete()}")
        complete = game.isComplete()
    endGame(game)


if __name__ == "__main__":
    main()