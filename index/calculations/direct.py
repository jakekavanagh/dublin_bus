def direct(ori, des, dic, route):
    route, ori, des = str(route), str(ori), str(des)
    dir_0, dir_1 = dic[route]['0'], dic[route]['1']
    if ori in dir_0 and des in dir_0:
        return 0
    elif ori in dir_1 and des in dir_1:
        return 1
    else:
        return -1


def routey(route):
    route = str(route)
    if len(route) == 3:
        key = route
    elif len(route) == 2:
        key = '0'+route
    elif len(route) == 1:
        key = '00'+route
    return key


def bare(x):
    while x[0] == '0':
        x = x[1:]
    return x
