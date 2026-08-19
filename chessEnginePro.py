# Engine: Responsible for storing current state info & analyzing valid moves

class GameState():
    def __init__(self):
        # Board is 8X8 2d list, each element has 2 characters.
        # Character 1: Piece Color: "b" || "w"
        # Character 2: Piece Type: "R" || "N" || "B" || "Q" || "K" || "P"
        # "--" Represents empty spot.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveFunctions = {'P': self.getPawnMoves, 'R' : self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.enPassantPossible = () # Square location that enables en passant
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wqs, self.currentCastlingRight.wks, self.currentCastlingRight.bqs, self.currentCastlingRight.bks)]
        self.checkmate = False
        self.stalemate = False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn promotion    
        if move.isPawnPromotion:
            options = ['Q', 'R', 'B', 'N']
            flag = True
            while flag:
                choice = input("What would you like to promote to? ")
                if choice in options:
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + choice
                    flag = False
                else:
                    print("Please enter one: \nQ:Queen\nR: Rook\nB: Bishop\nN: Knight\n")

        # En Passant
        move.enPassantPossibleBeforeMove = self.enPassantPossible
        if move.isEnPassant:
            self.board[move.startRow][move.endCol] = '--'

        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enPassantPossible = ()

        # Castling
        if move.isCastle:
            if move.endCol - move.startCol == 2: # Kingside as he moves +2 cols
                self.board[move.endRow][5] = self.board[move.endRow][7]
                self.board[move.endRow][7] = '--'
            else: # Queenside from moving -2 cols
                self.board[move.endRow][3] = self.board[move.endRow][0]
                self.board[move.endRow][0] = '--'

        # Updating Castling Rights (when rook/king moves)
        self.updateCastlingRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wqs, self.currentCastlingRight.wks, self.currentCastlingRight.bqs, self.currentCastlingRight.bks))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnPassant:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enPassantPossible = move.enPassantPossibleBeforeMove 
            self.castleRightsLog.pop()
            self.currentCastlingRight = self.castleRightsLog[-1]

            if move.isCastle:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][7] = self.board[move.endRow][5]
                    self.board[move.endRow][5] = '--'
                else:
                    self.board[move.endRow][0] = self.board[move.endRow][3]
                    self.board[move.endRow][3] = '--'


    def updateCastlingRights(self, move):
        # King Handling
        if move.pieceMoved[1] == 'K':
            if move.pieceMoved[0] == 'w':
                self.currentCastlingRight.wks = False
                self.currentCastlingRight.wqs = False
            elif move.pieceMoved[0] == 'b':
                self.currentCastlingRight.bks = False
                self.currentCastlingRight.bqs = False
        elif move.pieceMoved[1] == 'R':
            if move.pieceMoved[0] == 'w':
                if (move.startRow, move.startCol) == (0,0):
                    self.currentCastlingRight.wqs = False
                elif (move.startRow, move.startCol) == (0,7):
                    self.currentCastlingRight.wks = False
            elif move.pieceMoved[0] == 'b':
                if (move.startRow, move.startCol) == (7,0):
                    self.currentCastlingRight.bqs = False
                elif (move.startRow, move.startCol) == (7,7):
                    self.currentCastlingRight.bks = False


    def getValidMoves(self):
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        moves = []
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = [] # squares that pieces can move to

                if pieceChecking[1] == "N": # knights cannot be blocked; must capture or move king
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8): # distance ahead of piece potential
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)    
                        if validSquare[0] ==  checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves


    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # Gets moves per piece 
        return moves


    def getPawnMoves(self, r, c, moves):
        pinnedPiece = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[r-1][c] == '--': # Regular step forward
                if not pinnedPiece or pinDirection == (-1, 0):
                    if r == 6 and self.board[r-2][c] == '--': # Initial two step
                        moves.append(Move((r, c), (r-2, c), self.board))
                    moves.append(Move((r, c), (r-1, c), self.board))

            if c != 7 and self.board[r-1][c+1][0] == 'b' and (not pinnedPiece or pinDirection == (-1, 1)): # Capturing up right
                moves.append(Move((r, c), (r-1, c+1), self.board))
            elif c != 7 and (r-1, c+1) == self.enPassantPossible and (not pinnedPiece or pinDirection == (-1, 1)): # Capturing up right
                moves.append(Move((r, c), (r-1, c+1), self.board, isEnPassant=True))

            if c != 0 and self.board[r-1][c-1][0] == 'b' and (not pinnedPiece or pinDirection == (-1, -1)): # Capturing up left
                moves.append(Move((r, c), (r-1, c-1), self.board))
            elif c != 0 and (r-1, c-1) == self.enPassantPossible and (not pinnedPiece or pinDirection == (-1, -1)): # Capturing up left
                moves.append(Move((r, c), (r-1, c-1), self.board, isEnPassant=True))
            
        else:
            if self.board[r+1][c] == '--':
                if not pinnedPiece or pinDirection == (1, 0):
                    if r == 1 and self.board[r+2][c] == '--':  # Initial two step
                        moves.append(Move((r, c), (r+2, c), self.board))
                    moves.append(Move((r, c), (r+1, c,), self.board))

            if c != 7 and self.board[r+1][c+1][0] == 'w' and (not pinnedPiece or pinDirection == (1, 1)): # Capturing down right
                moves.append(Move((r, c), (r+1, c+1), self.board))
            elif c != 7 and (r+1, c+1) == self.enPassantPossible and (not pinnedPiece or pinDirection == (1, 1)): # Capturing down right
                moves.append(Move((r, c), (r+1, c+1), self.board, isEnPassant=True))
            if c != 0 and self.board[r+1][c-1][0] == 'w' and (not pinnedPiece or pinDirection == (1, -1 )): # Capturing down left
                moves.append(Move((r, c), (r+1, c-1), self.board))
            elif c != 0 and (r+1, c-1) == self.enPassantPossible and (not pinnedPiece or pinDirection == (1, -1 )): # Capturing down left
                moves.append(Move((r, c), (r+1, c-1), self.board, isEnPassant=True))


    def getRookMoves(self, r, c, moves):
        pinnedPiece = False 
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True 
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            if pinnedPiece and pinDirection != d and pinDirection != (-d[0], -d[1]):
                continue
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i 
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break   
        

    def getKnightMoves(self, r, c, moves):
        piecePinned = False 
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True 
                self.pins.remove(self.pins[i])
                break
        spots = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (-1, -2), (1, -2), (-2, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for spot in spots: 
            endRow = r + spot[0]
            endCol = c + spot[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--' or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        pinnedPiece = False 
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                pinnedPiece = True 
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        directions = ((-1,1), (1,1), (1,-1), (-1,-1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            if pinnedPiece and pinDirection != d and pinDirection != (-d[0], -d[1]):
                continue
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i 
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break   


    def getQueenMoves(self, r, c, moves):
        for pin in self.pins:
            if pin[0] == r and pin[1] == c:
                self.pins.append(pin)
                break
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        

    def getKingMoves(self, r, c, moves):
        spots = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for spot in spots:
            endRow = r + spot[0]
            endCol = c + spot[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, allyColor)


    '''
    Castling
    '''
    def getCastleMoves(self, r, c, moves, allyColor):
        if self.inCheck:
             return 
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSide(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSide(r, c, moves, allyColor)
         
    def getKingSide(self, r, c, moves, allyColor):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--' and self.board[r][c+3] == allyColor + 'R':
            if allyColor == 'w':
                self.whiteKingLocation = (r, c+1)
                inCheck, x, y = self.checkForPinsAndChecks()
                if not inCheck:
                    self.whiteKingLocation = (r, c+2)
                    inCheck, x, y = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (r, c+2), self.board, isCastle=True))
                self.whiteKingLocation = (r, c)
            else:
                self.blackKingLocation = (r, c+1)
                inCheck, x, y = self.checkForPinsAndChecks()
                if not inCheck:
                    self.blackKingLocation = (r, c+2)
                    inCheck, x, y = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (r, c+2), self.board, isCastle=True))
                self.blackKingLocation = (r, c)

    def getQueenSide(self, r, c, moves, allyColor):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' and self.board[r][c-4] == allyColor + 'R':
            if allyColor == 'w':
                self.whiteKingLocation = (r, c-1)
                inCheck, x, y = self.checkForPinsAndChecks()
                if not inCheck:
                    self.whiteKingLocation = (r, c-2)
                    inCheck, x, y = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (r, c-2), self.board, isCastle = True))
                self.whiteKingLocation = (r, c)
            else:
                self.blackKingLocation = (r, c-1)
                inCheck, x, y = self.checkForPinsAndChecks()
                if not inCheck:
                    self.blackKingLocation = (r, c-2)
                    inCheck, x, y = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (r, c-2), self.board, isCastle = True))
                self.blackKingLocation = (r, c)

    '''
    Pins & Checks
    '''
    def checkForPinsAndChecks(self):
        inCheck = False
        pins = []
        checks = []
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1),  (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            dir = directions[j]
            possiblePin = () 
            for i in range(1, 8):
                endRow = kingRow + dir[0] * i
                endCol = kingCol + dir[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]  
                    if endPiece[0] == allyColor and endPiece[1] != 'K' :
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, dir[0], dir[1])
                        else: # 2nd allied piece removes pin chance
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') \
                        or (4 <= j <= 7 and type == 'B') \
                        or (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) \
                        or (type == 'Q') \
                        or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, dir[0], dir[1]))
                                break 
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break

        knightSpots = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (-1, -2), (1, -2), (-2, -1))
        for spot in knightSpots:
            endRow = kingRow + spot[0]
            endCol = kingCol + spot[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True 
                    checks.append((endRow, endCol, spot[0], spot[1]))
        return inCheck, pins, checks


class CastleRights():
    def __init__(self, wqs, wks, bqs, bks):
        self.wqs = wqs
        self.wks = wks
        self.bqs = bqs
        self.bks = bks
        


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassant = False, isCastle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Pawn Promotion
        self.isPawnPromotion = self.pieceMoved[1] == 'P' and (self.endRow == 0 or self.endRow == 7)

        # En Passant
        self.isEnPassant = isEnPassant
        if self.isEnPassant:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        self.isCastle = isCastle

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # "hash function"
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)

    def getFileRank(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] 