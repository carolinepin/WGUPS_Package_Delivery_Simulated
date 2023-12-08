class customTime:
    # Runtime complexity of O(1)
    def __init__(self):
        self.__hour = 0
        self.__minute = 0
        self.__AM = True

    # Runtime complexity of O(1)
    def setTime(self, h, min, ampm):
        self.__hour = h
        self.__minute = min
        self.__AM = ampm

    # Runtime complexity of O(1)
    def getTime(self):
        return self.__hour, self.__minute, self.__AM

    # Runtime complexity of O(n)
    def addMinutes(self, min):
        self.__minute += min
        while self.__minute >= 60:
            self.__hour += 1
            self.__minute -= 60

        if self.__hour > 12 and self.__AM is True:
            self.__AM = False
            self.__hour -= 12
        elif self.__hour > 12 and self.__AM is False:
            self.__AM = True
            self.__hour -= 12
        return None

    # Runtime complexity of O(1)
    def __gt__(self, other):
        if self.__AM is True and other.__AM is False:
            return False
        if self.__AM is False and other.__AM is True:
            return True
        if self.__hour > other.__hour:
            return True
        if self.__hour < other.__hour:
            return False
        if self.__minute > other.__minute:
            return True
        else:
            return False

    # Runtime complexity of O(1)
    def __lt__(self, other):
        if self.__AM is True and other.__AM is False:
            return True
        if self.__AM is False and other.__AM is True:
            return False
        if self.__hour > other.__hour:
            return False
        if self.__hour < other.__hour:
            return True
        if self.__minute > other.__minute:
            return False
        else:
            return True

    # Runtime complexity of O(1)
    def __le__(self, other):
        if self.__AM is True and other.__AM is False:
            return True
        if self.__AM is False and other.__AM is True:
            return False
        if self.__hour > other.__hour:
            return False
        if self.__hour < other.__hour:
            return True
        if self.__minute > other.__minute:
            return False
        if self.__minute <= other.__minute:
            return True

    # Runtime complexity of O(1)
    def __eq__(self, other):
        if self.__AM == other.__AM and self.__minute == other.__minute and self.__hour == other.__hour:
            return True
        else:
            return False

    # Runtime complexity of O(1)
    def __str__(self):
        merdian = 'AM'
        if self.__AM is False:
            merdian = 'PM'
        return format(self.__hour) + ':'"{:02d}".format(int(self.__minute)) + merdian


