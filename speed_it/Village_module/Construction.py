import time
import Village

def construct(my_v, building_list):
    #check if construction_status
    construction_status = my_v.construction_status
    if construction_status == 'busy':
        return None

    #list of all crops and building
    my_buildings = merge_lists(my_v.crops, my_v.buildings)
    #get one of the items to evolve. holds 'identifier' and 'level'
    to_evolve = get_building(building_list)
    to_evolve_ident, to_evolve_lvl = to_evolve['identifier'], to_evolve['lvl']

    #find building and try to upgrade it
    for b in my_buildings:
        if b['identifier'] == to_evolve_ident:
            link = b['link']
            if b['lvl'] < to_evolve_lvl:
                upgrade(my_v, link)
                print "sent an upgrade order. returning. waiting (i guess)."
                return None
    print "could not find the building. returning"
    return None

def upgrade(my_v, link):
    #create driver and assure the corrent functioning of it -> load village homepage
    driver = my_v.driver
    driver.get(my_v.homepage)
    driver.get(link)

    xpath = "//button[contains(.,'Amplia')]"
    try:
        button = driver.find_element_by_xpath(xpath)
        button.click()
    except:
        print "could not find button to evolve!"

def get_building(l):
    for item in l:
        temp = l.pop(0)
        l.append(temp)
        return item

def merge_lists(l1, l2):
    return l1 + l2
