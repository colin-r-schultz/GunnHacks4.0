import numpy as np
import random
from minesweeper import MineSweeperGame
from interface import Interface

class Region:
	def __init__(self, coord_set, num_bombs):
		self.coords = coord_set
		self.num_bombs = num_bombs

	def is_empty(self):
		return len(self.coords) == 0

	def fully_contains(self, region):
		for coord in region.coords:
			if coord not in self.coords:
				return False

		return True

	def remove(self, region):
		for coord in region.coords:
			self.coords.remove(coord)

		self.num_bombs -= region.num_bombs

	def danger(self):
		return self.num_bombs/len(self.coords)

	def pick_one(self):
		return random.sample(self.coords, 1)[0]


class Bot:
	def play(self, reveal_board, num_board, flag_board, num_flags):
		assert reveal_board.shape == num_board.shape == flag_board.shape
		w, h = reveal_board.shape
		unknown = reveal_board + flag_board

		region_set = set()

		coord_set = set()
		for x in range(w):
			for y in range(h):
				if not unknown[x, y]:
					coord_set.add((x, y))

		self.add_to_region_set(region_set, Region(coord_set, num_flags))

		for x in range(w):
			for y in range(h):
				if num_board[x, y] > 0:
					neighbors = self.get_neighbors((x, y), w, h)
					new_neighbors = set()
					for coord in neighbors:
						if not reveal_board[coord]:
							new_neighbors.add(coord)

					neighbors = new_neighbors.copy()

					flags = 0
					for coord in neighbors:
						if flag_board[coord]:
							new_neighbors.remove(coord)
							flags += 1

					num = num_board[x, y]

					self.add_to_region_set(region_set, Region(new_neighbors, num - flags))

		min_danger = 2
		least_danger = None
		openset = set()
		flagset = set()
		for region in region_set:
			if region.danger() == 0:
				openset = openset.union(region.coords)
			elif region.danger() == 1:
				flagset = flagset.union(region.coords)
			elif region.danger() < min_danger:
				min_danger = region.danger()
				least_danger = region
		if len(openset) == len(flagset) == 0:
			openset.add(least_danger.pick_one())
		return openset, flagset

	def get_neighbors(self, coord, w, h):
		x, y = coord
		coords = set()
		for ix in [-1, 0, 1]:
			for iy in [-1, 0, 1]:
				if ix == 0 and iy == 0:
					continue
				tx = x + ix
				ty = y + iy
				if tx in range(w) and ty in range(h):
					coords.add((tx, ty))

		return coords

	def add_to_region_set(self, region_set, region):
		if region.is_empty():
			return
		invalid = set()
		for old_region in region_set:
			if old_region.fully_contains(region):
				old_region.remove(region)
				invalid.add(old_region)

		region_set.add(region)

		for region in invalid:
			region_set.remove(region)
		for region in invalid:
			if not region.is_empty():
				self.add_to_region_set(region_set, region)


game = Interface()
bot = Bot()
while True:
	state = 0
	while state == 0:
		reveal_board, num_board, flag_board, flags_left = game.get_bot_obs()
		openset, flagset = bot.play(reveal_board, num_board, flag_board, flags_left)
		for coord in flagset:
			game.flag(coord)
		for coord in openset:
			state = game.reveal(coord)
			if state == -1:
				break

	print(state)
	game.reset()
