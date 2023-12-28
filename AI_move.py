import ChessEngine
import random
gs = ChessEngine.GameState()
checkmate = 200000
stalemate = 0
maxdepth = 4
count = 0
check_count = 0
k = 0
last_move = None
last_move_count = 0
curdepth = maxdepth
endGame = False
greedy,negamax = False, True
Position = {'N' : [[10,10,10,10,10,10,10,10],
                   [10,20,20,20,20,20,20,10],
                   [10,20,30,30,30,30,20,10],
                   [10,20,30,40,40,30,20,10],
                   [10,20,30,40,40,30,20,10],
                   [10,20,30,30,30,30,20,10],
                   [10,20,20,20,20,20,20,10],
                   [10,10,10,10,10,10,10,10]],
            'B' : [[10,20,20,20,20,20,20,10],
                   [20,30,25,20,20,25,30,20],
                   [20,25,35,30,30,35,25,20],
                   [20,20,30,40,40,30,20,20],
                   [20,20,30,40,40,30,20,20],
                   [20,25,35,30,30,35,25,20],
                   [20,30,25,20,20,25,30,20],
                   [10,20,20,20,20,20,20,10]],
            'Q' : [[10,20,20,25,25,20,20,10],
                   [20,30,30,30,30,30,30,20],
                   [20,30,30,30,30,30,30,20],
                   [25,30,30,40,40,30,30,25],
                   [25,30,30,40,40,30,30,25],
                   [20,30,30,30,30,30,30,20],
                   [20,30,30,30,30,30,30,20],
                   [10,20,20,25,25,20,20,10]],
            'R' : [[10,10,10,10,10,10,10,10],
                   [ 5,10,10,10,10,10,10, 5],
                   [ 5,10,10,10,10,10,10, 5],
                   [ 5,10,10,10,10,10,10, 5],
                   [ 5,10,10,10,10,10,10, 5],
                   [ 5,10,10,10,10,10,10, 5],
                   [ 5,10,10,10,10,10,10, 5],
                   [10,10,10,10,10,10,10,10]],
            'wp': [[80,80,80,80,80,80,80,80],
                   [80,80,80,80,80,80,80,80],
                   [50,60,60,65,65,60,60,50],
                   [20,30,30,50,50,30,30,20],
                   [10,20,20,40,40,20,20,10],
                   [10,10,20,25,25,20,10,10],
                   [10,10,10, 0, 0,10,10,10],
                   [0, 0, 0, 0, 0, 0, 0, 0]],
            'bp': [[ 0, 0, 0, 0, 0, 0, 0, 0],
                   [10,10,10, 0, 0,10,10,10],
                   [10,10,20,25,25,20,10,10],
                   [10,20,20,40,40,20,20,10],
                   [20,30,30,50,50,30,30,20],
                   [50,60,60,65,65,60,60,50],
                   [80,80,80,80,80,80,80,80],
                   [80,80,80,80,80,80,80,80]],
            'wK': [[10,10,10,10,10,10,10,10],
                   [20,20,20,20,20,20,20,20],
                   [30,30,30,30,30,30,30,30],
                   [35,40,40,30,30,40,40,35],
                   [40,45,45,30,30,45,45,40],
                   [50,50,50,45,45,50,50,50],
                   [65,65,60,60,60,60,65,65],
                   [75,80,75,75,75,75,80,75]],
            'bK': [[75,80,75,75,75,75,80,75],
                   [65,65,60,60,60,60,65,65],
                   [50,50,50,45,45,50,50,50],
                   [40,45,45,30,30,45,45,40],
                   [35,40,40,30,30,40,40,35],
                   [30,30,30,30,30,30,30,30],
                   [20,20,20,20,20,20,20,20],
                   [10,10,10,10,10,10,10,10]],
            'eK': [[ 0,10,20,20,20,20,10, 0],
                   [10,30,40,40,40,40,30,10],
                   [20,40,50,50,50,50,40,20],
                   [20,40,50,50,50,50,40,20],
                   [20,40,50,50,50,50,40,20],
                   [20,40,50,50,50,50,40,20],
                   [10,30,40,40,40,40,30,10],
                   [ 0,10,20,20,20,20,10, 0]]}
def PositionPoints(piece,row,col):
        if not endGame:
            for name in Position:
                if piece == name:
                    if piece[0] == 'w':
                        return Position[name][row][col]
                    else:
                        return -Position[name][row][col]
                elif piece[1] == name:
                    if piece[0] == 'w':
                        return Position[name][row][col]
                    else:
                        return -Position[name][row][col]
        
    
        
        
        else:
                

                if piece[1] == 'p':
                    if piece[0] == 'w':#pawns
                        return Position[piece][row][col]
                    else:
                        return -Position[piece][row][col]
                elif piece[1] == 'K':#King 
                    if piece[0] == 'w':
                        return Position['eK'][row][col] + pieceAroundCount(gs.board,row,col,'w')*10
                    else:
                        return -Position['eK'][row][col] - pieceAroundCount(gs.board,row,col,'b')*10
                else:
                    return 0

def PiecePoints(Piece):
    point = {'p' : 100, 'N' : 320, 'B' : 330, 'R' : 500, 'Q' : 900, 'K' : 20000}
    
    if Piece[0] == 'w':
        return point[Piece[1]]
    elif Piece[0] == 'b':
        return -point[Piece[1]]   
def StatePoint(gs,depth):
        global piece_count,maxdepth, whiteScore,blackScore
        piece_count = 0
        whiteBishopCount = 0
        blackBishopCount = 0
        whiteScore = 0
        blackScore = 0
        
        if gs.checkmate:
            
            if not gs.whiteToMove:
                total_points = checkmate - (maxdepth-depth) *100
            else:
                 total_points = - checkmate + (maxdepth-depth)*100
            
        elif gs.stalemate:
            
             total_points = stalemate
             
        
        
        else:
            total_points = 0       

            for row in range (len(gs.board)):
                for col in range(len(gs.board[row])):
                    if gs.board[row][col] != '--':
                        if gs.board[row][col] == 'wB':
                            whiteBishopCount += 1
                        elif gs.board[row][col] == 'bB':
                            blackBishopCount += 1
                        if gs.board[row][col][1] != 'K':
                            if gs.board[row][col][0] == 'w':
                                whiteScore += PiecePoints(gs.board[row][col])
                            elif gs.board[row][col][0] == 'b':
                                blackScore -= PiecePoints(gs.board[row][col])
                        #bonus points for pawns
                        if gs.board[row][col] == 'wp':
                            if col > 0 :
                                if gs.board[row-1][col-1] == 'wp':
                                    total_points += 5
                            if col < 7 :
                                if gs.board[row-1][col+1] == 'wp':
                                    total_points += 5
                        elif gs.board[row][col] == 'bp':
                            if col > 0 :
                                if gs.board[row+1][col-1] == 'bp':
                                    total_points -= 5
                            if col < 7 :
                                if gs.board[row+1][col+1] == 'bp':
                                    total_points -= 5


                        piece_count +=1
                        total_points += float(PiecePoints(gs.board[row][col])) + PositionPoints(gs.board[row][col],row,col)
            #bonus points for 2 bishops
            if whiteBishopCount >= 2:
                total_points += 50
            elif blackBishopCount >= 2:
                total_points -= 50
        return total_points
def DisplayPiecePoints(board):
        if gs.checkmate:
            if gs.whiteToMove:
                total_points = checkmate
            else:
                 total_points = - checkmate
        elif gs.stalemate:
             total_points = stalemate
        else:
            total_points = 0       
        
            for row in range (len(board)):
                for col in range(len(board[row])):
                    if board[row][col] != '--':
                        total_points += PiecePoints(board[row][col])
        return total_points

    

def getRandomMove(Validmoves):
    if Validmoves != []:
        return Validmoves[random.randint(0,len(Validmoves)-1)]
def getGreedyMove(gs,ValidMoves):
    global nextmove
    muliplier = 1 if gs.whiteToMove else -1
    bestopponentMINMAXscore = checkmate
    
    nextmove = None
    random.shuffle(ValidMoves)
    for AImove in ValidMoves:
        gs.makeMove(AImove)
        if gs.isPawnPromotion:
            gs.undoMove()
            gs.makePromotionMove(AImove,'Q')
        opponentMoves = gs.getValidMove()
        if gs.checkmate:
                score = -checkmate * muliplier
        elif gs.stalemate:
                score = 0
        else:
            opponentMaxScore = -checkmate
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                if gs.isPawnPromotion:
                    gs.undoMove()
                    gs.makePromotionMove(opponentMove,'Q')
                if gs.checkmate:
                    score = -checkmate * muliplier
                elif gs.stalemate:
                    score = 0
                else:
                    score = -StatePoint(gs,maxdepth) * muliplier
                if  score > opponentMaxScore:
                    opponentMaxScore = score
                    
                gs.undoMove()
            
        if bestopponentMINMAXscore > opponentMaxScore:
            bestopponentMINMAXscore = opponentMaxScore
            nextmove = AImove
        gs.undoMove()
    return nextmove
def getNegaMaxMove(gs, ValidMove, depth, alpha, beta, multiplier):
    global nextmove,count,check_count,gameover,last_move,last_move_count

    count+=1
    gameover = False
    #sort valid moves
    sortedvalidMoves = []
    
    
   
    if depth != 0: #not leaf
        for move in ValidMove:
            gs.makeMove(move)
            if gs.isPawnPromotion:
                gs.undoMove()
                gs.makePromotionMove(move,'Q')
            score = StatePoint(gs,depth)
            sortedvalidMoves.append((move,score))
            gs.undoMove()
        if not gs.whiteToMove:
            sortedvalidMoves.sort(key=lambda x : x[1])
        else:
            sortedvalidMoves.sort(key=lambda x : x[1],reverse=True)
            
        
            
    if gs.inCheck():
        check_count +=1
    else:
        check_count = 0
    if check_count == 5:
        gameover = True
        gs.stalemate = True
        return 0
    else:
        if gs.checkmate or gs.stalemate:
            gameover = True
        if gameover or depth == 0:
            return multiplier*StatePoint(gs,depth)
        
        
        else:
            maxscore = - checkmate
            #consider maxdepth moves 
            for m in sortedvalidMoves:
                if depth != 0 :
                   move = m[0]
                else:
                    move = m 
                gs.makeMove(move)
                if gs.isPawnPromotion:
                    gs.undoMove()
                    gs.makePromotionMove(move,'Q')
                nextmoves = gs.getValidMove()
                score = -getNegaMaxMove(gs,nextmoves,depth - 1,-beta,-alpha, -multiplier)
                if score > maxscore:
                    maxscore = score
                    if depth == maxdepth:
                        if move == last_move and last_move_count == 3: 
                            last_move_count = 0
                        else:
                            nextmove = move
                gs.undoMove()
                # prunning
                if maxscore > alpha:
                    alpha = maxscore
                if alpha >= beta:
                    break

    return maxscore

def getNegaScoutMove(gs, ValidMove, depth, alpha, beta, multiplier):
    global nextmove,count,check_count,gameover,last_move,last_move_count

    count+=1
    gameover = False
    #sort valid moves
    sortedvalidMoves = []
    
    
   
    if depth != 0: #not leaf
        for move in ValidMove:
            gs.makeMove(move)
            if gs.isPawnPromotion:
                gs.undoMove()
                gs.makePromotionMove(move,'Q')
            score = StatePoint(gs,depth)
            sortedvalidMoves.append((move,score))
            gs.undoMove()
        if not gs.whiteToMove:
            sortedvalidMoves.sort(key=lambda x : x[1])
        else:
            sortedvalidMoves.sort(key=lambda x : x[1],reverse=True)
            
    if gs.inCheck():
        check_count +=1
    else:
        check_count = 0
    if check_count == 5:
        gameover = True
        gs.stalemate = True
        return 0
    else:
        if gs.checkmate or gs.stalemate:
            gameover = True
        if depth == 0 or gameover:
            return multiplier*StatePoint(gs,depth)
        else:
            maxscore = - checkmate
            #consider maxdepth moves
            for i in range (len(sortedvalidMoves)): 
                move = sortedvalidMoves[i][0]
                gs.makeMove(move)
                if gs.isPawnPromotion:
                    gs.undoMove()
                    gs.makePromotionMove(move,'Q')
                nextmoves = gs.getValidMove()
                if i == 0 :
                    score = -getNegaScoutMove(gs,nextmoves,depth - 1,-beta,-alpha, -multiplier)
                else:
                    score = -getNegaScoutMove(gs,nextmoves,depth - 1,-alpha-1,-alpha, -multiplier) #null window
                    if alpha < score < beta:
                        score = -getNegaScoutMove(gs,nextmoves,depth - 1,-beta,-alpha, -multiplier) #fail high ->  do normal negamax search

                if score > maxscore:
                    maxscore = score
                    if depth == maxdepth:
                        if move == last_move and last_move_count == 3: 
                            last_move_count = 0
                        else:
                            nextmove = move
                gs.undoMove()
                # prunning
                if maxscore > alpha:
                    alpha = maxscore
                if alpha >= beta:
                    break

    return alpha
 
def pieceAroundCount(board,row,col,color):
    pieceAround = 0
    if 0 < row < 7 and 0 < col <7:
        for i in range(row-1,row+2):
            for j in range(col-1,col+2):
                if board[i][j][0] == color:
                    pieceAround+=1
        return pieceAround - 1
    elif 0 < row < 7:
        if col == 7:
            for i in range(row-1,row+2):
                for j in range(col-1,col+1):
                    if board[i][j][0] == color:
                        pieceAround+=1
        elif col == 0:
            for i in range(row-1,row+2):
                for j in range(col,col+2):
                    if board[i][j][0] == color:
                        pieceAround+=1
        return pieceAround - 1
    elif 0 < col < 7:
        if row == 7:
            for i in range(row-1,row+1):
                for j in range(col-1,col+2):
                    if board[i][j][0] == color:
                        pieceAround+=1
        elif row == 0:
            for i in range(row,row+2):
                for j in range(col-1,col+2):
                    if board[i][j][0] == color:
                        pieceAround+=1
        return pieceAround - 1
    else:
        if (row,col) == (0,7):
            for i in range(row,row+2):
                for j in range(col-1,col+1):
                    if board[i][j][0] == color:
                        pieceAround+=1
        elif (row,col) == (0,0):
            for i in range(row,row+2):
                for j in range(col,col+2):
                    if board[i][j][0] == color:
                        pieceAround+=1
        elif (row,col) == (7,7):
            for i in range(row-1,row+1):
                for j in range(col-1,col+1):
                    if board[i][j][0] == color:
                        pieceAround+=1
        elif (row,col) == (7,0):
            for i in range(row-1,row+1):
                for j in range(col,col+2):
                    if board[i][j][0] == color:
                        pieceAround+=1
        return pieceAround - 1
        

def getBestMove(gs, ValidMove):
    global nextmove,count,maxdepth,endGame,piece_count,k,last_move,last_move_count,count_store,whiteScore,blackScore
    nextmove = None
    
    print('-----------------------------------')
    if greedy:
        getGreedyMove(gs,ValidMove)
        
    elif negamax:
        getNegaMaxMove(gs,ValidMove,maxdepth,-checkmate,checkmate,1 if gs.whiteToMove else -1)
        
    
    #adapt maxdepth
    print('Nodes: ' + str(count))
    count_store = count
    p = StatePoint(gs,maxdepth)
    if whiteScore <= 1500 or blackScore <= 1500:
        endGame = True
    
    if last_move == nextmove:
        last_move_count += 1
    if  k % 2 ==0:
        last_move = nextmove
    count=0 
    k += 1

    
    
    count=0

    return nextmove

    
    
    