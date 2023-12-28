import pygame as p
import ChessEngine
import AI_move
import sys
W,H = 512,512 #the width and height of the board
dim = 8 #8x8 chessboard
sq_size = W//dim
images = {} #the images of each chess piece
moveLog = []
button = {}
def LoadImages():
    
    pieces = ["bp","bB",'bK','bQ','bR','bN','wp','wB','wK','wQ','wR','wN']
    buttonList = ['Play','Choose Algorithm','Quit','button1']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("chess_piece/" + piece +'.png'),(sq_size,sq_size))
    
    for b in buttonList:
        button[b] = p.image.load('image/button.jpg').convert()
    



def main():
    p.init()
    screen = p.display.set_mode((W+4*sq_size,H))
    global gameover
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()

    #generate all valid moves at the beginning
    ValidMoves = gs.getValidMove()
    moveMade = False #at first no valid move is made
    #load the images from the package, do once before while loop
    LoadImages()
    #running is the status of the game
    running = True
    gameover = False
    sqSelected = ()
    #at the beginning no square is selected so the tuple is empty
    #the tuple keep track of the last click into a square of the user 
    playerClicks = []
    
    AI = False
    whiteCheckcount = 0
    blackCheckcount = 0
    colorCheck = None
    total_time = 0
    AI_count = 0
    data = []
    players = False
    
    p.display.set_caption('Chess')
    
    while running: #display menu
        
        displayStartMenu(screen)
        
        complete = False
        event = p.event.get()
        for i in event:
            if i.type == p.MOUSEBUTTONDOWN:
                
                x, y = i.pos
                if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x, y):
                    complete = True
                
                elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x, y):
                    
                    while running: 
                        chooseAlgorithm(screen)
        
        
                        complete1 = False
                        event = p.event.get()
                        
                        for click in event:
                            if click.type == p.MOUSEBUTTONDOWN:
                                x1, y1 = click.pos
                                if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x1,y1):
                                    complete1 = True
                                    AI_move.greedy = True
                                    AI_move.negamax = False
                                elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x1,y1):
                                    complete1 = True
                                    AI_move.negamax = True
                                    AI_move.greedy = False
                        if complete1:
                            break
                    
                    
                elif button['Quit'].get_rect(center=(6*sq_size,float(6.5*sq_size))).collidepoint(x, y):
                    sys.exit()
                    
                    
                    
                    
        if complete:
            break
        
    
    
     # display starting screen
    while running: # check what color player choose
        displayStart(screen)
        
        
        complete = False
        event = p.event.get()
        for i in event:
            if i.type == p.MOUSEBUTTONDOWN:
                
                x, y = i.pos
                if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x, y):
                    complete = True
                    humanPlayer = True
                    AIPlayer = False
                
                elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x, y):
                    complete = True
                    humanPlayer = False
                    AIPlayer = True
                    
                    
                    
                elif button['Quit'].get_rect(center=(6*sq_size,float(6.5*sq_size))).collidepoint(x, y):
                    complete = True
                    humanPlayer = True
                    AIPlayer = True
                    players = True
        if complete:
            break
    
    while (not players) and AI_move.negamax: #choose depth
        chooseDepth(screen)
        
        
        complete = False
        event = p.event.get()
        for i in event:
            if i.type == p.MOUSEBUTTONDOWN:
                
                x, y = i.pos
                if button['Play'].get_rect(center=(4*sq_size,float(2.5*sq_size))).collidepoint(x, y):
                    complete = True
                    AI_move.maxdepth = 1
                
                elif button['Choose Algorithm'].get_rect(center=(4*sq_size,float(4.5*sq_size))).collidepoint(x, y):
                    complete = True
                    AI_move.maxdepth = 2
                    
                    
                elif button['Quit'].get_rect(center=(7*sq_size,float(2.5*sq_size))).collidepoint(x, y):
                    complete = True
                    AI_move.maxdepth = 3
                elif button['button1'].get_rect(center=(7*sq_size,float(4.5*sq_size))).collidepoint(x, y):
                    complete = True
                    AI_move.maxdepth = 4
        if complete:
            break
    
    drawGamestate(screen,gs, ValidMoves, sqSelected,moveLog) #draw board in case white is AI since it take a long time to do first move and screen stuck in starting screen
    p.display.flip()
    while running:
      
        
        humanTurn = (humanPlayer and gs.whiteToMove) or (not gs.whiteToMove and AIPlayer)
        

        if gs.stalemate or gs.checkmate: #check if game over
            gameover = True
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanTurn and not gameover:
                    
                    mouse_pos = p.mouse.get_pos() #get the (x,y) coordinate of the mouse cursor 
                    col = mouse_pos[0]//sq_size #determine the position of the square that user's mouse pointed 
                    row = mouse_pos[1]//sq_size
                    if sqSelected == (row,col): #click on the same square twice
                        sqSelected = ()
                        playerClicks = [] #reset the click
                    #must consider the case when 1st click is on a empty square
                    elif col >= 8 and gs.isPawnPromotion == False:
                        sqSelected = ()
                        playerClicks = []
                    elif len(playerClicks) > 3:
                        playerClicks = []
                        sqSelected = ()
                    
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    #promotion
                    if len(playerClicks) == 3 and gs.isPawnPromotion == True:
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board) #check if player clicks are valid
                        temp = [playerClicks[0],playerClicks[1]]
                        if playerClicks[2][0] == 7:
                            if playerClicks[2][1] == 8:
                                gs.makePromotionMove(move,'Q')
                                playerClicks = []
                                moveMade = True
                                moveLog.append(move.getMovements())
                            elif playerClicks[2][1] == 9:
                                gs.makePromotionMove(move,'R')
                                playerClicks = []
                                moveMade = True
                                moveLog.append(move.getMovements())
                            elif playerClicks[2][1] == 10:
                                gs.makePromotionMove(move,'B')
                                playerClicks = []
                                moveMade = True
                                moveLog.append(move.getMovements())
                            elif playerClicks[2][1] == 11:
                                gs.makePromotionMove(move,'N')
                                playerClicks = []
                                moveMade = True
                                moveLog.append(move.getMovements())
                            else:
                                
                                playerClicks = temp
                                sqSelected = ()
                            
                        else:
                            playerClicks = temp
                            sqSelected = ()
                    if len(playerClicks) == 2 and gs.isPawnPromotion == False: #after make 2 clicks that are valid
                            
                            
                            move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                            
                            if move.isPawnPromotion and ((gs.whiteToMove == True if move.pieceMoved[0] == 'w' else False ) or (gs.whiteToMove == False if move.pieceMoved[0] == 'b' else False )):
                                gs.isPawnPromotion = True
                                
                                
                            else:
                                gs.isPawnPromotion = False
                                for i in range(len(ValidMoves)):
                                    if move == ValidMoves[i]:
                                        gs.makeMove(ValidMoves[i])
                                        if gs.inCheck():
                                            if gs.whiteToMove:
                                                whiteCheckcount += 1
                                            else:
                                                blackCheckcount += 1
                                        else:
                                            if gs.whiteToMove:
                                                whiteCheckcount = 0
                                            else:
                                                blackCheckcount = 0
                                    
                                        moveMade = True
                                    
                                        moveLog.append(move.getMovements())
                                    sqSelected = ()
                                    playerClicks = []
                        
                                sqSelected = ()
                                playerClicks = []
                
            elif e.type == p.KEYDOWN: #undo move
                if e.key == p.K_z: #choose z as the undo button
                    if AI: #if opponent is AI then undo 2 times
                        for i in range (2):
                            gs.undoMove()

                            if moveLog != []:
                                moveLog.pop()
                            gs.stalemate,gs.checkmate = False,False
                        moveMade = True
                        playerClicks = []
                        sqSelected = ()
                        gameover = False
                        
                    else: #human player just need 1 undo
                        gs.undoMove()
                        

                        if moveLog != []:
                            moveLog.pop()
                        
                        moveMade = True
                        playerClicks = []
                        sqSelected = ()
                        gameover = False
                        gs.stalemate,gs.checkmate = False,False
        

        if (not humanTurn) and (not gameover):
            
            start_time = p.time.get_ticks()
            AI = True #save for undoMove
            displayIsThinking(screen)
            AImove = AI_move.getBestMove(gs,ValidMoves)
            if AImove is None:
                AImove = AI_move.getRandomMove(ValidMoves)
            gs.makeMove(AImove)
            
            if gs.isPawnPromotion:
                gs.undoMove()
                gs.makePromotionMove(AImove,'Q')
            if gs.inCheck():
                if gs.whiteToMove:
                    whiteCheckcount += 1
                    colorCheck = True
                else:
                    blackCheckcount += 1
                    colorCheck = False
            else:
                if gs.whiteToMove:
                    whiteCheckcount = 0
                    colorCheck = None
                else:
                    blackCheckcount = 0
                    colorCheck = None
                                    
            end_time = p.time.get_ticks()

            print('Time: ' + str((end_time-start_time)/1000) + ' seconds') # get time process
            AI_count += 1
            total_time += (end_time-start_time)/1000
            moveLog.append(AImove.getMovements())
            moveMade = True
            if AI_count != 0:
                print('Average time: ' + str(float(total_time/AI_count)))
            data.append(((end_time-start_time)/1000,AI_move.count_store))
            print(data)
        if moveMade:
            #after a valid move is made
            #reset
            ValidMoves = gs.getValidMove()
            moveMade = False
        if colorCheck != None:
            if( whiteCheckcount == 5 and not colorCheck) or (blackCheckcount == 5 and colorCheck):
                gs.stalemate = True
        
        drawGamestate(screen,gs, ValidMoves, sqSelected,moveLog)
        p.display.flip()
def DisplayMoveLog(screen,gs,moveLog): #display previous move, score and win condition
        
        surface = p.Surface((4*sq_size,8*sq_size))
        surface.fill(p.Color('Blue'))
        screen.blit(surface, (8*sq_size,0))
        font = p.font.SysFont(None, 24)
        bigfont = p.font.SysFont(None, 48)
        #display movelog
       
        limitMoveLog = 5
        displayMoveLog = bigfont.render('LAST MOVE',True,'white')
        screen.blit(displayMoveLog,(10*sq_size-95,int(0.166*8*sq_size)))
        displayscore = bigfont.render('SCORE',True,'white')
        screen.blit(displayscore,(10*sq_size-60,int(0.05*8*sq_size)))
        if moveLog!=[]:
                
                curMoveLog = []
                if len(moveLog) >= limitMoveLog:
                    for i in range (limitMoveLog):
                        curMoveLog.append(moveLog[-1-i])
                    for i in range (limitMoveLog):
                        if gs.whiteToMove:
                            img = font.render((('Black' if (i%2 == 0) else 'White')+': '+str(curMoveLog[i])) , True, 'white')
                            screen.blit(img, (10*sq_size-75, int(0.244*8*sq_size + 0.049*8*sq_size*i)))
                        else:
                            img = font.render((('Black' if (i%2 == 1) else 'White')+': '+str(curMoveLog[i])) , True, 'white')
                            screen.blit(img, (10*sq_size-75, int(0.244*8*sq_size + 0.049*8*sq_size*i)))
                else:
                    for i in range (len(moveLog)):
                        if gs.whiteToMove:
                            img = font.render((('Black' if (i%2 == 0) else 'White')+': '+str(moveLog[-1-i])) , True, 'white')
                            screen.blit(img, (10*sq_size-75, int(0.244*8*sq_size + 0.049*8*sq_size*i)))
                        else:
                            img = font.render((('Black' if (i%2 == 1) else 'White')+': '+str(moveLog[-1-i])) , True, 'white')
                            screen.blit(img, (10*sq_size-75, int(0.244*8*sq_size + 0.049*8*sq_size*i)))
        #display points
                
        score = font.render(('White:'+str(AI_move.DisplayPiecePoints(gs.board))) if (AI_move.DisplayPiecePoints(gs.board)>=0) else ('Black:'+str(-AI_move.DisplayPiecePoints(gs.board))), True, 'white')
        screen.blit(score,(10*sq_size-35,int(0.117*8*sq_size)))
        #display win, draw state
        if gs.checkmate == True:
            
            font = p.font.SysFont(None, 48)
            win = font.render(('BLACK' if gs.whiteToMove else 'WHITE')+' WIN', True, 'white')
            screen.blit(win,(10*sq_size-90,int(0.586*8*sq_size)))
        elif gs.stalemate == True:
            
            font = p.font.SysFont(None, 48)
            win = font.render('DRAW', True, 'white')
            screen.blit(win,(10*sq_size-50,int(0.586*8*sq_size)))
        
        

    
def HighLightSq(screen, gs, ValidMoves, sqSelected):

    if sqSelected != () and sqSelected[1]<8:
        r, c = sqSelected
        #highlight selected piece
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            surface = p.Surface((sq_size,sq_size))
            surface.set_alpha(150)
            surface.fill(p.Color('blue'))
            screen.blit(surface, (c*sq_size,r*sq_size))
            #highlight valid move
            surface.fill(p.Color('yellow'))
            if ValidMoves != None:
                for move in ValidMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(surface, (move.endCol*sq_size,move.endRow*sq_size))
    #red highlight if incheck
    if gs.inCheck():
        surface = p.Surface((sq_size,sq_size))
        surface.set_alpha(150)
        surface.fill(p.Color('red'))
        if gs.whiteToMove:
            screen.blit(surface,(gs.whiteKingPos[1]*sq_size,gs.whiteKingPos[0]*sq_size))
        else:
            screen.blit(surface,(gs.blackKingPos[1]*sq_size,gs.blackKingPos[0]*sq_size))

def drawGamestate(screen,gs, ValidMoves, sqSelected, moveLog):
    drawboard(screen)
    HighLightSq(screen, gs, ValidMoves, sqSelected)
    
    
    DisplayMoveLog(screen,gs,moveLog)
    drawpiece(screen,gs.board,gs)

def drawboard(screen):
    #paint the squares on the chess board with colors
    #can change the color into the color we want if we have the rgb code to that color
    colors = [p.Color("white"),p.Color("dark gray")]
    for r in range(dim):
        for c in range(dim):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
def drawpiece(screen,board,gs):
    #draw the piece in the board
    #there is a small problem that the resolution of the chess piece images are not too good
    #can be solved by some high resolution chess pieces
    for r in range(dim):
        for c in range(dim):
            if board[r][c] != "--": #if the element at row r column c is not empty space
                screen.blit(images[board[r][c]],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))
    if gs.isPawnPromotion:
        possiblePromotion = ['Q','R','B','N']
        if gs.whiteToMove:
            for i in range (len(possiblePromotion)):
                screen.blit(images['w' + possiblePromotion[i]],p.Rect((8+i)*sq_size,7*sq_size,sq_size,sq_size))
        else:
            for i in range (len(possiblePromotion)):
                screen.blit(images['b' + possiblePromotion[i]],p.Rect((8+i)*sq_size,7*sq_size,sq_size,sq_size))
def displayStartMenu(screen):
    color,color1,color2 = 'white','white','white'
    screen.fill('brown')
    screen.blit(p.transform.scale(button['Play'],(4*sq_size,sq_size)),(4*sq_size,2*sq_size))
    button['Play'] = p.transform.scale(button['Play'],(4*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Choose Algorithm'],(5*sq_size,sq_size)),(3.5*sq_size,4*sq_size))
    button['Choose Algorithm'] = p.transform.scale(button['Choose Algorithm'],(5*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Quit'],(4*sq_size,sq_size)),(4*sq_size,6*sq_size))
    button['Quit'] = p.transform.scale(button['Quit'],(4*sq_size,sq_size))
    bigfont = p.font.SysFont(None, int(0.75*sq_size))
    welcome = bigfont.render('Welcome to our chess game', True, 'white')
    mouse_pos = p.mouse.get_pos()
    x, y = mouse_pos[0],mouse_pos[1]
    if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x, y):
        color = 'Blue'
    elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x, y):
        color1 = 'blue'
    elif button['Quit'].get_rect(center=(6*sq_size,float(6.5*sq_size))).collidepoint(x, y):
        color2 = 'blue'
    
     
    text = bigfont.render('Play', True, color)
    text1 = bigfont.render('Select Algorithm', True, color1)
    text2 = bigfont.render('Quit', True, color2)
    screen.blit(welcome,(2.5*sq_size,0.5*sq_size))
    screen.blit(text,(5.5*sq_size,2.2*sq_size))
    screen.blit(text1,(3.9*sq_size,4.2*sq_size))
    screen.blit(text2,(5.4*sq_size,6.2*sq_size))
    p.display.flip()
def chooseAlgorithm(screen):
    color,color1 = 'white', 'white'
    screen.fill('brown')
    screen.blit(p.transform.scale(button['Play'],(4*sq_size,sq_size)),(4*sq_size,2*sq_size))
    button['Play'] = p.transform.scale(button['Play'],(4*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Choose Algorithm'],(5*sq_size,sq_size)),(3.5*sq_size,4*sq_size))
    button['Choose Algorithm'] = p.transform.scale(button['Choose Algorithm'],(5*sq_size,sq_size))
    
    bigfont = p.font.SysFont(None, 48)
    mouse_pos = p.mouse.get_pos()
    x, y = mouse_pos[0],mouse_pos[1]
    if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x, y):
        color = 'Blue'
    elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x, y):
        color1 = 'blue'
    
    welcome = bigfont.render('Choose Algorithm', True, 'white')
    text = bigfont.render('Greedy', True, color)
    text1 = bigfont.render('Negamax', True, color1)
    
    screen.blit(welcome,(3.8*sq_size,0.5*sq_size))
    screen.blit(text,(5.1*sq_size,2.2*sq_size))
    screen.blit(text1,(4.8*sq_size,4.2*sq_size))
    
    p.display.flip()
def displayStart(screen):
    color,color1,color2 = 'white','white','white'
    screen.fill('brown')
    screen.blit(p.transform.scale(button['Play'],(4*sq_size,sq_size)),(4*sq_size,2*sq_size))
    button['Play'] = p.transform.scale(button['Play'],(4*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Choose Algorithm'],(4*sq_size,sq_size)),(4*sq_size,4*sq_size))
    button['Choose Algorithm'] = p.transform.scale(button['Choose Algorithm'],(5*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Quit'],(4*sq_size,sq_size)),(4*sq_size,6*sq_size))
    button['Quit'] = p.transform.scale(button['Quit'],(4*sq_size,sq_size))
    bigfont = p.font.SysFont(None, int(0.75*sq_size))
    welcome = bigfont.render('Choose your color', True, 'white')
    mouse_pos = p.mouse.get_pos()
    x, y = mouse_pos[0],mouse_pos[1]
    if button['Play'].get_rect(center=(6*sq_size,float(2.5*sq_size))).collidepoint(x, y):
        color = 'Blue'
    elif button['Choose Algorithm'].get_rect(center=(6*sq_size,float(4.5*sq_size))).collidepoint(x, y):
        color1 = 'blue'
    elif button['Quit'].get_rect(center=(6*sq_size,float(6.5*sq_size))).collidepoint(x, y):
        color2 = 'blue'
    
     
    text = bigfont.render('White', True, color)
    text1 = bigfont.render('Black', True, color1)
    text2 = bigfont.render('2 Players', True, color2)
    screen.blit(welcome,(3.6*sq_size,0.5*sq_size))
    screen.blit(text,(5.3*sq_size,2.2*sq_size))
    screen.blit(text1,(5.3*sq_size,4.2*sq_size))
    screen.blit(text2,(4.9*sq_size,6.2*sq_size))
    p.display.flip()
    
def chooseDepth(screen):
    color,color1,color2,color3 = 'white','white','white','white'
    screen.fill('brown')
    screen.blit(p.transform.scale(button['Play'],(2*sq_size,sq_size)),(3*sq_size,2*sq_size))
    button['Play'] = p.transform.scale(button['Play'],(2*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Choose Algorithm'],(2*sq_size,sq_size)),(3*sq_size,4*sq_size))
    button['Choose Algorithm'] = p.transform.scale(button['Choose Algorithm'],(2*sq_size,sq_size))
    screen.blit(p.transform.scale(button['Quit'],(2*sq_size,sq_size)),(6*sq_size,2*sq_size))
    button['Quit'] = p.transform.scale(button['Quit'],(2*sq_size,sq_size))
    screen.blit(p.transform.scale(button['button1'],(2*sq_size,sq_size)),(6*sq_size,4*sq_size))
    button['button1'] = p.transform.scale(button['button1'],(2*sq_size,sq_size))
    bigfont = p.font.SysFont(None, int(0.75*sq_size))
    welcome = bigfont.render('Choose depth', True, 'white')
    mouse_pos = p.mouse.get_pos()
    x, y = mouse_pos[0],mouse_pos[1]
    if button['Play'].get_rect(center=(4*sq_size,float(2.5*sq_size))).collidepoint(x, y):
        color = 'Blue'
    elif button['Choose Algorithm'].get_rect(center=(4*sq_size,float(4.5*sq_size))).collidepoint(x, y):
        color1 = 'blue'
    elif button['Quit'].get_rect(center=(7*sq_size,float(2.5*sq_size))).collidepoint(x, y):
        color2 = 'blue'
    elif button['button1'].get_rect(center=(7*sq_size,float(4.5*sq_size))).collidepoint(x, y):
        color3 = 'blue'
    
     
    text = bigfont.render('1', True, color)
    text1 = bigfont.render('2', True, color1)
    text2 = bigfont.render('3', True, color2)
    text3 = bigfont.render('4', True, color3)
    screen.blit(welcome,(3.6*sq_size,0.5*sq_size))
    screen.blit(text,(3.7*sq_size,2.2*sq_size))
    screen.blit(text1,(3.7*sq_size,4.2*sq_size))
    screen.blit(text2,(6.7*sq_size,2.2*sq_size))
    screen.blit(text3,(6.7*sq_size,4.2*sq_size))
    p.display.flip()
def displayIsThinking(screen):
    bigfont = p.font.SysFont(None, 32)
    
       
    
    displayAiIsThinking = bigfont.render('AI IS THINKING...',True,'white')
    screen.blit(displayAiIsThinking,(10*sq_size-95,int(0.605*8*sq_size)))
    p.display.flip()



if __name__ == "__main__":
    main()