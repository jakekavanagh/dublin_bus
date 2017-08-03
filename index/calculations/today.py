import datetime as dt


def dayw():
    num = dt.datetime.today().weekday()
    if num == 0:
        word = 'Monday'
    elif num == 1:
        word = 'Tuesday'
    elif num == 2:
        word = 'Wednesday'
    elif num == 3:
        word = 'Thursday'
    elif num == 4:
        word = 'Friday'
    elif num == 5:
        word = 'Saturday'
    elif num == 6:
        word = 'Sunday'
    return word + str(num)
