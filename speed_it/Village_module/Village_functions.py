import Village_functions as VF
import unidecode

def villages_links_get(driver):
    HOMEPAGE = 'https://ts3.travian.it/dorf1.php'
    driver.get(HOMEPAGE)
    villages = []
    #There are two possibilities:
    #1)either there is only one village
    #    -> xpath = //*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li/a/div
    #2)there are more than one village
    #   -> xpath = //*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li[X]/a/div
    #we want: 1) name, 2)coord
    village_list_el_xpath = '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul'
    village_list_el = driver.find_element_by_xpath(village_list_el_xpath)
    number_villages = len(village_list_el.find_elements_by_tag_name('li'))
    if number_villages == 0:
        print "error getting villages information"
        return None
    elif number_villages == 1:
        xpath = '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li/a'
        link = driver.find_element_by_xpath(xpath).get_attribute('href')
        xpath = '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li/a/div'
        name = driver.find_element_by_xpath(xpath).text
        village = {'name': name, 'link': link}
        villages.append(village)
    else:
        for i in range(1, number_villages +1):
            xpath = '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li[' + str(i) +']/a'
            link = driver.find_element_by_xpath(xpath).get_attribute('href')
            xpath = '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/ul/li[' + str(i) +']/a/div'
            name = driver.find_element_by_xpath(xpath).text
            village = {'name': name, 'link': link}
            villages.append(village)
    return villages

def resources_available_get(driver):
    RESOURCES = {"wood": 0, "clay": 0, "iron": 0, "cereal": 0}
    for i in range(1,5):
        identifier = 'stockBarResource' + str(i)
        resources_div = driver.find_element_by_id(identifier)
        resource = resources_div.text
        resource = resource.encode('ascii', 'ignore')
        if i == 1:
            RESOURCES['wood'] = resource
        elif i == 2:
            RESOURCES['clay'] = resource
        elif i == 3:
            RESOURCES['iron'] = resource
        else:
            RESOURCES['cereal'] = resource
    return RESOURCES

def resources_prod_get(driver):
    PRODUCTION = {"wood": 0, "clay": 0, "iron": 0, "cereal": 0}
    for i in range(1,5):
        xpath = '//*[@id="production"]/tbody/tr[' +str(i) + ']/td[3]'
        prod_table = driver.find_element_by_xpath(xpath)
        prod = prod_table.text
        prod = prod.encode('ascii', 'ignore')
        if i == 1:
            PRODUCTION['wood'] = prod
        elif i == 2:
            PRODUCTION['clay'] = prod
        elif i == 3:
            PRODUCTION['iron'] = prod
        else:
            PRODUCTION['cereal'] = prod
    return PRODUCTION

def crops_get(driver):
    CROPS = crops_get_info(driver)
    return CROPS

def crops_get_info(driver):
    CROPS = []
    for i in range(1, 19):
        identifier = '//*[@id="rx"]/area[' + str(i) + ']'
        crop_div = driver.find_element_by_xpath(identifier)
        crop_text = crop_div.get_attribute('alt')
        #crop info contains now the lvl of crop
        crop_info = translate_crop_text(crop_text)
        #we can also append the link
        crop_part_link = crop_div.get_attribute('href')
        crop_type = crop_info['crop_pos']
        crop_lvl, crop_link = crop_info['lvl'], crop_part_link
        crop_link = crop_link.encode('ascii', 'ignore')
        crop_object = {'res_type': '', 'lvl': crop_lvl, 'link': crop_link, 'identifier': i}
        if crop_type == 0:
            crop_object["res_type"] = 'wood'
        elif crop_type == 1:
            crop_object["res_type"] = 'clay'
        elif crop_type == 2:
            crop_object["res_type"] = 'iron'
        else:
            crop_object["res_type"] = 'cereal'
        CROPS.append(crop_object)
    return CROPS

def translate_crop_text(text):
    """ Bosco == wood; Pozzo = clay; fer = iron; grano = cereal"""
    crop_key_words = ["Bosco", "Pozzo", "fer", "grano"]
    text = text.encode('ascii', 'ignore')
    for pos, crop_ident in enumerate(crop_key_words):
        is_in = text.find(crop_ident)
        if is_in != -1:
            lvl = int(filter(str.isdigit, text))
            return {'crop_pos': pos, 'lvl': lvl}

def troops_av_get(driver, homepage):
    troops = {}
    driver.get(homepage)
    xpath = '//*[@id="troops"]/tbody/tr'
    troops_table = driver.find_elements_by_xpath(xpath)
    if len(troops_table) == 0:
        return troops
    for i in range(1, len(troops_table) + 1):
        troop_name_path = xpath + '[' + str(i) + ']/td[2]'
        troop_num_path = xpath + '[' + str(i) + ']/td[3]'
        troop_name = unidecode.unidecode(driver.find_element_by_xpath(troop_num_path).text)
        troop_num = int(unidecode.unidecode(driver.find_element_by_xpath(troop_name_path).text))
        troops[troop_name] = troop_num
    return troops

def construction_status(driver):
    class_name = 'buildingList'
    construction_box = driver.find_elements_by_class_name(class_name)
    if len(construction_box) > 0:
        return 'busy'
    return 'free'

def building_get(driver):
    driver.get('https://ts3.travian.it/dorf2.php')
    buildings = []
    for i in range(1, 22+1):
        xpath = '//*[@id="clickareas"]/area[' + str(i) + ']'
        el = driver.find_element_by_xpath(xpath)
        name = el.get_attribute('alt')
        name = name.encode('ascii', 'ignore')
        level = 0
        if name.find('level') != -1:
            [name, level] = building_translate(name)
        link = el.get_attribute('href')
        link = link.encode('ascii', 'ignore')
        building = {'name': name, 'lvl': level, 'link': link, 'identifier': i + 18}
        buildings.append(building)
    return buildings

def building_translate(text):
    ident = 'level'
    start = text.find(ident)
    end = text.find('</span>')
    lvl_text = text[start:end]
    lvl_text = lvl_text.encode('ascii', 'ignore')
    lvl = int(filter(str.isdigit, lvl_text))
    name = text[:text.find('<span')]
    return [name, lvl]
