my_farm_list = [[48,31],[47,44],[42,14],[33,9],[54,40],[53,39],[55,36],[28,11],[55,31],[59,36],[65,17],[45,26],[49,34],[52,38]]

def get_coords():
    x, y =  my_farm_list.pop(0)
    my_farm_list.append([x,y])
    return x, y
