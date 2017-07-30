import unidecode
import time
from Time_module import time_functions

def upgrade_status(driver, lowest_crop):
    driver.get(lowest_crop['link'])
    error_messages = driver.find_elements_by_class_name("statusMessage")
    if error_messages:
        #resources not available; get time for when it will be
        try:
            identifier = '//*[@class="statusMessage"]/span/span'
            span_div = driver.find_element_by_xpath(identifier)
            time_till_resources = span_div.get_attribute('value')
            return time_till_resources
        except Exception as e:
            print e
        try:
            identifier = '//*[@class="statusMessage"]/span'
            span_div = driver.find_element_by_xpath(identifier)
            time_till_resources = span_div.get_attribute('value')
            return time_till_resources
        except Exception as e:
            print e
        finally:
            return 999
    return 0

def compare_res(upgrade_cost, village_res):
    upgrade_res = []
    available_res = []
    for res_type, res in upgrade_cost.iteritems():
        upgrade_res.append(int(res))
    for res_type, res in village_res.iteritems():
        available_res.append(int(res))

    result = True
    for x, y in zip(available_res, upgrade_res):
        if x < y :
            result = False
    return result

def update_crop(driver, lowest_crop):
    driver.get(lowest_crop['link'])
    construct_time = time_functions.convert_time(driver.find_element_by_class_name('clocks').text)
    #click button to upgrade
    xpath = "//button[contains(.,'liorer')]"
    upgrade_button = driver.find_element_by_xpath(xpath)
    upgrade_button.click()
    return construct_time

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

def translate_crop_text(text):
    """ bucheron == wood; argile = clay; fer = iron; cereales = cereal"""
    crop_key_words = ["cheron", "argile", "fer", "ales"]
    text = text.encode('ascii', 'ignore')
    for pos, crop_ident in enumerate(crop_key_words):
        is_in = text.find(crop_ident)
        if is_in != -1:
            lvl = int(filter(str.isdigit, text))
            return {'crop_pos': pos, 'lvl': lvl}

def crops_get_level(driver, CROPS_LEVEL):
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

def crops_get_info(driver):
    CROPS = {"wood": [], "clay": [], "iron": [], "cereal": [] }
    CROPS = crops_get_level(driver, CROPS)
    return CROPS

def check_construction(driver):
    #we need to return a TIMER for when the construction will be completed
    class_name = 'buildingList'
    construction_box = driver.find_elements_by_class_name(class_name)
    if len(construction_box) > 0:
        identifier = '//*[@class="buildDuration"]/span'
        span_div = driver.find_element_by_xpath(identifier)
        time_till_complete = span_div.get_attribute('value')
        if time_till_complete:
            print time_till_complete
            return time_till_complete
        else:
            #THIS PRINT IS FOR DEBUGGING PURPOSES CASE SOMETHING GOES WRONG
            print "TIME_TILL_COMPLETE is False"
            return 999
    else:
        return 0

def troops_get(driver, homepage):
    troops = {}
    driver.get(homepage)
    xpath = '//*[@id="troops"]/tbody/tr'
    troops_table = driver.find_elements_by_xpath(xpath)
    troops_len = len(troops_table)
    for i in range(1, troops_len + 1):
        troop_name_path = xpath + '[' + str(i) + ']/td[2]'
        troop_num_path = xpath + '[' + str(i) + ']/td[3]'
        troop_name = unidecode.unidecode(driver.find_element_by_xpath(troop_num_path).text)
        troop_num = int(unidecode.unidecode(driver.find_element_by_xpath(troop_name_path).text))
        troops[troop_name] = troop_num
    return troops

class Village(object):
    def __init__(self, driver, HOMEPAGE):
        self.homepage = HOMEPAGE
        self.driver = driver
        self.resources_available = None
        self.resources_prod = None
        self.crops = None
        #self.crops_lvl_avg = None
        self.lowest_crop = None
        self.troops = None

    @property
    def resources_available(self):
        return self._resources_available

    @resources_available.setter
    def resources_available(self, val):
        self._resources_available = resources_available_get(self.driver)

    @property
    def resources_prod(self):
        return self._resources_prod

    @resources_prod.setter
    def resources_prod(self, val):
        self._resources_prod = resources_prod_get(self.driver)

    @property
    def crops(self):
        return self._crops

    @crops.setter
    def crops(self, val):
        self._crops =  crops_get_info(self.driver)


    @property
    def crops_lvl_avg(self):
        return self._crops_lvl_avg

    @crops_lvl_avg.setter
    def crops_lvl_avg(self, val):
        avg_lvl = {"wood": 0, "clay": 0, "iron": 0, "cereal": 0}
        for key, vals in self._crops.iteritems():
            summ = 0
            for val in vals:
                summ += int(val)
            avg_lvl[key] = summ/len(vals)
        self._crops_lvl_avg = avg_lvl


    @property
    def lowest_crop(self):
        return self._lowest_crop

    @lowest_crop.setter
    def lowest_crop(self, val):
        low_crop = {'res_type': '', 'lvl': 99, 'link': ''}
        for res_type, crops_info in self._crops.iteritems():
            for item in crops_info:
                lvl, link = item['lvl'], item['link']
                if int(lvl) <= low_crop['lvl']:
                    low_crop['res_type'] = res_type
                    low_crop['lvl'] = int(lvl)
                    low_crop['link'] = link
        self._lowest_crop = low_crop

    @property
    def troops(self):
        return self._troops

    @troops.setter
    def troops(self, val):
        self._troops = troops_get(self.driver, self.homepage)
