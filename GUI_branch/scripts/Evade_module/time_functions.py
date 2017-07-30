import time
import random
import datetime

def convert_time(timer):
    hours, mins, secs = int(timer[0:1]), int(timer[2:4]), int(timer[5:])
    timer = secs + mins*60 + hours*3600
    return timer

def convert_hours_mins_secs(timer):
    print timer
    timer = timer.encode('ascii', 'ignore').replace(' ', '')
    print timer
    hours, mins, secs = int(timer[0:2]), int(timer[3:5]), int(timer[6:])
    print hours, mins, secs
    return [int(hours), int(mins), int(secs)]

def convert_to_epoch_time(time_str):
    time_list = convert_hours_mins_secs(time_str)
    hours, mins, secs = time_list[0], time_list[1], time_list[2]
    today = datetime.date.today()
    year, month, day = today.year, today.month, today.day
    #HOURS -1 because travian hours is in french, while python is system hours,
    #which is portuguese!
    d = datetime.datetime(year, month, day, hours -1 , mins, secs)
    epoch_time = time.mktime(d.timetuple())
    return epoch_time

"""
def sleep(time_task, time_adv):
    SLEEP_TIME = min([int(time_adv), int(time_task)])
    SLEEP_TIME = abs(SLEEP_TIME) + random.randint(1,120)
    print 'sleeping for: ' + str(SLEEP_TIME) +' secs'
    if time_adv < time_task:
        print 'waiting for adventure to finish'
    else:
        print 'waiting for task (crop) to finish'
    time.sleep(SLEEP_TIME)
"""

def sleep(movs_dict):
	keys, vals = [], []
	for key, val in some_dict.iteritems():
		keys.append(key)
		vals.append(val)
	min_val = min(vals)
	min_index = vals.index(min(vals))
	print 'waiting for ' + keys[min_index] + ' to finish'
	print 'sleeping for ' + str(min_val) + 'secs'
	time.sleep(min_val)
