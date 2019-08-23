import datetime
def class_now():
    today = datetime.datetime.today().weekday()
    now = datetime.datetime.now()
    class_now = False
    if today == 0 or today == 2 or today == 3:  #MWTh
        if now.hour >= 15 and now.hour <= 20:
            class_now = True
    elif today == 1:  #Tu
        if now.hour >= 14 and now.hour <= 20:
            class_now = True
    elif today == 5 or today == 6:  #SaSu
        if now.hour >= 10 and now.hour <= 18:
            class_now = True
    #return False
    return class_now
