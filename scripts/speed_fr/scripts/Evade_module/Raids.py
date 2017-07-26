from selenium.webdriver.common.keys import Keys

send_troops_link = 'https://tx3.travian.fr/build.php?tt=2&id=39'
x_enemy, y_enemy = 48, 31

def def_coords(driver):
    x_div = driver.find_element_by_name('x')
    x_div.send_keys(x_enemy)
    y_div = driver.find_element_by_name('y')
    y_div.send_keys(y_enemy)

def def_troops(driver):
    all_troops_one_xpath = '//*[@id="troops"]/tbody/tr[1]/td[1]/a'
    #select all troops (only maceman considered here) available
    driver.find_element_by_xpath(all_troops_one_xpath).click()

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
    def_coords(driver)
    def_troops(driver)
    def_atack_type(driver)
    send_troops(driver)
    #atacking that guy takes 17:40 mins, so 35:20 total
    return 35*60 + 20
