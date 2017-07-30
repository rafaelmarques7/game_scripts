"""
This is the main file.
It should produce the webdriver.
It is responsible for calling any script necessary.
"""
#IMPORTS
from selenium import webdriver
import time
import random
from Login_module import Login
from Construction_module import Construction
from Village_module import Village
from Adventures_module import Adventures
#from Evade_module import Evade
from Time_module import time_functions
from Raids_module import Raids
from Train_troops_module import Train
#_______________________________________________________________________________
HOMEPAGE = 'https://tx3.travian.fr/dorf1.php'
#_______________________________________________________________________________

#Create DRIVER
driver = webdriver.Chrome()     #useful for testing
#driver = webdriver.PhantomJS() #useful for automation (silent driver)

#do login -> directs to main village
driver = Login.login(driver)

sleep_timers = []
while True:
    print "getting homepage"
    driver.get(HOMEPAGE)
    #print "traning maceman"
    #Train.train_maceman(driver)
    print "atacking"
    raid_time = Raids.raid(driver)
    if raid_time != 0:
        sleep_timers.append(time.time() + raid_time)
        sleep_timers = sorted(sleep_timers)
    else:
        SLEEP_TIME = sleep_timers.pop(0) - time.time()
        print "sleeping now for: " + str(SLEEP_TIME)
        time.sleep(SLEEP_TIME + random.randint(30,180))

"""
while True:
    #get village status
    driver.get(HOMEPAGE)
    my_village = Village.Village(driver, HOMEPAGE)

    time_adv = Adventures.adventures_send(driver, my_village.troops)
    time_task = Construction.construct_crops(driver, HOMEPAGE)

    timer_dict = {'crops': time_task, 'adventure': time_adv}
    time_functions.sleep(timer_dict)
"""
