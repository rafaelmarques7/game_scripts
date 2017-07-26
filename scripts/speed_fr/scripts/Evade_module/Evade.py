#NOTE: -we should idealy evade atacks doing two things:
#       1) evade troops
#       2) hide resources (->hiding place; -> market place)
from selenium import webdriver
import Raids
import Login
import time
import random
import time_functions
HOMEPAGE = 'https://tx3.travian.fr/dorf1.php'
MEETING_PLACE = 'https://tx3.travian.fr/build.php?tt=1&id=39'

def check_movs_exist(driver):
    return  len(driver.find_elements_by_id('movements')) > 0

def movs_translate(mov_text, mov_timer):
    mov_text = mov_text.lower()
    mov_timer = mov_timer.encode('ascii', 'ignore')
    if mov_text.find('at') != -1:
        return {'atack': mov_timer}
    elif mov_text.find('ass') != -1:
        return {'support': mov_timer}
    elif mov_text.find('av') != -1:
        return {'adventure': mov_timer}
    else:
        print "ERROR: unknown move type: " + mov_text
        return {}

def check_movs(driver):
    #if atacks incoming, return timer; else return False
    moves = []
    movs_list = driver.find_elements_by_class_name('mov')
    timer_path = '//*[@class="dur_r"]/span'
    timer_list = driver.find_elements_by_xpath(timer_path)
    for mov_info, timer_info in zip(movs_list, timer_list):
        mov_text = mov_info.text
        mov_timer = timer_info.get_attribute('value')
        #create move object
        moves.append(movs_translate(mov_text, mov_timer))
    return moves

def incoming_atacks(driver):
    #this function should check if there are incoming atacks; if yes, return atack timer
    movs_exist = check_movs_exist(driver)
    if not movs_exist:
        print "no moves"
        #return None
    #if movement exists, it does not mean its an atack; we need to check the typ
    moves = check_movs(driver)
    print moves

def check_incoming_atacks(driver):
    #check if there are incoming atacks
    incoming = driver.find_elements_by_class_name('att1')
    if len(incoming) > 0:
        #there are incoming atacks, now get the timer!
        #NOTE: when atacks are incoming, they are always in the first position
        #of the situation if the meeting place
        driver.get(MEETING_PLACE)
        div = driver.find_elements_by_class_name('at')
        arr_time = div[0].text
        time_att = time_functions.convert_to_epoch_time(arr_time)
        #now we have the arrival time of the atacks
        #we need to wait till just before the attack, and than send the troops away
        #followed by the canceling of that atack
        print "there is at least one incoming atack"
        avoid_incoming_atacks(driver, time_att)
    else:
        print "no incoming atacks"

def cancel_atack(driver):
    while True:
        time_now = time.time()
        if time_now > time_att + 5:
            #cancel attack
            print 'cancelling atack!'
            abort_div = driver.find_elements_by_class_name('abort')
            if len(abort_div):
                driver.find_element_by_xpath('//*[@class="abort"]/button').click()
            return None

def avoid_incoming_atacks(driver, time_att):
    print 'time now: ' + str(time.time())
    print 'time of incoming atack: ' +str(time_att)
    while True:
        time_now = time.time()
        if time_now + 15 > time_att:
            #send troops
            print "sending atack!"
            Raids.raid(driver)
            cancel_atack(driver)
            return None

def evade_atacks():
    print "creating phantomjs driver"
    driver = webdriver.PhantomJS()
    driver = Login.login(driver)
    print "login sucessful"
    while True:
        driver.get(HOMEPAGE)
        #check incoming atacks calls all functions necessary to avoid the atacks!
        check_incoming_atacks(driver)

        SLEEP_TIME = 5*60 - random.randint(0,60)
        print 'sleeping for: ' + str(SLEEP_TIME)
        time.sleep(SLEEP_TIME)

#execute the evade function!
evade_atacks()
