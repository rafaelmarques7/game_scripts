#NOTE: -we should idealy evade atacks doing two things:
#       1) evade troops
#       2) hide resources (->hiding place; -> market place)

def check_movs_exist(driver):
    return  len(driver.find_elements_by_id('movements')) > 0

def movs_translate(mov_text, mov_timer):
    mov_text = mov_text.lower()
    if mov_text.find('at') != -1:
        return {'atack': mov_timer}
    elif mov_text.find('ass') != -1:
        return {'support': mov_timer}
    elif mov_text.find('av') != -1:
        return {'adventure': mov_timer}
    else:
        print "ERROR: unknown move type: " + mov_text
        return {}

def check_movs(driver):
    #if atacks incoming, return timer; else return False
    moves = []
    movs_list = driver.find_elements_by_class_name('mov')
    timer_path = '//*[@class="dur_r"]/span'
    timer_list = driver.find_elements_by_xpath(timer_path)
    for mov_info, timer_info in zip(movs_list, timer_list):
        mov_text = mov_info.text
        mov_timer = timer_info.get_attribute('value')
        #create move object
        moves.append(movs_translate(mov_text, mov_timer))
    return moves

def incoming_atacks(driver):
    #this function should check if there are incoming atacks; if yes, return atack timer
    movs_exist = check_movs_exist(driver)
    if not movs_exist:
        print "no moves"
        #return None
    #if movement exists, it does not mean its an atack; we need to check the typ
    moves = check_movs(driver)
    print moves
