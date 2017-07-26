#IMPORTS
from selenium.webdriver.common.keys import Keys

#_______________________________________________________________________________
#CONSTANTS
TRAVIAN_URL = "https://tx3.travian.fr/"
USER_NAME = "KillingDary"
USER_PASS = "86MyTravianPass94"
#_______________________________________________________________________________
#FUNCTIONS
def login(driver):
    #go to site
    driver.get(TRAVIAN_URL)
    #complete form
    login_elem = driver.find_element_by_name("name")
    login_elem.send_keys(USER_NAME)
    login_elem = driver.find_element_by_name("password")
    login_elem.send_keys(USER_PASS)
    #submit form (press Enter)
    login_elem.send_keys(Keys.RETURN)
    print "done logging in"
    return driver
