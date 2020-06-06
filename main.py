"""
#########Tic Tac Toe Game###########
Using the minimax algorithm, this programm provides an unbeatable tic tac toe enemy.


"""

import tkinter as tk

X = 'X'  # AI
O = 'O'  # Human
EMPTY = '-'
GameOver = "Draw"

class MiniMax():
    def __init__(self,evalFunc):
        self.evalFunc = evalFunc

    def copyBoard(self,board):
        """
        creates a copy of the given board.
        This could also be accomplished using the copy() function.
            :param board: the board to be copy
            :returns: a copy of the board
        """
        newBoard = []
        for i in range(0, 9):
            newBoard.append(board[i])
        return newBoard

    def getPossibleMoves(self,board):
        """
            :param board: the board to be evaluated
            :return: the indices of the positions, where a move could be placed
        """
        moves = []
        for counter, i in enumerate(board):
            if i == EMPTY:
                moves.append(counter)
        return moves

    def getBestMove(self,board,player):
        """
        Using the miniMax algorithm the best move for the player(parameter) is found
        by exploring all possible moves and returning the best move for the respective player.
            :param board: the board, upon the best move is to be found
            :param player: the player, from whose point the best move is to be found
            :return: the best move, and its value (-1 -> good for AI, 0 -> neutral, 1 -> good for player)
            """
        moves = []
        gameStatus = self.evalFunc(board)
        if gameStatus == GameOver:
            return None, 0
        elif gameStatus == X:
            return None, 1
        elif gameStatus == O:
            return None, -1
        possibleMoves = self.getPossibleMoves(board)
        for possibleMove in possibleMoves:
            move = {'index': possibleMove}
            nextState = self.copyBoard(board)
            nextState[possibleMove] = player
            if player == X:
                retMove, result = self.getBestMove(nextState, 'O')
                move['score'] = result
            elif player == O:
                retMove, result = self.getBestMove(nextState, 'X')
                move['score'] = result
            moves.append(move)

        playMove = None
        best = None
        if player == O:
            best = 100
            for move in moves:
                if move['score'] <= best:
                    playMove = move['index']
                    best = move['score']
        elif player == X:
            best = -100
            for move in moves:
                if move['score'] >= best:
                    playMove = move['index']
                    best = move['score']

        return playMove, best


class TicTacToeGui():
    def __init__(self):
        self.board = ['-','-','-','-','-','-','-','-','-']
        self.continueToPlay = True
        self.gameRunning = True
        self.window = tk.Tk()
        self.againstAI = True
        self.AI = MiniMax(self.checkBoard)
        self.tiles = []
        self.curPlayer = O

    def makeMove(self,pos):
        """
        Places the given position on the board if the spot is free.
        Otherwise the player is asked again, and the function is recursivly recalled
            :param board: the board upon the placement is supposed to be made
            :param player: the player, who is supposed to be placed
            :param pos: the position of the placement
            :returns: Nothing
        """
        if self.gameRunning and self.board[pos] != EMPTY:
            print("Place already taken")
        elif self.gameRunning:
            self.board[pos] = self.curPlayer
            self.updateTiles()
            if self.checkBoard(self.board) :
                self.labelInfoText['text'] = "Game Over. " + self.checkBoard(self.board) + " has won.\n Click anywhere to rematch"
                self.gameRunning = False
                return
            self.window.update()
            if self.curPlayer == X:
                self.curPlayer = O
            else:
                self.curPlayer = X
            if self.againstAI == True and self.curPlayer == X:
                self.makeMove(self.AI.getBestMove(self.board,self.curPlayer)[0])
        else:
            self.board = ['-','-','-','-','-','-','-','-','-']
            self.updateTiles()
            self.labelInfoText['text'] = "The game is on!!!"
            self.curPlayer = O
            self.gameRunning = True

    def updateTiles(self):
        for counter,tile in enumerate(self.tiles):
            tile['text'] = self.board[counter]

    def checkBoard(self,board):
        """
            :param board:
            :returns: if there is a winner, the winner, gameOver if draw, else False
        """
        for i in range(0, 3):
            if {board[int(i * 3)], board[int(i * 3) + 1], board[int(i * 3) + 2]} == {X} or {board[i], board[i + 3], board[i + 6]} == {X}:
                return X
            elif {board[int(i * 3)], board[int(i * 3) + 1], board[int(i * 3) + 2]} == {O} or {board[i], board[i + 3], board[i + 6]} == {O}:
                return O

        if {board[0], board[4], board[8]} == {O} or {board[2], board[4], board[6]} == {O}:
            return O
        if {board[0], board[4], board[8]} == {X} or {board[2], board[4], board[6]} == {X}:
            return X
        if board.count(EMPTY) == 0:
            return GameOver

        return False

    def callTheJudge(self):
        """
        executes checkboard from the position of a judge.
            :param board: the board to be evaluated
            :returns: game continues -> true/false
        """
        if self.checkBoard(self.board):
            return True
        return True

    def initGui(self):
        """
        initializes the the buttons for the game and the info text.
            :return: None
        """
        self.window.geometry("550x600")
        self.window.title("Tic Tac Toe")
        for i in range(0,9):
            button = tk.Button(self.window,text=self.board[i],command=lambda i=i:self.makeMove(i),width=14,height=7,font=('Arial',12))
            button.grid(row=int(i/3),column=i%3,padx=10,pady=3)
            self.tiles.append(button)
        self.labelInfoText = tk.Label(self.window,text="Place your move human!")
        self.labelInfoText.grid(row=4,column=1)


    def printBoard(self, board):
        """
        Prints the board in a styled way, debug purpose only.
        Text version is deprecated
            :param board: the board to be printed
        """
        for row in range(0, 3):
            for cell in range(0, 3):
                print("|", board[row * 3 + cell], "|", end="")
            print("\n")



if __name__ == '__main__':
    tttgui = TicTacToeGui()
    tttgui.initGui()
    tttgui.window.mainloop()