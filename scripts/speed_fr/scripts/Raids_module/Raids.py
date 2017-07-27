from selenium.webdriver.common.keys import Keys
import random
import math
import farm

send_troops_link = 'https://tx3.travian.fr/build.php?tt=2&id=39'

def calculate_sleep_time(x_t, y_t):
    x_me, y_me = 47, 27
    map_dist = math.sqrt(math.pow(x_me - x_t, 2) + math.pow(y_me-y_t,2))
    maceman_speed = 14
    time_hours = map_dist/maceman_speed
    time_secs = time_hours * 3600
    return 2 * time_secs

def def_coords(driver):
    x, y = farm.get_coords()
    x_div = driver.find_element_by_name('x')
    x_div.send_keys(x)
    y_div = driver.find_element_by_name('y')
    y_div.send_keys(y)
    SLEEP_TIME = calculate_sleep_time(x, y)
    return SLEEP_TIME

"""
def def_troops(driver):
    all_troops_one_xpath = '//*[@id="troops"]/tbody/tr[1]/td[1]/a'
    #select all troops (only maceman considered here) available
    try:
        driver.find_element_by_xpath(all_troops_one_xpath).click()
        return True
    except Exception:
        print "no troops available"
        return False
"""
def def_troops(driver):
    maceman_div = driver.find_element_by_name('t1')
    maceman_div.send_keys('25')
    #check if no troops are available, and return 0 in that case
    maceman_av_xpath = '//*[@id="troops"]/tbody/tr[1]/td[1]/a'
    try:
        maceman_av = driver.find_element_by_xpath(maceman_av_xpath)
        return True
    except Exception:
        print "no troops available"
        return False

def def_atack_type(driver):
    raid_xpath = '//*[@id="build"]/div[2]/form/div[2]/label[3]/input'
    driver.find_element_by_xpath(raid_xpath).click()

def send_troops(driver):
    send_button_xpath = '//*[@id="btn_ok"]/div/div[2]'
    driver.find_element_by_xpath(send_button_xpath).click()
    #confirm (next page)
    confirm_button_xpath = '//*[@id="btn_ok"]/div/div[2]'
    driver.find_element_by_xpath(confirm_button_xpath).click()

def raid(driver):
    driver.get(send_troops_link)
    SLEEP_TIME = def_coords(driver)
    #answer = def_troops(driver)
    troops_av = def_troops(driver)
    if not troops_av:
        return 0
    def_atack_type(driver)
    send_troops(driver)
    return SLEEP_TIME

    """
    if answer:
        def_atack_type(driver)
        send_troops(driver)
        return SLEEP_TIME
    else:
        SLEEP_TIME = 5*60
        return SLEEP_TIME
    #atacking that guy takes 17:40 mins, so 35:20 total
    """
