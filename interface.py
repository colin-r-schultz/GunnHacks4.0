from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np

class Interface:
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.actions = ActionChains(self.driver)
		self.driver.get('http://minesweeperonline.com/')

	def reset(self):
		self.actions.click(self.driver.find_element_by_id('face'))
		self.actions.perform()
		self.actions.reset_actions()
		time.sleep(.5)

	def reveal(self, coord):
		x, y = coord
		x += 1
		y += 1
		elem = self.driver.find_element_by_id('{}_{}'.format(y, x))
		actions = ActionChains(self.driver)
		actions.click(elem)
		actions.perform()
		elem = self.driver.find_element_by_id('face')
		if elem.get_attribute('class') == 'facedead':
			return -1
		if elem.get_attribute('class') == 'facewin':
			return 1
		return 0

	def flag(self, coord):
		x, y = coord
		x += 1
		y += 1
		elem = self.driver.find_element_by_id('{}_{}'.format(y, x))
		actions = ActionChains(self.driver)
		actions.context_click(elem)
		actions.perform()

	def close(self):
		self.driver.close()

	def get_bot_obs(self):
		flags_left = 0
		elem = self.driver.find_element_by_id('mines_hundreds')
		flags_left += 100 * int(elem.get_attribute('class')[4])
		elem = self.driver.find_element_by_id('mines_tens')
		flags_left += 10 * int(elem.get_attribute('class')[4])
		elem = self.driver.find_element_by_id('mines_ones')
		flags_left += int(elem.get_attribute('class')[4])

		w = 0
		while True:
			try:
				w += 1
				self.driver.find_element_by_id('1_{}'.format(w))
			except NoSuchElementException:
				w -= 2
				break

		h = 0
		while True:
			try:
				h += 1
				self.driver.find_element_by_id('{}_1'.format(h))
			except NoSuchElementException:
				h -= 2
				break

		revealed_board = np.zeros((w, h), dtype=np.int32)
		num_board = np.full((w, h), -1, dtype=np.int32)
		flag_board = np.zeros((w, h), dtype=np.int32)

		for x in range(w):
			for y in range(h):
				status = self.driver.find_element_by_id('{}_{}'.format(y+1, x+1)).get_attribute('class')
				if status == 'square bombflagged':
					flag_board[x, y] = 1
				elif status != 'square blank':
					revealed_board[x, y] = 1
					num_board[x, y] = status[11]

		return revealed_board, num_board, flag_board, flags_left

# inter = Interface()
# inter.open()
# while True:
# 	input()
# 	for i in inter.get_bot_obs():
# 		print(i)
