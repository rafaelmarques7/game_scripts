#IMPORTS
import Village_functions as VF
import pprint
#_______________________________________________________________________________
#CONSTANTS
HOMEPAGE = 'https://ts3.travian.it/dorf1.php'
#_______________________________________________________________________________

def villages_create(driver):
    driver.get(HOMEPAGE)
    villages_info = VF.villages_links_get(driver)
    my_villages = []
    for v_info in villages_info:
        my_villages.append(Village(driver, v_info['name'], v_info['link']))
    return my_villages

class Village(object):
    def __init__(self, web_driver, name, homepage):
        self.driver = web_driver
        self.name = name
        self.homepage = homepage
        self.resources_available = None
        self.resources_prod = None
        self.crops = None
        self.lowest_crop = None
        self.troops_av = None
        self.troops_all = None                  #NOTE:missing function
        self.construction_status = VF.construction_status(self.driver)

    @property
    def resources_available(self):
        return self._resources_available

    @resources_available.setter
    def resources_available(self, val):
        self._resources_available = VF.resources_available_get(self.driver)


    @property
    def resources_prod(self):
        return self._resources_prod

    @resources_prod.setter
    def resources_prod(self, val):
        self._resources_prod = VF.resources_prod_get(self.driver)


    @property
    def crops(self):
        return self._crops

    @crops.setter
    def crops(self, val):
        self._crops =  VF.crops_get(self.driver)


    @property
    def lowest_crop(self):
        return self._lowest_crop

    @lowest_crop.setter
    def lowest_crop(self, val):
        self._lowest_crop = VF.lowest_crop_get(self._crops)
        if self._lowest_crop == None:
            print "error getting lowest crop"


    @property
    def troops(self):
        return self._troops

    @troops.setter
    def troops_av(self, val):
        self._troops_av = VF.troops_av_get(self.driver, self.homepage)


    def __repr__(self):
        #return "village - name: {0}, link: {1}, upgrade status: {2}, res prod: {3}, res av: {4}, troops av: {5}, crops: {6}".format(
        #    self.name, self.homepage, self.upgrade_status, self._resources_prod, self._resources_available, self._troops_av, self._crops)
        return "village -\n name: {0},\n link: {1},\n upgrade status: {2},\n res prod: {3},\n res av: {4},\n troops av: {5}\n".format(
            self.name, self.homepage, self.construction_status, self._resources_prod, self._resources_available, self._troops_av)
    def __str__(self):
        #return "village - name: {0}, link: {1}, upgrade status: {2}, res prod: {3}, res av: {4}, troops av: {5}, crops: {6}".format(
        #    self.name, self.homepage, self.upgrade_status, self._resources_prod, self._resources_available, self._troops_av, self._crops)
        return "village -\n name: {0},\n link: {1},\n upgrade status: {2},\n res prod: {3},\n res av: {4},\n troops av: {5}\n".format(
            self.name, self.homepage, self.construction_status, self._resources_prod, self._resources_available, self._troops_av)
