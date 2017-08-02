#the objective of this module is to create a script that
#finds ALL crops on the travian map!
#->method:
#   1)iterate over all coordenatis possible;
#   2)center map on the coordenatis
#   3)try to get number of crop fields using xpath
#       -> return 0 if not possble (meaning it's either occupied village or oasis)
#   4)save the crops coordinatis in a field when we find one!
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import Login
import time
import Clean_functions
MAP = 'https://tx3.travian.it/karte.php?x=59&y=31'

def coord_gen():
	for x in range(68,77):
		for y in range(14,21):
			yield [x, y]

def map_centering(driver, coord_x, coord_y):
	if (coord_x == 68 and coord_y == 14):
		driver.get(MAP)
	element_x_path = '//*[@id="xCoordInputMap"]'
	element_y_path = '//*[@id="yCoordInputMap"]'
	element_x = driver.find_element_by_xpath(element_x_path)
	element_x.clear()
	element_x.send_keys(coord_x)
	element_y = driver.find_element_by_xpath(element_y_path)
	element_y.clear()
	element_y.send_keys(coord_y)
	#submit form (press Enter)
	element_y.send_keys(Keys.RETURN)
	#print "centering complete"

def get_coords(driver):
	for [x, y] in coord_gen():
		print x, y
		map_centering(driver, x, y)
		center_click(driver)
		time.sleep(1)
		answer = check_crops(driver)
		if answer == 0:
			continue
		else:
			number_crops, free_flag = answer[0], answer[1]
			if (number_crops == 9 or number_crops == 15):
				write_to_file(x, y, number_crops, free_flag)

def center_click(driver):
    element_map_path = '//*[@id="mapContainer"]/div[2]'
    element_map = driver.find_element_by_xpath(element_map_path)
    # move_to_element moves the mouse to the middle of an element.
    action3 = ActionChains(driver)
    action3.move_to_element(element_map)
    action3.click(element_map)
    action3.perform()

def close_pop_up(driver):
	cancel_xpath = '//*[@id="dialogCancelButton"]'
	try:
		driver.find_element_by_xpath(cancel_xpath).click()
	except:
		driver.get(MAP)

def check_crops(driver):
	try:
		crop_div_xpath = '//*[@id="distribution"]/tbody/tr[4]/td[2]'
		crop_div =  driver.find_element_by_xpath(crop_div_xpath)
		crop_number =crop_div.text
		#print "clicking escape"
		close_pop_up(driver)
		print 'cereal crops: ' + str(crop_number)
		return [int(crop_number), 'free']
	except:
		pass
	try:
		crop_div_xpath = '//*[@id="distribution"]/tbody/tr/td[4]/img'
		crop_div =  driver.find_element_by_xpath(crop_div_xpath)
		crop_number =crop_div.text
		crop_number = Clean_functions.extract_health(crop_number)
		print 'cereal crops: ' + str(crop_number)
		return [crop_number, 'occ']
	except:
		pass
	#except Exception:
		#print "clicking escape"
	close_pop_up(driver)
	return 0

def write_to_file(x, y, c_n, free_flag):
	print 'writing to file. x = ' + str(x) + ' y= ' + str(y) + 'crop_number = ' + str(c_n)
	with open('crop_file.txt', 'a') as f:
		if free_flag == 'free':
			f.write('**' + str(x) + ' ' + str(y) + ' ' + str(c_n) +'\n')
		else:
			f.write(str(x) + ' ' + str(y) + ' ' + str(c_n) +'\n')

def main():
	driver = Login.login()
	print "login sucessful"
	get_coords(driver)

main()
