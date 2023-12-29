# Intro_to_AI_group-9-20231

Group 9
AI CHESS USING SEARCH ALGORITHMS


## chess_piece 
Python package contains the images of chess pieces.
## images 
File containing png images of button

## main.py  
The main file we will work with, contains code for the interface and get the user mouse/keyboard inputs. 

## ChessEngine.py 
This file contains all the attributes of the chess game such as:

GameState Class : has the chess board (8x8 matrix), bool variables for checkmate, stalemate, castling, en passant, pawn promotion. Moreover, it has functions to make move, undo move, get all the possible move of each chess piece. We also have the function to check if the king get checked and the function to know if a square is under attacked.

CastleRight Class : this class only contains attributes of castling

Move Class : this class contains the attributes of a move

startRow and startCol is the initial row and column before making a move

endRow and endCol is the row and column after making a move

pieceMoved return information about the piece that has been moved

pieceCaptured return information of the piece was at the row and column before the pieceMoved move to that position to take over it.

moveID is a 4 digits number that represent a move in the numerical form, which is equal to [1000 * self.startRow + 100 * self.startCol + 10 * self.endRow + self.endCol]

## AI_move.py 
This file contains all the algorithms and heuristics functions we used. All algorithms such as RandomMove, Greedy, NegaMax, NegaScout are included. If you want to change the algorithm, you can change it in the GetBestMove function (if you want to change into Greedy , you can change getNegaMaxMove(....) into getGreedyMove). The heuristics functions such as piece's value, position value , ..... are also in this file.


## How to run our files 
After import other files, you can run the main.py file to play Chess. In order to run the main.py file you must put all of those files above in the same folder.

You can choose the depth of the minimax algorithms from 1 to 6, with higher depth our AI takes very long time to return a move so we don't recommend you to do that (at depth = 6 the AI takes over 30 minutes to make a move at the mid game state)
After doing all these things you can try to play it yourself.

## git clone https://github.com/thanhbach0904/Intro_to_AI_group-9-20231

```python
install -q -r requirements.txt
```

## pip install -q -r requirements.txt



