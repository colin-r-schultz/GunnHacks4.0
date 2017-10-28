from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np

driver = webdriver.Firefox()
driver.get('http://minesweeperonline.com/')

time.sleep(10)

w = 0
while True:
	try:
		w += 1
		driver.find_element_by_id('1_{}'.format(w))
	except NoSuchElementException:
		w -= 2
		break

h = 0
while True:
	try:
		h += 1
		driver.find_element_by_id('{}_1'.format(h))
	except NoSuchElementException:
		h -= 2
		break

start = time.time()

revealed_board2 = np.zeros((w, h), dtype=np.int32)
num_board2 = np.full((w, h), -1, dtype=np.int32)
flag_board2 = np.zeros((w, h), dtype=np.int32)

html = driver.find_element_by_id('game').get_attribute('innerHTML')
print(html)
exit()

for x in range(w):
	for y in range(h):
		sub = '{}_{}'.format(y+1, x+1)
		i = html.find(sub)
		char = html[i - 7]
		if char == 'd':
			flag_board2[x, y] = 1
		elif char != 'k':
			revealed_board2[x, y] = 1
			num_board2[x, y] = int(char)


print('New method took {} seconds'.format(time.time()-start))

print(revealed_board)
print('\n')
print(revealed_board2)
print('\n')
print('\n')
print(num_board)
print('\n')
print(num_board2)
print('\n')
print('\n')
print(flag_board)
print('\n')
print(flag_board2)
