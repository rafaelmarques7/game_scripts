barracks_link = 'https://tx3.travian.fr/build.php?id=32'

def train_maceman(driver):
    driver.get(barracks_link)
    max_troops_xpath = '//*[@id="build"]/form/div/div[1]/div[2]/a'
    driver.find_element_by_xpath(max_troops_xpath).click()

    submit_button_xpath = '//*[@id="s1"]/div/div[2]'
    driver.find_element_by_xpath(submit_button_xpath).click()
    print "traning maceman sucessful!"
