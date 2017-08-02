def extract_health(string):
    #this should only be used if there are only ONE number in string
    #else, it will concatenate all numbers!
    string = string.decode('ascii','ignore')
    return int(filter(str.isdigit, string))
