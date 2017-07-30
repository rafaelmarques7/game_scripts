import time
import ast
from pprint import pprint
from Time_module import time_functions
from Cleaner_module import Clean_functions
MAP_LINK = 'https://tx3.travian.pt/karte.php'
ADV_LINK = 'https://tx3.travian.fr/hero.php?t=3'
HOMEPAGE = 'https://tx3.travian.fr/dorf1.php'

def hero_in_town(troops):
    if 'Heros' in troops:
        return True
    return False

def hero_health(driver):
    health_bar_xpath = '//*[@id="sidebarBoxHero"]/div[2]/div[2]/div[2]/div[1]/div'
    driver.get(HOMEPAGE)
    health_bar = driver.find_element_by_xpath(health_bar_xpath).getAttribute('style')
    health = Clean_functions.extract_health(health_bar)
    return health

def get_coords(c):
    c = c.encode('ascii', 'ignore')
    x_s, x_e = c.find('x='), c.find('&')
    y_s = c.find('y=')
    x_coord, y_coord = c[x_s:x_e], c[y_s:]
    return [x_coord, y_coord]

def adventures_find(driver):
    adventures_list = []
    driver.get(ADV_LINK)
    #the first elements of each list is just the table header -> disregard it!
    coords_info = driver.find_elements_by_xpath('//a[contains(@href, "karte.php")]')
    duration_info = driver.find_elements_by_class_name('moveTime')
    advs_links_info = driver.find_elements_by_class_name('gotoAdventure')

    coords = [get_coords(c.get_attribute('href')) for c in coords_info[2:]]
    durations = [time_functions.convert_time(d.text) for d in duration_info[1:]]
    adv_links = [l.get_attribute('href') for l in advs_links_info[:]]

    for coord, duration, adv_link in zip(coords, durations, adv_links):
        adv_object = {'coord': coord, 'distance': duration, 'link': adv_link}
        adventures_list.append(adv_object)
    return adventures_list

def adventures_find_closest(adventures):
    distances = [{'pos': n, 'dist': adv['distance']} for n, adv in enumerate(adventures)]
    distances_list = [d['dist'] for d in distances]
    min_index = distances_list.index(min(distances_list))
    return distances[min_index]['pos']

def adventure_start(driver, adventures):
    closest_pos = adventures_find_closest(adventures)
    link = adventures[closest_pos]['link']
    driver.get(link)
    driver.find_element_by_xpath('//*[@type="submit"]').click()
    return 2*adventures[closest_pos]['distance']

def adventures_send(driver, troops):
    adventures = adventures_find(driver)
    #check if hero is available
    if not hero_in_town(troops):
        return 9999
    #allow only adventures if health > 25%
    if hero_health(driver) > 25:
        time_till_complete = adventure_start(driver, adventures)
        return time_till_complete
    #if hero health does not allow adventures, return high value!
    return 9999
