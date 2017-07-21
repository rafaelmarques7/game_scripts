"""
This is the main file.
It should produce the webdriver.
It is responsible for calling any script necessary.
"""
#IMPORTS
from selenium import webdriver
import Login
import Construction
from village_module import Village
from adventures_module import Adventures
#_______________________________________________________________________________
HOMEPAGE = 'https://tx3.travian.pt/dorf1.php'
#_______________________________________________________________________________

#Create DRIVER
driver = webdriver.Chrome()     #usefull for testing
#driver = webdriver.PhantomJS() #usefull for automation (silent driver)

#do login -> directs to main village
driver = Login.login(driver)

#get village status
driver.get(HOMEPAGE)
#my_village = Village.Village(driver, HOMEPAGE)

#here comes the real scripting part
while True:
    #Try to construct stuff
    Construction.construct(driver, HOMEPAGE)
    #DO OTHER STUFF

#adventures = Adventures.adventures_do(driver)

driver.quit()
