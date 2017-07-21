from selenium import webdriver
from selenium.webdriver.common.keys import Keys

travian_url = "https://tx3.travian.pt/?lang=pt"
user_name = "rafaelmarques7"
user_pass = "Rafa86rafa94"

driver = webdriver.Chrome()
driver.get(travian_url)

login_elem = driver.find_element_by_name("name")
login_elem.send_keys(user_name)
login_elem = driver.find_element_by_name("password")
login_elem.send_keys(user_pass)
login_elem.send_keys(Keys.RETURN)

print "done logging in"

iron_pit_url = "https://tx3.travian.pt/build.php?id=4"
driver.get(iron_pit_url)
#upgrade_button = driver.find_element_by_class_name("button-container")
upgrade_button = driver.find_element_by_xpath("//button[contains(.,'Melhorar')]")
upgrade_button.click()
