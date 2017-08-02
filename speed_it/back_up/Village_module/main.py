#IMPORTS
import Login
import Village
#_______________________________________________________________________________
#CONSTANTS
HOMEPAGE = 'https://ts3.travian.it/dorf1.php'
#_______________________________________________________________________________

#create browser
driver = Login.login()
#my_vs is a list wih a Village object for each village in the account
my_vs = Village.villages_create(driver)
print my_vs[0]
