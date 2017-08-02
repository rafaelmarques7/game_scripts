#IMPORTS
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
#_______________________________________________________________________________
#CONSTANTS
TRAVIAN_URL = "https://ts3.travian.it/"
USER_NAME = "Rafa"
USER_PASS = "Rafa86rafa94"
#_______________________________________________________________________________
#FUNCTIONS
def login():
    #create browser
    driver = webdriver.Chrome()
    #go to site
    driver.get(TRAVIAN_URL)
    #complete login form
    login_elem = driver.find_element_by_name("name")
    login_elem.send_keys(USER_NAME)
    login_elem = driver.find_element_by_name("password")
    login_elem.send_keys(USER_PASS)
    #submit form (press Enter)
    login_elem.send_keys(Keys.RETURN)
    print "Done logging in"
    return driver
