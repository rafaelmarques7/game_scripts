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
    CROPS = {"wood": [], "clay": [], "iron": [], "cereal": [] }
    CROPS = crops_get_info(driver, CROPS)
    return CROPS

def crops_get_info(driver, CROPS_LEVEL):
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
        crop_object = {'lvl': crop_lvl, 'link': crop_link}
        if crop_type == 0:
            CROPS_LEVEL["wood"].append(crop_object)
        elif crop_type == 1:
            CROPS_LEVEL["clay"].append(crop_object)
        elif crop_type == 2:
            CROPS_LEVEL["iron"].append(crop_object)
        else:
            CROPS_LEVEL["cereal"].append(crop_object)
    return CROPS_LEVEL

def translate_crop_text(text):
    """ Bosco == wood; Pozzo = clay; fer = iron; grano = cereal"""
    crop_key_words = ["Bosco", "Pozzo", "fer", "grano"]
    text = text.encode('ascii', 'ignore')
    for pos, crop_ident in enumerate(crop_key_words):
        is_in = text.find(crop_ident)
        if is_in != -1:
            lvl = int(filter(str.isdigit, text))
            return {'crop_pos': pos, 'lvl': lvl}

def lowest_crop_get(crops):
    low_crop = {'res_type': '', 'lvl': 99, 'link': ''}

    for res_type, crops_info in crops.iteritems():
        for item in crops_info:
            lvl, link = item['lvl'], item['link']
            if int(lvl) <= low_crop['lvl']:
                low_crop['res_type'] = res_type
                low_crop['lvl'] = int(lvl)
                low_crop['link'] = link
    if low_crop['lvl'] != 99:
        return low_crop
    return None

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
