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

while True:
    print "traning maceman"
    Train.train_maceman(driver)
    print "atacking"
    atack_time = Raids.raid(driver)
    print "returning to homepage"
    driver.get(HOMEPAGE)
    print "sleeping now for: " + str(atack_time)
    time.sleep(atack_time + random.randint(63,298))

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
