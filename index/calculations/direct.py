def direct(ori, des, dic):
    dir_0 = dic[str(0)]['index']
    dir_1 = dic[str(1)]['index']
    if ori in dir_0 and des in dir_0:
        return 0
    elif ori in dir_1 and des in dir_1:
        return 1
    else:
        return -1