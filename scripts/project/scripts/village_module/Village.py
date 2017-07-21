import unidecode

CROPS_LINKS = { "wood": ["https://tx3.travian.pt/build.php?id=1", "https://tx3.travian.pt/build.php?id=3", "https://tx3.travian.pt/build.php?id=14", "https://tx3.travian.pt/build.php?id=17"],
                "clay": ["https://tx3.travian.pt/build.php?id=6", "https://tx3.travian.pt/build.php?id=5", "https://tx3.travian.pt/build.php?id=18", "https://tx3.travian.pt/build.php?id=16"],
                "iron": ["https://tx3.travian.pt/build.php?id=7", "https://tx3.travian.pt/build.php?id=11", "https://tx3.travian.pt/build.php?id=10", "https://tx3.travian.pt/build.php?id=4"],
                "cereal": ["https://tx3.travian.pt/build.php?id=2", "https://tx3.travian.pt/build.php?id=8", "https://tx3.travian.pt/build.php?id=9", "https://tx3.travian.pt/build.php?id=12", "https://tx3.travian.pt/build.php?id=13", "https://tx3.travian.pt/build.php?id=15", ]
               }

def upgrade_cost(driver, lowest_crop):
    COST = {"wood": 0, "clay": 0, "iron": 0, "cereal": 0}
    driver.get(lowest_crop['link'])
    for i in range(1,5):
        xpath = '//*[@id="contract"]/div/div/div/span[' + str(i) + ']'
        res_cost = driver.find_element_by_xpath(xpath)
        res_cost = res_cost.text
        res_cost = int(res_cost)
        if i == 1:
            COST['wood'] = res_cost
        elif i == 2:
            COST["clay"] = res_cost
        elif i == 3:
            COST["iron"] = res_cost
        elif i == 4:
            COST["cereal"] = res_cost
    return COST

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
    xpath = "//button[contains(.,'Melhorar')]"
    upgrade_button = driver.find_element_by_xpath(xpath)
    upgrade_button.click()

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

def crops_get_level(driver, CROPS_LINKS, CROPS_LEVEL):
    for res_type, links in CROPS_LINKS.iteritems():
        for link in links:
            driver.get(link)
            xpath = '//*[@id="content"]/h1/span'
            item = driver.find_element_by_xpath(xpath)
            lvl = item.text
            lvl = lvl.encode('ascii', 'ignore')
            lvl = filter( lambda x: x in '0123456789', lvl )
            CROPS_LEVEL[res_type].append(lvl)
    return CROPS_LEVEL

def crops_get_info(driver):
    CROPS_LEVEL = {"wood": [], "clay": [], "iron": [], "cereal": [] }
    CROPS_LEVEL = crops_get_level(driver, CROPS_LINKS, CROPS_LEVEL)
    return CROPS_LEVEL

def check_construction(driver):
    class_name = 'buildingList'
    construction_box = driver.find_elements_by_class_name(class_name)
    print "construction box:"
    print construction_box
    if len(construction_box) > 0:
        return True
    else:
        return False


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
        self.crops_lvl_avg = None
        self.lowest_crop = None
        self.troops = None

    @property
    def resources_available(self):
        return self._resources_available

    @resources_available.setter
    def resources_available(self, val):
        self._resources_available = resources_available_get(self.driver)
        print "Resources available; value: "
        print self._resources_available

    @property
    def resources_prod(self):
        return self._resources_prod

    @resources_prod.setter
    def resources_prod(self, val):
        self._resources_prod = resources_prod_get(self.driver)
        print "Resources Production; value: "
        print self._resources_prod

    @property
    def crops(self):
        return self._crops

    @crops.setter
    def crops(self, val):
        self._crops =  crops_get_info(self.driver)
        print ('crops level:')
        print self._crops

    @property
    def crops_lvl_avg(self):
        return self._crops_lvl_avg

    @crops_lvl_avg.setter
    def crops_lvl_avg(self, val):
        avg_lvl = {"wood": 0, "clay": 0, "iron": 0, "cereal": 0}
        for key, vals in self._crops.iteritems():
            print key
            summ = 0
            for val in vals:
                summ += int(val)
            avg_lvl[key] = summ/len(vals)
        self._crops_lvl_avg = avg_lvl
        print "crops average lvl: "
        print self._crops_lvl_avg

    @property
    def lowest_crop(self):
        return self._lowest_crop

    @lowest_crop.setter
    def lowest_crop(self, val):
        low_crop = {'res_type': '', 'lvl': 99, 'link': ''}

        for res_type, lvls in self._crops.iteritems():
            print res_type, lvls
            for pos, lvl in enumerate(lvls):
                if int(lvl) <= low_crop['lvl']:
                    low_crop['res_type'] = res_type
                    low_crop['lvl'] = int(lvl)
                    low_crop['link'] = CROPS_LINKS[res_type][pos]
        self._lowest_crop = low_crop
        print "lowest crop:"
        print self._lowest_crop

    @property
    def troops(self):
        return self._troops

    @troops.setter
    def troops(self, val):
        self._troops = troops_get(self.driver, self.homepage)
        print self._troops
