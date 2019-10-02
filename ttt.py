import math
import random
import copy

def print_board(board):
	for row in board:
		print(row)


def get_user_input(board_size):
	user_input = -1
	again = False
	if board_size == 3:
		while not(1 <= user_input <= 9):
			if again:
				print("That's not a number between 1 and 9")
			again = True
			try:
				user_input = int(input("Pick a square 1 - 9: "))
			except:
				continue
	elif board_size == 4:
		while not(1 <= user_input <= 16):
			if again:
				print("That's not a number between 1 and 16")
			again = True
			try:
				user_input = int(input("Pick a square 1 - 16: "))
			except:
				continue
	else:
		print("Illegal Board Size")
		
	return user_input
	
def evaluate(board, board_size):
	for j in range(board_size - 2):
		for i in range(board_size):
			value = 0
			if board[i][0+j] == board[i][1+j] == board[i][2+j] != "_":
				if board[i][0+j] == 'X':
					value = - 10
					return value
				if board[i][0+j] == 'O':
					value = 10
					return value
			if board[0+j][i] == board[1+j][i] == board[2+j][i] != "_":
				if board[0+j][i] == 'X':
					value = -10
					return value
				if board[0+j][i] == 'O':
					value = 10
					return value
		for k in range(board_size - 2):
			if board[1+j][1+k] != "_":
				if (board[0+j][0+k] == board[1+j][1+k] == board[2+j][2+k] or board[0+j][2+k] == board[1+j][1+k] == board[2+j][0+k]):
					if board[1+j][1+k] == 'X':
						value = -10
						return value
					if board[1+j][1+k] == 'O':
						value = 10
						return value
	return value

def getMoves(board, board_size):
	moves = []
	for row in range(board_size):
		for col in range(board_size):
			if board[row][col] =='_':
				value = (board_size * row ) + (col + 1)
				moves.append(value)
	return moves

def update_board(board, input, user, board_size):
	row = math.trunc((input+(board_size - 1))/board_size) - 1
	col = (input - 1)%board_size
	new_board = copy.deepcopy(board)
	if new_board[row][col] == 'X' or new_board[row][col] =='O':
		raise ValueError
	if user == "user":
		new_board[row][col]= 'X'
	elif user == "cpu":
		new_board[row][col] = 'O'
	return new_board


def is_full(board, prt):
	for row in board:
		for val in row:
			if val == "_":
				return False
	if prt:
		print("You Tied!")
	return True

def game_over(board, prt, board_size):
	if is_full(board, True):
		return True
	else:
		for j in range(board_size - 2):
			for i in range(board_size):
				value = 0
				if board[i][0+j] == board[i][1+j] == board[i][2+j] != "_":
					if board[i][0+j] == 'X':
						if prt:
							print("You Win!")
						return True
					if board[i][0+j] == 'O':
						if prt:
							print("You Lose!")
						return True
				if board[0+j][i] == board[1+j][i] == board[2+j][i] != "_":
					if board[0+j][i] == 'X':
						if prt:
							print("You Win!")
						return True
					if board[0+j][i] == 'O':
						if prt:
							print("You Lose!")
						return True
			for k in range(board_size - 2):
				if board[1+j][1+k] != "_":
					if (board[0+j][0+k] == board[1+j][1+k] == board[2+j][2+k] or board[0+j][2+k] == board[1+j][1+k] == board[2+j][0+k]):
						if board[1+j][1+k] == 'X':
							if prt:
								print("You Win!")
							return True
						if board[1+j][1+k] == 'O':
							if prt:
								print("You Lose!")
							return True
	return False

def get_cpu_input(board, board_size):
	currval = -1000
	moves = getMoves(board, board_size)
	if board_size == 3:
		maxdepth = len(moves)
	else:
		maxdepth = min(len(moves), 8)
	for move in moves:
		val = minimax(0,'X',update_board(board, move, 'cpu', board_size), len(moves), board_size)
		if val > currval:
			currval = val
			selection = move
	return selection

def minimax(currdepth, turn, board, maxdepth, board_size):
	if is_full(board, False) or game_over(board, False, board_size) or currdepth == maxdepth:
		return evaluate(board, board_size)
	else:
		old_board = board
		moves = getMoves(board, board_size)
		if turn == 'O':
			best = -100
			for move in moves:
				new_board = update_board(board, move, 'cpu', board_size)
				value = minimax(currdepth + 1,'X', new_board, maxdepth, board_size)
				best = max(best, value)
			return best - currdepth
		else:
			best = 100
			for move in moves:
				new_board = update_board(board, move, 'user', board_size)
				value = minimax(currdepth + 1, 'O', new_board, maxdepth, board_size)
				best = min(best, value)
			return best + currdepth

def run_game():
	user_turn = True
	board_size = int(input("Input board size (3 or 4): "))
	game_board_init = []
	for i in range(board_size):
		game_board_init.append([])
		for j in range(board_size):
			game_board_init[i].append("_")

	print_board(game_board_init)
	new_board = game_board_init

	while not game_over(new_board, True, board_size):
		if user_turn:
			print("Your turn!")
			user_input = get_user_input(board_size)
			try:
				new_board = update_board(new_board, user_input,"user", board_size)
				print_board(new_board)
				user_turn = False
			except:
				print("That spot has been taken!")
				continue

		else:
			print("AI's turn!")
			cpu_input = get_cpu_input(new_board, board_size)
			try:
				new_board = update_board(new_board, cpu_input,"cpu", board_size)
				print_board(new_board)
				user_turn = True
			except:
				continue

	print("Game Over!")
	play_again = ""
	play_again = raw_input("Restart? (Y/N): ")
	if play_again == "Y" or play_again == "y":
		run_game()

run_game()