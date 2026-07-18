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

    #  Doesn't work with en passant, castling, & pawn promotion.
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
         if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getPossibleMoves()

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
        if self.whiteToMove:
            if self.board[r-1][c] == '--': # Regular step forward
                if r == 6 and self.board[r-2][c] == '--': # Initial two step
                    moves.append(Move((r, c), (r-2, c), self.board))
                moves.append(Move((r, c), (r-1, c), self.board))
            if c != 7 and self.board[r-1][c+1][0] == 'b': # Capturing up right
                moves.append(Move((r, c), (r-1, c+1), self.board))
            if c != 0 and self.board[r-1][c-1][0] == 'b': # Capturing up left
                moves.append(Move((r, c), (r-1, c-1), self.board))
            
        else:
            if self.board[r+1][c] == '--':
                if r == 1 and self.board[r+2][c] == '--':  # Initial two step
                    moves.append(Move((r, c), (r+2, c), self.board))
                moves.append(Move((r, c), (r+1, c,), self.board))
            if c != 7 and self.board[r+1][c+1][0] == 'w': # Capturing down right
                moves.append(Move((r, c), (r+1, c+1), self.board))
            if c != 0 and self.board[r+1][c-1][0] == 'w': # Capturing down left
                moves.append(Move((r, c), (r+1, c-1), self.board))


    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            rTry = 1 # Finding valid non-white piece spaces up
            moveToSave = None
            while r - rTry >= 0 and self.board[r - rTry][c][0] == '-':
                moves.append(Move((r, c),(r - rTry, c), self.board))
                rTry += 1
            if r - rTry >= 0 and self.board[r - rTry][c][0] == 'b':
                moves.append(Move((r, c),(r - rTry, c), self.board))

            rTry = 1 # Finding valid non-white piece spaces down
            moveToSave = None
            while r + rTry <= 7 and self.board[r + rTry][c][0] == '-':
                moves.append(Move((r, c),(r + rTry, c), self.board))
                rTry += 1
            if r + rTry <= 7 and self.board[r + rTry][c][0] == 'b':
                moves.append(Move((r, c),(r + rTry, c), self.board))

            cTry = 1 # Finding valid non-white piece spaces left
            moveToSave = None
            while c - cTry >= 0 and self.board[r][c - cTry][0] == '-':
                moves.append(Move((r, c),(r, c - cTry), self.board))
                cTry += 1
            if c - cTry >= 0 and self.board[r][c - cTry][0] == 'b':
                moves.append(Move((r, c),(r, c - cTry), self.board))

            cTry = 1 # Finding valid non-white piece spaces right
            moveToSave = None
            while c + cTry <= 7 and self.board[r][c + cTry][0] == '-':
                moves.append(Move((r, c),(r, c + cTry), self.board))
                cTry += 1   
            if  c + cTry <= 7 and self.board[r][c + cTry][0] == 'b':
                moves.append(Move((r, c),(r, c + cTry), self.board))


        else:
            rTry = 1 # Finding valid non-white piece spaces up
            moveToSave = None
            while r - rTry >= 0 and self.board[r - rTry][c][0] == '-':
                moves.append(Move((r, c),(r - rTry, c), self.board))
                rTry += 1
            if r - rTry >= 0 and self.board[r - rTry][c][0] == 'w':
                moves.append(Move((r, c),(r - rTry, c), self.board))

            rTry = 1 # Finding valid non-white piece spaces down
            moveToSave = None
            while r + rTry <= 7 and self.board[r + rTry][c][0] == '-':
                moves.append(Move((r, c),(r + rTry, c), self.board))
                rTry += 1
            if r + rTry <= 7 and self.board[r + rTry][c][0] == 'w':
                moves.append(Move((r, c),(r + rTry, c), self.board))

            cTry = 1 # Finding valid non-white piece spaces left
            moveToSave = None
            while c - cTry >= 0 and self.board[r][c - cTry][0] == '-':
                moves.append(Move((r, c),(r, c - cTry), self.board))
                cTry += 1
            if c - cTry >= 0 and self.board[r][c - cTry][0] == 'w':
                moves.append(Move((r, c),(r, c - cTry), self.board))

            cTry = 1 # Finding valid non-white piece spaces right
            moveToSave = None
            while c + cTry <= 7 and self.board[r][c + cTry][0] == '-':
                moves.append(Move((r, c),(r, c + cTry), self.board))
                cTry += 1   
            if c + cTry <= 7 and self.board[r][c + cTry][0] == 'w':
                moves.append(Move((r, c),(r, c + cTry), self.board))

        # alternate codeblock:
        '''
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i 
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move(r, c), (endRow, endCol), self.board)
                    elif endPiece[0] == enemyColor:
                        moves.append(Move(r, c), (endRow, endCol), self.board)
                        break
                    else:
                        break
                else:
                    break   

        return moves
        '''


    def getKnightMoves(self, r, c, moves):
        spots = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (-1, -2), (1, -2), (-2, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for spot in spots: 
            endRow = r + spot[0]
            endCol = c + spot[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--' or endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1,1), (1,1), (1,-1), (-1,-1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
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
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        

    def getKingMoves(self, r, c, moves):
        pass

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # "hash function"
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getFileRank(self.startRow, self.startCol) + self.getFileRank(self.endRow, self.endCol)

    def getFileRank(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] 