from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import Login

driver = Login.login()
print "login sucessful"

def map_centering(driver):
    MAP = 'https://tx3.travian.fr/karte.php?x=42&y=58'

    driver.get(MAP)

    element_x_path = '//*[@id="xCoordInputMap"]'
    element_y_path = '//*[@id="yCoordInputMap"]'

    coord_x = 47
    coord_y = 27

    element_x = driver.find_element_by_xpath(element_x_path)
    element_x.send_keys(coord_x)

    element_y = driver.find_element_by_xpath(element_y_path)

    element_y.send_keys(coord_y)

    #submit form (press Enter)
    element_y.send_keys(Keys.RETURN)
    print "centering complete"

    center_click(driver)

def center_click(driver):
    element_map_path = '//*[@id="mapContainer"]/div[2]'
    element_map = driver.find_element_by_xpath(element_map_path)
    # move_to_element moves the mouse to the middle of an element.
    action3 = ActionChains(driver)
    action3.move_to_element(element_map)
    action3.click(element_map)
    action3.perform()

    #send_troops(driver)

def send_troops(driver):

    send_button_path = '//*[@id="tileDetails"]/div[1]/div/div[2]/span'
    send_button = driver.find_elements_by_xpath(send_button_path).click()


map_centering(driver)
