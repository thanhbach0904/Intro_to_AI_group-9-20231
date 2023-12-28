class GameState():
    def __init__(self):
        #"--" represent the blank space
        #b and w represent black and white piece, the capital letter behind them represent:
        #R : Rook, N: Knight, Q : Queen , K : King, B : Bishop , p : pawn
        self.board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["wp","wp","wp","wp","wp","wp","wp","wp"],
                      ["wR","wN","wB","wQ","wK","wB","wN","wR"]]

        #this allow the white player move first
        self.whiteToMove = True
        #this list stores the movements of both players             
        self.moveLog = []
        self.moveFunction = {'p' : self.getPawnMoves,'R' : self.getRookMoves,
                              'N' : self.getKnightMoves,'B' : self.getBishopMoves, 
                              'Q' : self.getQueenMoves, "K" : self.getKingMoves}
        self.whiteKingPos = (7,4)
        self.blackKingPos = (0,4)
        self.checkmate = False #bool variables to check if the gamestate is check mate or stalemate
        self.stalemate = False
        self.enPassantPossible = () #position of the possible en passant move
        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.Castle = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        self.isPawnPromotion = False
        self.checkTurn = None
        self.check_count = 0
        
    def makePromotionMove(self,move,promotion):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved #the first try i used "==" instead of '=' XD
        self.moveLog.append(move) #save the moves so that we can undo it 
        self.whiteToMove = not self.whiteToMove #swap player
        

        self.isPawnPromotion = False
        
        if move.pieceMoved == "wK":
            self.whiteKingPos = (move.endRow,move.endCol) #update the white king position
        elif move.pieceMoved == "bK":
            self.blackKingPos = (move.endRow,move.endCol)
        #pawn promotion
        if move.isPawnPromotion:
            if self.whiteToMove:
                self.board[move.endRow][move.endCol] = 'b' + promotion #because after making the promotion move its the opponent's move 
                
            else:
                self.board[move.endRow][move.endCol] = 'w' + promotion
                
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved 
        self.moveLog.append(move) #save the moves so that we can undo it 
        self.whiteToMove = not self.whiteToMove #swap player
        self.isPawnPromotion = False
        if move.pieceMoved == "wK":
            self.whiteKingPos = (move.endRow,move.endCol) #update the white king position
        elif move.pieceMoved == "bK":
            self.blackKingPos = (move.endRow,move.endCol)
        #pawn promotion
        if move.isPawnPromotion:
            if self.whiteToMove:
                self.board[move.endRow][move.endCol] = 'bQ' #because after making the promotion move its the opponent's move 
                
            else:
                self.board[move.endRow][move.endCol] = 'wQ'
        
        #en passant 
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "--" #capturing the pawn
        #update enpassantpossible variable
        if move.pieceMoved[1] == "p" and abs(move.endRow - move.startRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()
        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:#kingside
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]#move rook
                self.board[move.endRow][move.endCol+1] = '--'
            else:#queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]#move rook
                self.board[move.endRow][move.endCol-2] = '--'


        #upadte castling right
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))
        
    def updateCastleRights(self,move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
            
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left white rook
                    self.currentCastlingRight.wqs = False

                elif move.startCol == 7: #right white rook
                   
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'wR':
             if move.endRow == 7:
                if move.endCol == 0: #left white rook
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7: #right white rook
                    
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left black rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right black rook
                    self.currentCastlingRight.bks = False
                    
        elif move.pieceCaptured == 'bR':
             if move.endRow == 7:
                if move.endCol == 0: #left white rook
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7: #right white rook
                    self.currentCastlingRight.bks = False
                    

            

    

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingPos = (move.startRow,move.startCol) #reset the position of white king 
            elif move.pieceMoved == "bK":
                self.blackKingPos = (move.startRow,move.startCol)
            #undo Enpassant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow,move.endCol)
            if move.pieceMoved[1] == "p" and abs(move.endRow - move.startRow) == 2:
                self.enPassantPossible = ()
            #undo castling right
            
            self.currentCastlingRight = self.castleRightsLog[-1]#last move
            self.castleRightsLog.pop()
            self.Castle = self.castleRightsLog[-1]
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:#kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]#move rook
                    self.board[move.endRow][move.endCol-1] = '--'
                else:#queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]#move rook
                    self.board[move.endRow][move.endCol+1] = '--'
            
            
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #focus on white pawns
            if r > 0:
                if self.board[r-1][c] == "--": #the square ahead of the pawn is empty
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c] == '--': #its the first move of a white pawn
                        moves.append(Move((r,c),(r-2,c),self.board))
                if c-1 >= 0:
                    if self.board[r-1][c-1][0] == "b": #if there's an opponent in front of white pawn
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                    elif (r-1,c-1) == self.enPassantPossible:
                        moves.append(Move((r,c),(r-1,c-1),self.board,isEnPassantMove=True))
                if c+1 <= 7:
                    if self.board[r-1][c+1][0] == "b":
                        moves.append(Move((r,c),(r-1,c+1),self.board))
                    elif (r-1,c+1) == self.enPassantPossible:
                        moves.append(Move((r,c),(r-1,c+1),self.board,isEnPassantMove=True))
        else: #black's turn 
            if r  < 7:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),self.board))
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == "w":
                        moves.append(Move((r,c),(r+1,c-1),self.board))
                    elif (r+1,c-1) == self.enPassantPossible:
                        moves.append(Move((r,c),(r+1,c-1),self.board,isEnPassantMove=True))
                if c+1 <= 7:
                    if self.board[r+1][c+1][0] == "w":
                        moves.append(Move((r,c),(r+1,c+1),self.board))
                    elif (r+1,c+1) == self.enPassantPossible:
                        moves.append(Move((r,c),(r+1,c+1),self.board,isEnPassantMove=True))

    def getRookMoves(self,r,c,moves):
        #check in 4 directions, if the square has the same color of the rook, then it cant attack it
        for c1 in range(c+1,8):
            if self.board[r][c1][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r][c1] == "--":
                moves.append(Move((r,c),(r,c1),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r,c1),self.board))
                break
        for c2 in range(c-1,-1,-1): #check from column c-1 to 0
            if self.board[r][c2][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r][c2] == "--":
                moves.append(Move((r,c),(r,c2),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r,c2),self.board))
                break
        for r1 in range(r+1,8):
            if self.board[r1][c][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r1][c] == "--":
                moves.append(Move((r,c),(r1,c),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r1,c),self.board))
                break
        for r2 in range(r-1,-1,-1):
            if self.board[r2][c][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r2][c] == "--":
                moves.append(Move((r,c),(r2,c),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r2,c),self.board))
                break
        #change the code later
    def getKnightMoves(self,r,c,moves):
        #knight has 8 possible moves ,if the square has the same color of the knight, then it cant attack it
        if r+2 <= 7:
            if c+1 <= 7 and self.board[r][c][0] != self.board[r+2][c+1][0]:
                moves.append(Move((r,c),(r+2,c+1),self.board))
            if c-1 >= 0 and self.board[r][c][0] != self.board[r+2][c-1][0]:
                moves.append(Move((r,c),(r+2,c-1),self.board))
        if r-2 >= 0:
            if c+1 <= 7 and self.board[r][c][0] != self.board[r-2][c+1][0]:
                moves.append(Move((r,c),(r-2,c+1),self.board))
            if c-1 >= 0  and self.board[r][c][0] != self.board[r-2][c-1][0]:
                moves.append(Move((r,c),(r-2,c-1),self.board))
        if c+2 <= 7:
            if r+1 <= 7 and self.board[r][c][0] != self.board[r+1][c+2][0]:
                moves.append(Move((r,c),(r+1,c+2),self.board))
            if r-1 >= 0 and self.board[r][c][0] != self.board[r-1][c+2][0]:
                moves.append(Move((r,c),(r-1,c+2),self.board))
        if c-2 >= 0:
            if r+1 <= 7 and self.board[r][c][0] != self.board[r+1][c-2][0]:
                moves.append(Move((r,c),(r+1,c-2),self.board))
            if r-1 >= 0 and self.board[r][c][0] != self.board[r-1][c-2][0]:
                moves.append(Move((r,c),(r-1,c-2),self.board))
        #change the code later
    def getQueenMoves(self,r,c,moves):
        #queen has all the possibilities of rook and bishop
        #diagonals
        dir = [(1,1),(1,-1),(-1,1),(-1,-1)]
        
        for d in dir:
            r1,c1  = r,c
            while 0 <= r1 + d[0] <=7 and 0 <= c1 + d[1] <= 7:
                r1 += d[0]
                c1 += d[1]
                piece = self.board[r1][c1]
                if piece == "--":
                    moves.append(Move((r,c),(r1,c1),self.board))
                elif piece[0] != self.board[r][c][0]:
                    moves.append(Move((r,c),(r1,c1),self.board))
                    break
                else:
                    break
        #straight
        for c1 in range(c+1,8):
            if self.board[r][c1][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r][c1] == "--":
                moves.append(Move((r,c),(r,c1),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r,c1),self.board))
                break
        for c2 in range(c-1,-1,-1): #check from column c-1 to 0
            if self.board[r][c2][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r][c2] == "--":
                moves.append(Move((r,c),(r,c2),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r,c2),self.board))
                break
        for r1 in range(r+1,8):
            if self.board[r1][c][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r1][c] == "--":
                moves.append(Move((r,c),(r1,c),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r1,c),self.board))
                break
        for r2 in range(r-1,-1,-1):
            if self.board[r2][c][0] == self.board[r][c][0]: #the same color
                break
            elif self.board[r2][c] == "--":
                moves.append(Move((r,c),(r2,c),self.board))
            else: #the square in the way has different color
                moves.append(Move((r,c),(r2,c),self.board))
                break
    def getBishopMoves(self,r,c,moves):
        #check diagonals
        dir = [(1,1),(1,-1),(-1,1),(-1,-1)]
        
        for d in dir:
            r1,c1  = r,c
            while 0 <= r1 + d[0] <=7 and 0 <= c1 + d[1] <= 7:
                r1 += d[0]
                c1 += d[1]
                piece = self.board[r1][c1]
                if piece == "--":
                    moves.append(Move((r,c),(r1,c1),self.board))
                elif piece[0] != self.board[r][c][0]:
                    moves.append(Move((r,c),(r1,c1),self.board))
                    break
                else:
                    break
    def getKingMoves(self,r,c,moves):
        #king can move to any square nearby within 1 square
        #the first 4 is straight direction, the other 4 is diagonal
        all_direction = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for direction in all_direction:
            r1,c1 = r + direction[0] , c + direction[1]
            if (0 <= r1 <= 7 and 0 <= c1 <= 7) and (self.board[r1][c1][0] != self.board[r][c][0]):
                moves.append(Move((r,c),(r1,c1),self.board))
        


    def getCastleMove(self,r,c,moves):
        if self.square_under_attack(r,c):
            return
        if (self.whiteToMove and self.Castle.wks) or (not self.whiteToMove and self.Castle.bks):
            self.getKingSideCastleMove(r,c,moves)
        if (self.whiteToMove and self.Castle.wqs) or (not self.whiteToMove and self.Castle.bqs):
            self.getQueenSideCastleMove(r,c,moves)
    def getKingSideCastleMove(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.square_under_attack(r,c+1) and not self.square_under_attack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove = True))
    def getQueenSideCastleMove(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.square_under_attack(r,c-1) and not self.square_under_attack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove = True))

    def getValidMove(self):
        
        #generate all possible move
        tempEnpassantPossible = self.enPassantPossible
        tempCastleRight = CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMove()
        if self.whiteToMove:
            self.getCastleMove(self.whiteKingPos[0],self.whiteKingPos[1],moves)
        else:
            self.getCastleMove(self.blackKingPos[0],self.blackKingPos[1],moves)
        #since all the moves is different from each other, we can use remove() function to delete the move that is invalid
        #for each move, make the move
        for i in range(len(moves)-1,-1,-1): #start from the end of the list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        
        #check if checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate , self.stalemate = False,False
        self.enPassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRight
        return moves
    def getAllPossibleMove(self):
        self.piece_count = 0
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '--':
                    self.piece_count += 1
                turn = self.board[r][c][0] #check if the piece at row r column c is white or black or empty
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves) #call the function base on the piece type
        

        return moves
    def inCheck(self):
        if self.whiteToMove:
            return self.square_under_attack(self.whiteKingPos[0],self.whiteKingPos[1]) 
                
        else:
            return self.square_under_attack(self.blackKingPos[0],self.blackKingPos[1]) 
                
    def square_under_attack(self,r,c):
        self.whiteToMove = not self.whiteToMove #swap turn to make the opponent's moves
        opponentMove = self.getAllPossibleMove()
        self.whiteToMove = not self.whiteToMove #swap back
        for move in opponentMove:
            if move.endRow == r and move.endCol == c: # the square is under attack
                
                return True
        return False 
class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
class Move():
    rankToRows = {"1" : 7,"2" : 6,"3": 5 ,"4" : 4,"5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowstoRank = {v:k for k,v in rankToRows.items()}
    fileToCols = {'a' : 0,'b' : 1,'c' : 2,'d' : 3,'e' : 4,'f' : 5,'g' : 6,'h' :7}
    colstofile = {v:k for k,v in fileToCols.items()}
    
    def __init__(self,startSq,endSq,board,isEnPassantMove = False, isCastleMove = False): #startSq and endSq are tuples
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] 
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        self.isCaptureMove = False
        if board[self.endRow][self.endCol] != '--':
            self.isCaptureMove = True
        self.piece = { 'p': 'Pawn', 'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King' }
        
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        self.PromotionType = ["Q","R","B","N"] #list all the possible promotion for later
        #en passant
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        #Castle
        self.isCastleMove = isCastleMove
        #create a 4 digits ID for each move
        self.moveID = 1000 * self.startRow + 100 * self.startCol + 10 * self.endRow + self.endCol
        
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getMovements(self):
        
        return self.piece[self.pieceMoved[1]] + ' ' + self.getPosition(self.startRow,self.startCol) + " to " + self.getPosition(self.endRow,self.endCol) 
    def getPosition(self,r,c): # get the position of the chess piece such as b7,a1,....
        return self.colstofile[c] + self.rowstoRank[r]