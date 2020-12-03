
import random
import sys

#Grid dimensions
numNormCol = 7
numAdvCol = 9
numRow = 6

#Tokens
player = "  O  "
bot = "  X  "

print("Let's play Connect Four!")

# Function for choosing difficulty.
def decideDifficulty():
    print("Choose a difficulty. 'Normal' or 'Advanced' mode? (type 'quit' to quit game.)")
    while True:
        difficulty = input()
        if difficulty.lower().startswith("qu") and difficulty.lower().endswith("it"):
            sys.exit()
        elif difficulty.lower().startswith("nor") and difficulty.lower().endswith("mal"):
            difficulty = numNormCol
            return difficulty
        elif difficulty.lower().startswith("adv") and difficulty.lower().endswith("ced"):
            difficulty = numAdvCol
            return difficulty
        else:
            print("Error. Could not recognise command.")
            continue

#Function for making 2D list.
def tokenSlot(diffCol):
    slot = []
    for x in range(diffCol):
        slot.append(["     "]*numRow)
    return slot

#Draw the first row of the grid.
def drawFirst(diffCol):
    line=""
    for x in range(1,diffCol+1):
        line+="+--" + str(x) + "--"
    line+="+"
    print(line)

#Draw the +-----+ of the grid.
def drawDivider(diffCol):
    line=""
    for x in range (diffCol):
        line+="+-----"
    line+="+"
    print(line)

#Draws the gaps and inserts elements from list into 2nd gap. Calls the drawDivider() function after 3 gap-rows are made.
def drawGap(slot, diffCol):
    for y in range(numRow):
        print("|     "*diffCol + "|")
        for x in range(diffCol):
            print("|{}".format(slot[x][y]),end="")
        print("|")
        print("|     "*diffCol + "|")
        drawDivider(diffCol)

#Draws the whole grid.
def drawGrid(slot, diffCol):
    drawFirst(diffCol)
    drawGap(slot, diffCol)



#Determines how the bot makes its move.
def botMove(slot, diffCol):
    while True:
        move = random.randint(1, diffCol)
        move-=1
        if validateMove(slot, move, diffCol):
            return move
        else:
            continue

#Asks the player for their input and uses the validate function to check if their input is a valid move.
def playerMove(slot, diffCol):
    while True:
        move = str(input("Choose a column to place 'O' token in (type 'quit' to quit game.)"))
        if move.lower().startswith("qu") and move.lower().endswith("it"):
            sys.exit()
        elif not move.isdigit():
            print("Error. Could not recognise command. Please try again.")
            continue
        move = int(move)-1
        if validateMove(slot, move, diffCol):
            return move
        else:
            continue

#Validates whether the move is valid, e.g. column 8 is not available in normal mode or the column is full.
def validateMove(slot, move, diffCol):
    if move >= diffCol or move < 0:
        print("The column you chose ({}) does not exist on the grid. Please choose a column between 1 and {}.".format(move+1, diffCol))
        return False
    if not slot[move][0] == "     ":
        print("Column full.")
        return False
    return True

#Checks and places a token in a blank element of the chosen column.
def placeToken(slot, col, token):
    for y in range(numRow-1,-1,-1):
        if slot[col][y] == "     ":
            slot[col][y] = token
            return


#Checks if there are tokens in a row to determine a winner depending on difficulty.
def winCondition(slot, token, diffCol):
    if diffCol == 7:
        #check rows
        for y in range(numRow):
            for x in range(diffCol-3):
                if slot[x][y] == token and slot [x+1][y] == token and slot[x+2][y] == token and slot[x+3][y] == token:
                    return True
        #check columns
        for x in range(diffCol):
            for y in range(numRow-3):
                if slot[x][y] == token and slot[x][y+1] == token and slot[x][y+2] == token and slot[x][y+3] == token:
                    return True
        #check left diagonal
        for y in range(numRow-3):
            for x in range(diffCol-3):
                if slot[x][y] == token and slot[x+1][y+1]== token and slot[x+2][y+2] == token and slot[x+3][y+3] == token:
                    return True
        #check right diagonal
        for y in range(3, numRow):
            for x in range(diffCol-3):
                if slot[x][y] == token and slot[x+1][y-1] == token and slot[x+2][y-2] == token and slot[x+3][y-3] == token:
                    return True
    elif diffCol == 9:
        #check rows
        for y in range(numRow):
            for x in range(diffCol-4):
                if slot[x][y] == token and slot [x+1][y] == token and slot[x+2][y] == token and slot[x+3][y] == token and slot[x+4][y]== token:
                    return True
        #check columns
        for x in range(diffCol):
            for y in range(numRow-4):
                if slot[x][y] == token and slot[x][y+1] == token and slot[x][y+2] == token and slot[x][y+3] == token and slot[x][y+4] == token:
                    return True
        #check left diagonal
        for y in range(numRow-4):
            for x in range(diffCol-4):
                if slot[x][y] == token and slot[x+1][y+1]== token and slot[x+2][y+2] == token and slot[x+3][y+3] and slot[x+4][y+4] == token:
                    return True
        #check right diagonal
        for y in range(4,numRow):
            for x in range(diffCol-4):
                if slot[x][y] == token and slot[x+1][y-1] == token and slot[x+2][y-2] == token and slot[x+3][y-3] == token and slot[x+4][y-4] == token:
                    return True
    return False

#Chooses who to go first.
def firstTurn():
    print("Choosing who goes first...")
    turn = random.randint(1,2)
    if turn == 1:
        print("Player goes first!")
        return "player"
    else:
        print("Bot goes first!")
        return "bot"

#Checks whether the grid is full.
def gridFull(slot, diffCol):
    for x in range(diffCol):
        for y in range(numRow):
            if slot[x][y] == "     ":
                return False
    return True


#Function that calls all other functions and uses its own written code to make a complete, playable game.
def playGame():
    while True:
        attempt = 1
        diffCol = decideDifficulty()
        turn = firstTurn()
        grid = tokenSlot(diffCol)
        while True:
            if turn == "player":
                drawGrid(grid, diffCol)
                move = playerMove(grid, diffCol)
                placeToken(grid, move, player)
                if winCondition(grid, player, diffCol):
                    winner = "player"
                    break
                turn = "bot"
                attempt+=1
            elif turn == "bot":
                drawGrid(grid, diffCol)
                print("Bot's turn.")
                move = botMove(grid, diffCol)
                placeToken(grid, move, bot)
                if winCondition(grid, bot, diffCol):
                    winner = "bot"
                    break
                turn = "player"

            elif gridFull(grid, diffCol):
                winner = "draw"
                break

        #Evaluation message
        if attempt < 10:
            evaluation = "You have the talent!"
        elif attempt < 15:
            evaluation = "Not too bad."
        else:
            evaluation = "You could do better."

        #Determine winner and print message
        message = "This round took you {} attempts. {}".format(attempt, evaluation)
        if winner == "player":
            drawGrid(grid, diffCol)
            print("You win!")
            print(message)
        if winner == "bot":
            drawGrid(grid, diffCol)
            print("Bot wins! You made {} moves. Better luck next time.".format(attempt))
        if winner == "draw":
            drawGrid(grid, diffCol)
            print("It's a draw!")






playGame()

