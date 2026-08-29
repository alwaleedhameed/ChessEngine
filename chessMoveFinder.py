import random

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
CHECKMATE = 1000
STALEMATE = 0


########################################################################
# AI Player Algorithms
def getRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


def getGreedyMove(gs, validMoves): 
    turnPrefix = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        gs.getValidMoves()
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = scoreMaterial(gs.board) * turnPrefix
        if score > maxScore: 
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove


def getManualMinMaxMove(gs, validMoves):
    turnPrefix = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = -CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if len(opponentsMoves) == 0:
            if gs.checkmate:
                gs.undoMove()
                return playerMove
            else:
                gs.undoMove(  )
                continue
        moveMinMax = CHECKMATE
        for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            gs.getValidMoves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate: 
                score = STALEMATE
            else:
                score = scoreMaterial(gs.board) * -turnPrefix
            if score < moveMinMax:
                moveMinMax = score
            gs.undoMove()
        if moveMinMax > opponentMinMaxScore:
            opponentMinMaxScore = moveMinMax
            bestMove = playerMove
        gs.undoMove()
    return bestMove

def getMinMaxMove(gs, validMoves, depthEntered):
    global nextMove
    random.shuffle(validMoves)
    nextMove = None
    depthCurrent = depthEntered
    getRecMinMax(gs, validMoves, depthEntered, depthCurrent)
    return nextMove

def getRecMinMax(gs, validMoves, depthEntered, depthCurrent):
    global nextMove
    if depthCurrent == 0:
        return scoreBoard(gs)

    whiteTurn = gs.whiteToMove
    maxScore = -CHECKMATE if whiteTurn else CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        if len(nextMoves) == 0:
            if gs.checkmate:
                score = CHECKMATE if whiteTurn else -CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
        else:
            score = getRecMinMax(gs, nextMoves, depthEntered, depthCurrent-1)
        if (whiteTurn and score > maxScore) or (not whiteTurn and score < maxScore):
            maxScore = score
            if depthCurrent == depthEntered:
                nextMove = move
        gs.undoMove()

    return maxScore


def getNegaMaxMove(gs, validMoves, depthEntered):
    global nextMove
    random.shuffle(validMoves)
    nextMove = None
    depthCurrent = depthEntered
    turnPrefix = (1 if gs.whiteToMove else -1)
    getRecNegaMax(gs, validMoves, depthEntered, depthCurrent, turnPrefix)
    return nextMove

def getRecNegaMax(gs, validMoves, depthEntered, depthCurrent, turnPrefix):
    global nextMove
    if depthCurrent == 0:
        return scoreBoard(gs) * turnPrefix

    maxScore = -CHECKMATE 
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        if len(nextMoves) == 0:
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
        else:
            score = -getRecNegaMax(gs, nextMoves, depthEntered, depthCurrent-1, -turnPrefix)
        if score > maxScore:
            maxScore = score
            if depthCurrent == depthEntered:
                nextMove = move
        gs.undoMove()
    
    return maxScore


def getNegaMaxMoveABPRUNING(gs, validMoves, depthEntered):
    global nextMove
    random.shuffle(validMoves)
    nextMove = None
    depthCurrent = depthEntered
    turnPrefix = (1 if gs.whiteToMove else -1)
    getRecNegaMaxABPRUNING(gs, validMoves, depthEntered, depthCurrent, -CHECKMATE, CHECKMATE, turnPrefix)
    return nextMove

def getRecNegaMaxABPRUNING(gs, validMoves, depthEntered, depthCurrent, alpha, beta, turnPrefix):
    global nextMove
    if depthCurrent == 0:
        return scoreBoard(gs) * turnPrefix

    maxScore = -CHECKMATE 
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        if len(nextMoves) == 0:
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
        else:
            score = -getRecNegaMaxABPRUNING(gs, nextMoves, depthEntered, depthCurrent-1, -beta, -alpha, -turnPrefix)
        if score > maxScore:
            maxScore = score
            if depthCurrent == depthEntered:
                nextMove = move
        gs.undoMove()

        if maxScore > alpha:
            alpha = maxScore

        if alpha >= beta:
            break
    
    return maxScore
 

#############################################################################
# Scoring Algorithms
# Positive: white leads. NegativeL Black leads
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
