import random,pygame,sys, time
from pygame.locals import *

FPS = 25
ww = 640
wh = 480
dimen = 20
bw = 10
bh = 20
sideways = 0.2
down = 0.1

period = '.'
margin = (ww-bw*dimen)
sidemargin = margin/2; # want uniform space on either sides of the borders
topmargin = wh-bh*dimen
topmargin = topmargin/2
# using major colors to color the background
white = (255,255,255)
gray = (185,185,185)
black = (0,0,0)
red = (155,0,0)
green = (0,155,0)
blue = (0,0,155)
yellow = (155,155,0)
colors = (red,blue,green,yellow)

fontcolor = black;
BORDERCOLOR = black
TEXTCOLOR = black
BGCOLOR= white # background color

width = 5
height = 5
mDown = False
mLeft = False
mRight = False
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}
lastMoveDownTime = time.time()
lastMoveSidewaysTime = time.time()
lastFallTime = time.time()

class gameplay:
    def __init__(self,board):
        self.board = []
    def getNewPiece(self):
        nextShape = random.choice(list(PIECES.keys()))
        newPiece = {'shape': nextShape,
                    'rotation': random.randint(0,len(PIECES[nextShape])-1),
                    'x': int(bw/2) - int(width/2),
                    'y': -2,
                    'color': random.randint(0,len(colors)-1)}
        return newPiece
    def getNewBoard(self):
        board=[]
        for i in range(bw):
            board.append([period]*bh)
        return board
    def checkRowFull(self,board,y):
        for i in range(bw):
            if(board[x][y]==period):
                return False
        return True
    def checkRowEmpty(self,board):
        numRemoved = 0
        y = bh
        assert y==bh
        y = bh-1 #since we have to start at the bottomm of the board
        limit1 = 0
        limitr = -1
        while y>=0:
            if checkRowFull(board,y):
                for removeone in range(y,limit1,limitr):
                    for x in range(bw):
                        board[x][removeone] = board[x][removeone-1]
                    for x in range(bw):
                        board[x][0]=period
                    numRemoved+=1
            else:
                y= y-1 #continue to check next row
            return numRemoved
        #def updateScore():

class board(gameplay):
    def __init__(self,piece):
        self.piece = piece
        gameplay.__init__(self,board)
    def checkPiecePos(self,board12,adjX=0, adjY=0):
        self.board12 = board12
        for x in range(width):
            for y in range(height):
                aboveMe = y + self.piece['y']+adjY <0
                if aboveMe or PIECES[self.piece['shape']][self.piece['rotation']][y][x] == period:
                    continue
                lm = x+self.piece['x'] + adjX
                no= y+self.piece['y']+adjY
                if not lm>=0 and lm<bw and no<bh:
                    return False
                if self.board12[lm][no]!=period:
                    return False
        return True

class block(gameplay):
    def __init__(self,fallingPiece):
        self.fallingPiece = fallingPiece
        gameplay.__init__(self,board)
    def rotate(self,board):
        self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(PIECES[self.fallingPiece['shape']])

    def moveLeft(self):
        self.fallingPiece['x'] -=1
        mLeft = True
        mRight = False
        lastMoveSidewaysTime = time.time()
    def moveRight(self):
        self.fallingPiece['x'] += 1
        mRight = True
        mLeft = False
        lastMoveSidewaysTime = time.time()
    def fillPiecePos(self,x,y,color,pixelx=None, pixely=None):
        self.color = color
        if self.color == period:
            return # if the block is not to be filled
        if pixelx == None and pixely == None:
            pixelx, pixely = convertToPixelCoords(x, y)
        pygame.draw.rect(DISPLAYSURF, colors[self.color],(pixelx+1,pixely+1, dimen,dimen))

def getBlankBoard():
    # create and return a new blank board data structure
    board2 = []
    for i in range(bw):
        board2.append([period] * bh)
    return board2

board1 = getBlankBoard()
gp = gameplay(board1)
fallingPiece = gp.getNewPiece()
nextPiece = gp.getNewPiece()
newBlock = block(fallingPiece)
bd = board(fallingPiece)
bdr = board(fallingPiece)
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((ww,wh))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris')

    showTextScreen('Tetris')
    while True:
        runGame()
        showTextScreen('Game Over')

def runGame():
    global bdr
    global fallingPiece,nextPiece,newBlock,gp
    global mDown,mLeft,mRight
    global lastFallTime,lastMoveDownTime,lastMoveSidewaysTime
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)
    while True: # game loop
        if fallingPiece == None:

            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()
            tryPiece = board(fallingPiece) #Board object for fallingPiece
            bdr = board(fallingPiece)
            if not bdr.checkPiecePos(board1):
                return

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p): #Press P to pause the game
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    #pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                #    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                fallingBlock = block(fallingPiece)

                if (event.key == K_LEFT or event.key == K_a) and bdr.checkPiecePos(board, adjX=-1):
                    fallingBlock.moveLeft()

                elif (event.key == K_RIGHT or event.key == K_d) and bdr.checkPiecePos(board,adjX=1):
                    fallingBlock.moveRight()


                elif (event.key == K_UP or event.key == K_w):
                    fallingBlock.rotate(board1)

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if bdr.checkPiecePos(board1,adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    mDown = False
                    mLeft = False
                    mRight = False
                    for i in range(1, bh):
                        if not bdr.checkPiecePos(board1,adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (mLeft or mRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if mLeft and bdr.checkPiecePos(board1, adjX=-1):
                fallingPiece['x'] -= 1
            elif mRight and bdr.checkPiecePos(board1, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if mDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and fallingPiece.checkPiecePos(board1,adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:

            if not bdr.checkPiecePos(board1,adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board1, fallingPiece) #adding the fallen piece
                score += gp.checkRowEmpty(board1)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board1)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showTextScreen(text):
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(ww / 2), int(wh / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(ww / 2) - 3, int(wh / 2) - 3)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press enter to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(ww / 2), int(wh / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():

    checkForQuit()


    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):

    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def drawBoard(board2):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (sidemargin - 3, topmargin - 7, (bw * dimen) + 8, (bh * dimen) + 8), 5)

    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (sidemargin, topmargin, dimen * bw, dimen * bh))
    for x in range(bw):
        for y in range(bh):
            newBlock.fillPiecePos(x, y, board2[x][y])

def drawStatus(score, level):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (ww - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (ww - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (ww - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)

    drawPiece(piece, pixelx=ww-120, pixely=100)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(width):
        for y in range(height):
            if shapeToDraw[y][x] != period:
                newBlock.fillPiecePos(None, None, piece['color'], pixelx + (x * dimen), pixely + (y * dimen))
def convertToPixelCoords(boxx, boxy):
    return (sidemargin + (boxx * dimen)), (topmargin + (boxy * dimen))
if __name__ == '__main__':
    main()
