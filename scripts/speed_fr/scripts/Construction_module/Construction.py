from Village_module import Village
import time

def check_if_can_construct(driver, my_village):
    lowest_crop = my_village.lowest_crop
    upgrade_status = Village.upgrade_status(driver, lowest_crop)
    if upgrade_status == 0:
        #means that resources are available
        return 0
    else:
        time_till_resources = upgrade_status
        return time_till_resources

def construct_crops(driver, HOMEPAGE):
    #check if something is constructing
    under_construction = Village.check_construction(driver)
    if under_construction != 0:
        SLEEP_TIME = under_construction
        return SLEEP_TIME
    else:
        #get (update) village status
        my_village = Village.Village(driver, HOMEPAGE)
        #check crops and resources
        upgrade_status = check_if_can_construct(driver, my_village)
        if upgrade_status == 0:
            #upgrade_status == 0 means resources are available; update can proceed
            time_till_complete = Village.update_crop(driver, my_village.lowest_crop)
            return time_till_complete
        else:
            SLEEP_TIME = upgrade_status
            return SLEEP_TIME
