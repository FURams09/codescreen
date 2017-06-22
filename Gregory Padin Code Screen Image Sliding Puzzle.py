"""
Gregory Padin Code Screen
02/08/2015

Image Sliding Puzzle

Make an image sliding puzzle playable via console. 
The game looks like this (ignore all the fancy sliding around): http://mypuzzle.org/sliding. 
The game is that you have an n x n grid of scrambled numbers with one spot free. 
On the console, you input the number in which to move and it moves the piece. 
The game is solved when all numbers are in order. Here is example output. 
The $> line is console input from the user playing the game. 
Think about extensibility when you design the game.

8 2 1
3 4 5
6 7 _
$> 5

8 2 1
3 4 _
6 7 5
$> 4

8 2 1
3 _ 4
6 7 5



To play the game call the Play function, passing it the size of n you want the game board.

I made the game itself a class so it could either be played in the console with startGame, or used in another
program to have the game function with a different interface, or in conjunction with making a solving program.
It would also give another developer the ability to easily create a specific custom starting board.
"""
def Play(size):
    try:
        sb= SlidingBoard(size)
        sb.startGame()
    except SizeError:
        newSize = raw_input("That was not a valid entry. Please enter a number greater than 1: ")
        Play(newSize)
    

 
class SlidingBoard:
    from random import shuffle, randint
    
    def startGame(self):
        #Play the Game through the console. 
        self.randomizeBoard()
        print('Enter \'X\' to quit.')
        self.userMove()
    
    def userMove(self):
        #Handles getting an input from the user and then starts the next move once completed.
        self.displayBoard()
        nextMove = raw_input('Tile to fill empty space: ')
        #By making X the next move, you can exit the game.
        if nextMove == 'X':
            return
        try:
            if self.move(int(nextMove)):
                if self.isSorted():
                    print("Congratulations you won!")
                    return
            else:
                self.displayInvalidEntry()
        except ValueError:
            self.displayInvalidEntry()
        #Recursively call userMove until the solution is found. 
        self.userMove()
            
    def move(self, tryMove):
        #Take the input value and checks that the move is legal.
        #Then swaps the blank space with the input if it is.
        #It will return True to indicate a valid move was made, or False for an invalid input. 
        if self.isAboveBlank(tryMove):
            self.gameBoard[self.blankCell], self.gameBoard[self.blankCell - self.size] = self.gameBoard[self.blankCell - self.size], self.gameBoard[self.blankCell] 
            self.blankCell = self.blankCell - self.size
            return True
        elif self.isBelowBlank(tryMove):
            self.gameBoard[self.blankCell], self.gameBoard[self.blankCell + self.size] = self.gameBoard[self.blankCell + self.size], self.gameBoard[self.blankCell]
            self.blankCell = self.blankCell + self.size
            return True
        elif self.isLeftOfBlank(tryMove):
            self.gameBoard[self.blankCell], self.gameBoard[self.blankCell - 1] = self.gameBoard[self.blankCell - 1], self.gameBoard[self.blankCell]
            self.blankCell = self.blankCell - 1
            return True
        elif self.isRightOfBlank(tryMove):
            self.gameBoard[self.blankCell], self.gameBoard[self.blankCell + 1] = self.gameBoard[self.blankCell + 1], self.gameBoard[self.blankCell]
            self.blankCell = self.blankCell + 1
            return True
        else:
            return False
            
            
    #Randomize and validate the game board
    #
    #
    #Decided to not do any difficulty checking.
    #This could be used to check for a minimum number of swapped pairs. 
    #Right now it just makes sure you don't get the original puzzle back.
    def randomizeBoard(self):
        self.shuffle(self.gameBoard)        
        #Set the number of Inverted Pairs to the self.invertedPairs object
        self.countInvertedPairs()
        
        if self.size%2 == 1:
            #odd sized puzzles need an even number of swapped cells
            if self.invertedPairs %2 == 1:
                self.swapFirstPair()
        else:
            #check if the blank cell is on an even numbered row, counting up from the bottom
            if (self.size -(self.blankCell/self.size)) % 2 == 0: 
                if self.invertedPairs %2 == 0: #Make sure there is an odd number of inverted pairs, if not swap one more. 
                    self.swapFirstPair()
            else:
                if self.invertedPairs % 2 == 1: #Make sure there's an evne number of inverted pairs, if not swap one.
                    self.swapFirstPair()
        if self.invertedPairs == 0: 
            self.randomizeBoard()

    #Used to find the number of inverted pairs in the puzzle. This is necessary for validating the puzzle.
    #
    #Set the new value for the blank cell's position, once it's found. If it's in the last cell it won't be found
    #But the blankCell will already be set to the last position by default. 
    #
    #
    #Since for my version of the game the count of pairs doesn't need to be updated throughout the game I decided
    #Against tracking the number of swapped pairs as the moves were being made, thought a function could easily be
    #written at a later date to do that if necessary.   
    def countInvertedPairs(self):
        self.invertedPairs = 0
        for i in range(len(self.gameBoard) -1):
            if self.gameBoard[i] == self.blankIcon:
                self.blankCell = i
            else:
                for j in range(i+1, len(self.gameBoard)):
                    if self.gameBoard[j] != self.blankIcon:
                        if self.gameBoard[i] > self.gameBoard[j]:
                            self.invertedPairs += 1
    #This will swap two adjacent numbers to give us the correct numbers of inverted pairs for the size of the grid.  
    def swapFirstPair(self):
        #use the 3rd and 4th tiles if the blank is in either the first two spaces.
        if self.blankCell <= 1:
            i = 2;
        else:
            i = 0
        self.gameBoard[i], self.gameBoard[i+1] = self.gameBoard[i+1], self.gameBoard[i]
        #Update's the inverted pairs count based on whether an inversion was created or a pair ordered.
        #even though the console game won't require it to be accurate anymore. Would be useful if a running count was ever added.
        if self.gameBoard[i] > self.gameBoard[i+1]:
            self.invertedPairs += 1
        else:
            self.invertedPairs -= 1
    

    #Prints the current board state to the console
    #Formatted to be a uniform width'd tile based on the size of the board's largest value.    
    def displayBoard(self):
        print('')
        for i in range(0, self.size):
            print(reduce(lambda x, y: str(x).ljust(self.padding) + '|' + str(y).ljust(self.padding),self.gameBoard[i*self.size:i*self.size+self.size]))            
    
    
    #Generic error message to display with an invalid entry.
    def displayInvalidEntry(self):
        print('That entry is invalid')
    
    #Check if the game is in it's final position. 
    def isSorted(self):
        return self.gameBoard == self.finishedBoard

    #These methods check and see if swapping the above, below, left, or right relative to the blank cell is a legal move
    #and if so check if that cell's value is the attempted move.  
    def isAboveBlank(self, tryValue):
        if self.blankCell >= self.size and self.gameBoard[self.blankCell - self.size] == tryValue:      
            return True
        else:
            return False   
    def isBelowBlank(self, tryValue):
        if (self.blankCell < self.size**2-self.size) and self.gameBoard[self.blankCell + self.size] == tryValue:
            return True
        else:
            return False      
    def isLeftOfBlank(self, tryValue):
        if self.blankCell % self.size != 0 and self.gameBoard[self.blankCell - 1] == tryValue:
            return True
        else:
            return False   
    def isRightOfBlank(self, tryValue):
        if self.blankCell % self.size != self.size-1 and self.gameBoard[self.blankCell + 1] == tryValue:
            return True
        else:
            return False      
    #Change the character used to represent the blank square
    #Will assume the self.blankCell is up to date. 
    def updateIcon(self, newIcon):
        if newIcon not in self.gameBoard:
            self.blankIcon = newIcon
            self.gameBoard[self.blankCell] = newIcon
            self.finishedBoard[self.size**2-1] = newIcon
    #Makes sure the size is a valid number before setting the instance variables. 
    def __init__(self, size):
        try:
            self.size = int(size)
            if self.size <= 1:
                raise SizeError('Size Must Be Greater Than 1')
        except ValueError:
            raise SizeError('Size Must Be A Number')

        #Set the board to be in order
        self.gameBoard = range(1, (self.size**2))
        self.gameBoard.append('_')
        self.blankIcon = '_' #Could be changed via the Update Icon method.         
        self.finishedBoard = self.gameBoard[:] #Store the final order so that we can do a comparison after a move.
        self.padding = len(str(self.size**2)) #Make sure every cell is the same width, equal to the size of the longest number. Is only designed for a game board with numeric values. 
        self.blankCell = self.size**2 - 1 #Keep track of where the empty space is
        self.invertedPairs = 0


#Custom error class to handle an invalid size. 
class SizeError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)