#TIC TAC TOE
import random
import math
import sys

def checkIntLength(int):
	return len(str(int))

def is_int(integer):
	try:
		int(integer)
	except ValueError:
		return False

	return integer

def create_game():
	global game

	#Wipe game
	game = None

	#Create new game, set it up, choose player to begin
	game = Game()
	game.setup_game()
	game.choose_player()

class Game:

	def __init__(self):
		self.player1 = None
		self.player2 = None
		self.board = None
		self.gameOver = False
		self.currentPlayer = None
		self.moves = 0

	def setup_game(self):

		#Get Player names - no restrictions
		print("Player 1, what is your name?")
		self.player1 = Player(input())
		print("Player 2, what is your name?")
		self.player2 = Player(input())

		#Randomly assign X and O
		if(random.randrange(0,2) == 0):
			self.player1.markerType = 'O'
			self.player2.markerType = 'X'
		else:
			self.player1.markerType = 'X'
			self.player2.markerType = 'O'

		#Get the square root of the grid to generate the board
		print("What square root would you like to generate a board with? (normal game is 3)")
		gridRoot = is_int(input())

		#Ensure user input is whole number
		while(gridRoot == False):
			print("Sorry, must be a whole number")
			gridRoot = is_int(input())
		
		#Generate board
		self.board = Board(float(gridRoot))

	def end_game(self, message):
		self.board.draw_board()

		print("\n"+str(message)+" wins!\nGAME OVER!")

		print("Would you like to play again, y/n?")
		run = True
		choice = input().lower()

		#Check if selection is y or n, if not try again
		while(run != False):
			if(choice == 'y' or choice == 'n'):
				run = False
				break
			else:
				print("That is not an option - please use either 'y' or 'n'")
				choice = input().lower()

		#End or begin again
		if(choice == 'n'):
			exit()
		elif(choice == 'y'):
			print("STARTING ANOTHER GAME")
			create_game()

	def check_win(self, coords):
		rowNum = coords[0]
		colNum = coords[1]
		checkMarker = self.currentPlayer.markerType
		gridRoot = int(math.sqrt(self.board.gridSize))
		playerName = self.currentPlayer.name

		#HORIZONTAL
		#Check if row, where latest move was made, resulted in horizontal win
		for i, slot in enumerate(self.board.grid[rowNum]):
			#If other marker detected, stop looking
			if(slot.marker != checkMarker):
				break
			#If loop ever runs to end, meaning all are the same, end game
			elif(i == gridRoot - 1):
				self.end_game(playerName)

		#VERTICAL
		#Check if column, where latest move was made, resulted in vertical win
		for i, row in enumerate(self.board.grid):
			if(row[colNum].marker != checkMarker):
				break
			elif(i == gridRoot - 1):
				self.end_game(playerName)

		#LEFT DIAGONAL
		#If latest move was 1->len diagonal (right-slant), or middle, check
		if(rowNum == colNum):
			for i, row in enumerate(self.board.grid):
				if(row[i].marker != checkMarker):
					break
				elif(i == gridRoot - 1):
					self.end_game(playerName)

		#RIGHT DIAGONAL
		#If latest move was [0][len]->[len][0] diagonal (left-slant), or middle, check
		if(rowNum + colNum + 1 == gridRoot):
			for i, row in enumerate(self.board.grid):
				#Calculate correct position of diagonal to check (x = gridRoot - 1 - i)
				colCheck = gridRoot - 1 - i
				if(row[colCheck].marker != checkMarker):
					break
				elif(i == gridRoot - 1):
					self.end_game(playerName)

	def choose_player(self):
		num = random.randrange(1,2)
		if(num == 1):
			self.currentPlayer = self.player1
		else:
			self.currentPlayer = self.player2

	def switch_player(self):
		if(self.currentPlayer == self.player1):
			self.currentPlayer = self.player2
		else:
			self.currentPlayer = self.player1

class Board:

	def __init__(self, root):
		self.gridRoot = int(root)
		self.gridSize = int(math.pow(root, 2))
		self.grid = []
		slotNum = 0

		#Build grid and populate with Empty Slots
		for x in range(0, int(root)):
			self.grid.append([])
			for y in range(0, int(root)):
				slotNum += 1
				self.grid[x].append(Slot('-'))

	def draw_board(self):
		#Create outer loop to run through rows in grid and inner loop to print elements (usually 3x3)
		#Local variable i and j counts the number of loops - last loop skips row print and column print, respectively
		div = ''
		divLen = 0

		#Give some space after last printed statement
		print('\n')

		#Calculate length of divider (3xrowLen) + (rowLen-1)
		divLen = (3*self.gridRoot) + (self.gridRoot-1)

		#Create divider
		for i in range(0, divLen):
			div += '-'

		#Create board array
		for i, row in enumerate(self.grid):
			rowString = ''
			for j, slot in enumerate(row):
				rowString += ' '+slot.marker+' '
				#Check if loop is final, skip printing column
				if(j != len(row)-1):
					rowString += '|'
			print(rowString)
			#Check if loop is final, skip printing row
			if(i != len(self.grid)-1):
				print(div)

		print('\n')

	def place_marker(self, coords):
		marker = game.currentPlayer.markerType
		row = coords[0]
		col = coords[1]

		#Place marker at coords, set slot to be used
		self.grid[row][col].marker = marker
		self.grid[row][col].used = True

	#Check if position is empty
	def check_slot(self, movePosition):
		coords = self.get_coords(movePosition)
		row = coords[0]
		col = coords[1]

		if(self.grid[row][col].used):
			return False
		else:
			return coords

	def get_coords(self, movePosition):
		gridRoot = math.sqrt(self.gridSize)
		movePosition = float(movePosition)

		#Find corresponding row by dividing position by the row length (gridRoot) and rounding up
		row = int(math.ceil(movePosition/gridRoot)-1.0)
		#Find corresponding column by subtracting the column length from position, and multiplying by row to convert value to simulate 1 row
		col = int((movePosition-(gridRoot*row))-1.0)

		return [row, col]

	#Check if board is full (comes after win check - this means nobody won)
	def check_full(self, moves):
		if(moves >= self.gridSize):
			game.end_game("Nobody")

class Slot:

	def __init__(self, init):
		self.marker = init
		self.used = False

class Player:

	def __init__(self, name):
		self.name = name
		self.markerType = None

	def set_marker(self, marker):
		self.markerType = marker

	def player_input(self, board):
		valid = False
		movePosition = input()

		#Validate input - must be a number (int), must be above 0 and less than, or equal to, the grid length
		while(valid != True):
			if(movePosition.isdigit() and int(movePosition) > 0 and int(movePosition) <= board.gridSize):
				valid = True
				break

			print("Invalid selection, please select a number corresponding to a position on the board.")
			movePosition = input()

			if(movePosition == 0):
				game.end_game("Nobody")

		return movePosition

	def player_turn(self, board):
		print(game.currentPlayer.name + ", it's your turn - where will you place your '"+
			game.currentPlayer.markerType+"'? (Choose Slot 1-"+str(board.gridSize)+")")

		#Set initial input
		movePosition = None
		coords = False

		#Check if slot is available, if not then get another input
		while(coords == False):
			if(movePosition != None):
				print('Sorry, that slot is already used, please pick another')

			movePosition = self.player_input(board)
			coords = board.check_slot(movePosition)

		#Once valid input found, and slot not used - place marker
		board.place_marker(coords)
		game.moves += 1

		#Send back coords so position can be win-checked
		return coords

##GAME LOGIC##
game = None
create_game()

#Run Game
while(game.gameOver == False):
	#Set which Player goes first
	game.board.draw_board()

	#Make Player turn, fetch coords of move
	moveCoords = game.currentPlayer.player_turn(game.board)

	#Check for winner here - if winner, state winner and end game
	game.check_win(moveCoords)

	#If no winner, check if board is full - if so, end game
	game.board.check_full(game.moves)

	#If no win, switch player
	game.switch_player()