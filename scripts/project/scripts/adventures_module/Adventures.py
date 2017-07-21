import time
import ast
from pprint import pprint
MAP_LINK = 'https://tx3.travian.pt/karte.php'

def adventures_find(driver):
    #object to be used
    adventures = []

    #loads page
    driver.get(MAP_LINK)
    page_source = driver.page_source
    time.sleep(3)

    #gets only the interesting part
    identifier_start = '{"elements":[{"x"'
    identifier_end = 'mapMarks:'
    start = page_source.find(identifier_start)
    end = page_source[start:].find(identifier_end)

    adventures_str = page_source[start:start+end].rstrip()
    adventures_dict = ast.literal_eval(adventures_str)
    adventures_dict = adventures_dict[0]

    #iterates over the nested dictionary to obtain the necessary info
    adventures_elem = adventures_dict['elements']
    for i in range(0, len(adventures_elem)):
        adv_coord = {}
        adv_dict = adventures_elem[i]
        for key, val in adv_dict.iteritems():
            if key == "x":
                adv_coord['x'] = val
            elif key == 'y':
                adv_coord['y'] = val
            elif key == 's':
                params_dict = val[0]
                for key, val in params_dict.iteritems():
                    if key == 'parameters':
                        adv_coord['diff'] = val['difficulty']
        #checks if an adventure object was constructed, and appends if it was
        if adv_coord:
            adventures.append(adv_coord)
    return adventures

def adventures_do(driver):
    #gets one adventure from top of the list
    #NOTE: other method could be choosen here, like choose the most diff adventure
    adventures_list = adventures_find(driver)
    adv_info = adventures_list.pop()

    coord_elem = driver.find_element_by_name('x')
    coord_elem.send_keys(adv_info['x'])

    coord_elem = driver.find_element_by_name('y')
    coord_elem.send_keys(adv_info['y'])

    driver.find_element_by_xpath('//*[@value="OK"]').click()

    time.sleep(10)
