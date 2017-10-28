from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
import time
import numpy as np

class Interface:
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.driver.get('http://minesweeperonline.com/')

	def reset(self):
		time.sleep(3)
		actions = ActionChains(self.driver)
		actions.click(self.driver.find_element_by_id('face'))
		actions.perform()

	def reveal(self, coord):
		x, y = coord
		x += 1
		y += 1
		elem = self.driver.find_element_by_id('{}_{}'.format(y, x))
		actions = ActionChains(self.driver)
		actions.click(elem)
		actions.perform()
		try:
			elem = self.driver.find_element_by_id('face')
		except UnexpectedAlertPresentException:
			Alert(self.driver).dismiss()
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

		# start = time.time()
		html = self.driver.find_element_by_id('game').get_attribute('innerHTML')

		flags_left = 100 * int(html[html.find('mines_hundreds')-7]) + 10 * int(html[html.find('mines_tens')-7]) \
			+ int(html[html.find('mines_ones')-7])

		# print('Getting flag number took {} seconds'.format(time.time()-start))
		# start = time.time()

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

		# print('Getting width and height took {} seconds'.format(time.time()-start))
		# start = time.time()

		revealed_board = np.zeros((w, h), dtype=np.int32)
		num_board = np.full((w, h), -1, dtype=np.int32)
		flag_board = np.zeros((w, h), dtype=np.int32)

		for x in range(w):
			for y in range(h):
				sub = '{}_{}'.format(y + 1, x + 1)
				i = html.find(sub)
				char = html[i - 7]
				if char == 'd':
					flag_board[x, y] = 1
				elif char != 'k':
					revealed_board[x, y] = 1
					num_board[x, y] = int(char)

		# print('Getting boards took {} seconds'.format(time.time()-start))
		return revealed_board, num_board, flag_board, flags_left

# inter = Interface()
# inter.open()
# while True:
# 	input()
# 	for i in inter.get_bot_obs():
# 		print(i)
