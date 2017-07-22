"""
This is the main file.
It should produce the webdriver.
It is responsible for calling any script necessary.
"""
#IMPORTS
from selenium import webdriver
from Login_module import Login
from Construction_module import Construction
from Village_module import Village
from Adventures_module import Adventures
from Evade_module import Evade
import time
import random
#_______________________________________________________________________________
HOMEPAGE = 'https://tx3.travian.fr/dorf1.php'
#_______________________________________________________________________________

#Create DRIVER
driver = webdriver.Chrome()     #usefull for testing
#driver = webdriver.PhantomJS() #usefull for automation (silent driver)

#do login -> directs to main village
driver = Login.login(driver)

#get village status
driver.get(HOMEPAGE)
my_village = Village.Village(driver, HOMEPAGE)

time_done = time.time()
while True:
    if time.time() > time_done:
        driver.get(HOMEPAGE) #not sure if this get is necessary
        wait_time = Construction.construct_crops(driver, HOMEPAGE)
        time_done = time.time() + int(wait_time) + random.randint(1,120)
        print "waiting: " + str(wait_time) + "secs"
    Evade.incoming_atacks(driver)
