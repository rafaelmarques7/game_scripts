import random
from village_module import Village
import time

SLEEPTIME = random.randint(1,60)

def construct(driver, HOMEPAGE):
    driver.get(HOMEPAGE)
    #check if something is constructing
    under_construction = Village.check_construction(driver)
    if not under_construction:
        #get (update) village status
        my_village = Village.Village(driver, HOMEPAGE)
        #check crops and resources
        lowest_crop = my_village.lowest_crop
        upgrade_cost = Village.upgrade_cost(driver, lowest_crop)
        village_availabe = my_village.resources_available
        res_available = Village.compare_res(upgrade_cost, village_availabe)
        #if resources are available -> construct
        if res_available:
            Village.update_crop(driver, lowest_crop)
        else:
            time.sleep(SLEEPTIME)
    else:
        time.sleep(SLEEPTIME)
