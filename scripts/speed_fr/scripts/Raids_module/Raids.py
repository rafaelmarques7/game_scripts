from selenium.webdriver.common.keys import Keys
import random

send_troops_link = 'https://tx3.travian.fr/build.php?tt=2&id=39'

def def_coords(driver):
    if random.randint(0,1) == 0:
        x, y = 48, 31
        SLEEP_TIME = 35*60+20
    else:
        x, y = 56, 29
        SLEEP_TIME = 2*(40*60)
    x_div = driver.find_element_by_name('x')
    x_div.send_keys(x)
    y_div = driver.find_element_by_name('y')
    y_div.send_keys(y)
    return SLEEP_TIME

def def_troops(driver):
    all_troops_one_xpath = '//*[@id="troops"]/tbody/tr[1]/td[1]/a'
    #select all troops (only maceman considered here) available
    try:
        driver.find_element_by_xpath(all_troops_one_xpath).click()
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
    answer = def_troops(driver)
    if answer:
        def_atack_type(driver)
        send_troops(driver)
        return SLEEP_TIME
    else:
        SLEEP_TIME = 5*60
        return SLEEP_TIME
    #atacking that guy takes 17:40 mins, so 35:20 total
