import numpy as np
import random

class MineSweeperGame:
	def __init__(self, w, h, num_bombs):
		self.width = w
		self.height = h
		self.num_bombs = num_bombs
		self.flags_left = num_bombs

		self.bomb_board = None
		self.revealed_board = None
		self.num_board = None
		self.flag_board = None

		self.reset()

	def reset(self):
		self.flags_left = self.num_bombs

		self.bomb_board = np.zeros((self.width, self.height), dtype=np.int32)

		coord_set = set()
		for x in range(self.width):
			for y in range(self.height):
				coord_set.add((x, y))

		for coord in random.sample(coord_set, self.num_bombs):
			self.bomb_board[coord] = 1

		self.revealed_board = np.zeros((self.width, self.height), dtype=np.int32)
		self.num_board = np.full((self.width, self.height), -1, dtype=np.int32)
		self.flag_board = np.zeros((self.width, self.height), dtype=np.int32)

	def reveal(self, coord):
		if self.revealed_board[coord] or self.flag_board[coord]:
			return 0

		self.revealed_board[coord] = 1

		if self.bomb_board[coord]:
			return -1

		num = 0
		neighbors = self.get_neighbors(coord)
		for xy in neighbors:
			if self.bomb_board[xy]:
				num += 1

		self.num_board[coord] = num
		if num == 0:
			for xy in neighbors:
				self.reveal(xy)

		if np.array_equal(self.revealed_board + self.bomb_board, np.full((self.width, self.height), 1)):
			return 1
		else:
			return 0

	def flag(self, coord):
		if self.revealed_board[coord]:
			return

		self.flag_board[coord] = (not self.flag_board[coord]) + 0
		if self.flag_board[coord]:
			self.flags_left -= 1
		else:
			self.flags_left += 1

	def get_neighbors(self, coord):
		x, y = coord
		coords = set()
		for ix in [-1, 0, 1]:
			for iy in [-1, 0, 1]:
				if ix == 0 and iy == 0:
					continue
				tx = x + ix
				ty = y + iy
				if tx in range(self.width) and ty in range(self.height):
					coords.add((tx, ty))

		return coords

	def get_bot_obs(self):
		return self.revealed_board, self.num_board, self.flag_board, self.flags_left
