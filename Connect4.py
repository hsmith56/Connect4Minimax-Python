import random
import copy

"""
TODO:
 - Add the different win conditions [vert,horiz,diag]
 - adjust isSameOver() to reflect accurate board states
 - [[Done* -> currently 0-6, simple fix later]] change moves to numbers 1-7 
 - [[Done -> makes move and returns true, otherwise false]] change logic to drop to lowest position 
 - [[Done -> returns list 0,6]] create is valid to get columns with open spots 
 - change minimax to only play on x axis
"""

PIECES = {0:'x',1:'o',None:'_'}

class Game:
	def __init__(self, p1, p2):
		self.board = [[Piece(None,None) for _ in range(7)] for _ in range(6)]
		self.gameover = False
		self.winner = None
		self.p1 = p1
		self.p2 = p2

	def move(self, piece, x):
		if self.board[0][x].control == None:
			for row in range(len(self.board)-1,0,-1):
				if self.board[row][x].control == None:
					self.board[row][x] = piece
					return True
			self.board[0][x] = piece
		return False

	def printBoard(self):
		for x in self.board:
			row = [l.piece for l in x]
			print(row)
		print('')

	def isGameOver(self):
		"""
		# 1 - returns true if there is a win across a row [Done]
		# 2 - returns true if there is a win on a column [Done]
		# 3 - returns true if diagional win from bottom left to top right
		# 4 - returns true if diagional win from top left to bottom right 
		# 5 - returns false if there is still empty spots to play [same as TicTacToe]
		# 6 - returns true if no spots left to play, meaning a tie [same as TicTacToe]
		"""

		for num, row in enumerate(self.board): # 1 Updated
			for index,pos in enumerate(row[0:len(row)-3]):
				if row[index:index+4].count(pos) == 4 and row[index].control != None:
					self.gameover = True
					self.winner = row[index]
					return True

		for col in range(len(self.board[0])):
			for row in range(0,len(self.board)-3):
				# to call x,y cartesian coordinate do self.board[row][col]
				if self.board[row][col].control != None:
					if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
						self.gameover = True
						self.winner = self.board[row][col]
						return True

		if self.board[2][0].control != None: # 3
			if self.board[2][0].control == self.board[1][1].control == self.board[0][2].control:
				self.gameover = True
				self.winner = self.board[2][0].control
				return True
				
		if self.board[0][0].control != None: # 4
			if self.board[0][0] == self.board[1][1] == self.board[2][2]:
				self.gameover = True
				self.winner = self.board[0][0].control
				return True

		for x in self.board: # 5
			row = [l.control for l in x]
			if None in row:
				return
						
		self.winner = 'Tie'	# 6	
		self.gameover = True
		return True 
		
	def getEmpty(self):
		"""
		Returns an array of all valid empty positions on a board
		"""
		list1 = []
		for x, piece in enumerate(self.board[0]):
			if piece.control == None:
				list1.append(x)
		return list1

class Piece:
	def __init__(self, control, name):
		self.control = control
		self.piece = PIECES[control]
		self.name = name

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

def minimax(board, depth, maximizingPlayer):
	if board.isGameOver():
		if board.gameover:
			if board.winner == board.p1.control:
				return 10*depth
			if board.winner == board.p2.control:
				return -11*depth
		return 0

	if maximizingPlayer:
		value = -5
		for pos in board.getEmpty():
			boardCopy = copy.deepcopy(board)
			boardCopy.move(boardCopy.p1,pos[0],pos[1])
			value = max(value, minimax(boardCopy, depth-1, False))
		return value

	else:
		value = 5
		for pos in board.getEmpty():
			boardCopy = copy.deepcopy(board)
			boardCopy.move(boardCopy.p2,pos[0],pos[1])
			value = min(value, minimax(boardCopy, depth-1, True))
		return value

def aiMove(game,p1):
	if game.board[5][3].control == None:
		game.move(p1, 3)
		return
	Value = -1
	pos = game.getEmpty()[0]
	for pos in game.getEmpty():
		gameCopy = copy.deepcopy(game)
		gameCopy.move(p1, pos[0], pos[1])
		preMax = Value
		Value = max(Value, minimax(gameCopy,4,False))
		if preMax != Value:
			aiMove = pos
	game.move(p1, aiMove[0], aiMove[1])
	return

def playerMove(game,p2):
	playerMove = input('Where would you like to move? ').split(sep=',')
	print(playerMove)
	playerMove = [int(playerMove[0]),int(playerMove[1])]
	while playerMove not in game.getEmpty():
		playerMove = input('Please enter a valid position ').split(sep=',')
		playerMove = [int(playerMove[0]),int(playerMove[1])]
	game.move(p2, playerMove[0], playerMove[1])






def newGame():
	"""
	Create a new Game object, initialize each Piece object and assign randomly 
	to ai and player. 
	"""
	replay = 'y'
	while replay == 'y':
		P1 = random.randint(0,1)
		P2 = 1 if P1 == 0 else 0
		p1 = Piece(P1,'AI')
		p2 = Piece(P2,'Player')
		game = Game(p1,p2)

		if P1 == 0: 
			aiMove(game, p1)
			game.printBoard()
		while not game.gameover:
			playerMove(game, p2)
			game.printBoard()
			if game.isGameOver():
				break
			aiMove(game, p1)
			game.printBoard()
			game.isGameOver()

		if game.winner == "Tie":
			print("Tie Game, better luck next time")
		elif game.winner == game.p2.control:
			print("You won! Good job.")
		else:	
			print("Yeah you lost, unsurprising")

		replay = input("Would you like to play again? [y/n] ").lower()		

# newGame()
def debug():
	P1 = random.randint(0,1)
	P2 = 1 if P1 == 0 else 0
	p1 = Piece(P1,'AI')
	p2 = Piece(P2,'Player')
	debug = Game(p1, p2)
	debug.move(p2, 0)
	debug.printBoard()
	debug.move(p2, 0)
	debug.printBoard()
	debug.isGameOver()
	debug.move(p2, 0)
	debug.printBoard()
	debug.isGameOver()
	debug.move(p2, 0)
	debug.printBoard()
	debug.isGameOver()
	print(debug.winner.piece)
	#print(debug.getEmpty())

debug()