#IMPORTS
import Login
import Village
import Construction
from pprint import pprint
import time
import random
#_______________________________________________________________________________
#CONSTANTS
HOMEPAGE = 'https://ts3.travian.it/dorf1.php'
#_______________________________________________________________________________

#create browser
driver = Login.login()
#my_vs is a list wih a Village object for each village in the account
my_vs = Village.villages_create(driver)
print my_vs[0]

building_list = [{'identifier': 2, 'lvl': 2}, {'identifier': 3, 'lvl': 1}]
while True:
    #my_vs is a list wih a Village object for each village in the account
    my_vs = Village.villages_create(driver)
    Construction.construct(my_vs[0], building_list)
    time.sleep(random.randint(60,120))
