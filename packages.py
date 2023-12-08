import custTime
class Package(object):
    # Runtime complexity of O(1)
    def __init__(self, packageID, streetAdr, city, state, zip, deadline, weight ):
        self.__packageID = packageID
        self.__streetAdr = streetAdr
        self.__city = city
        self.__state = state
        self.__zip = zip
        self.__deadline = custTime.customTime()
        if deadline != 'EOD':                           #the following few lines parse the time in a string into a time object
            deadline = deadline.split(" ")
            deadline[0] = deadline[0].split(":")
            if deadline[1] == 'AM':
                isAM = True
            else:
                isAM = False
            self.__deadline.setTime(int(deadline[0][0]),int(deadline[0][1]), isAM )
        self.__weight = weight
        self.__note = ''
        self.__timestampLeftHub = custTime.customTime()
        self.__timestampDelivered = custTime.customTime()

    #GETTERS START
    # Runtime complexity of O(1)
    def get_packageID(self):
        return self.__packageID

    # Runtime complexity of O(1)
    def get_streetAdr(self):
        return self.__streetAdr

    # Runtime complexity of O(1)
    def get_city(self):
        return self.__city

    # Runtime complexity of O(1)
    def get_state(self):
        return self.__state

    # Runtime complexity of O(1)
    def get_zip(self):
        return self.__zip

    # Runtime complexity of O(1)
    def get_deadline(self):
        return self.__deadline

    # Runtime complexity of O(1)
    def get_weight(self):
        return self.__weight

    # Runtime complexity of O(1)
    def get_note(self):
        return self.__note

    # Runtime complexity of O(1)
    def get_timestampLeftHub(self):
        return self.__timestampLeftHub

    # Runtime complexity of O(1)
    def get_timestampDelivered(self):
        return self.__timestampDelivered

    #GETTERS END
    #SETTERS START
    # Runtime complexity of O(1)
    def set_streetAdr(self, streetAdr):
        self.__streetAdr = streetAdr

    # Runtime complexity of O(1)
    def set_city(self, city):
        self.__city = city

    # Runtime complexity of O(1)
    def set_state(self, state):
        self.__state = state

    # Runtime complexity of O(1)
    def set_zip(self, zip):
        self.__zip = zip

    # Runtime complexity of O(1)
    def set_deadline(self, deadline):
        self.__deadline = deadline

    # Runtime complexity of O(1)
    def set_weight(self, weight):
        self.__weight = weight

    # Runtime complexity of O(1)
    def set_note(self, note):
        self.__note = note

    # Runtime complexity of O(1)
    def set_timestampDelivered(self, h, m, isAM):
        self.__timestampDelivered.setTime(h,m,isAM)

    # Runtime complexity of O(1)
    def set_timestampLeftHub(self, h, m, isAM):
        self.__timestampLeftHub.setTime(h,m,isAM)

    #SETTERS END

    #when package is printed, it prints all of it's relevant info
    # Runtime complexity of O(1)
    def __str__(self): #packageID, streetAdr, city, state, zip, deadline, weight
        printedDeadline = ''
        status = ''
        nullTime = custTime.customTime()
        if self.__deadline  == nullTime:
            printedDeadline = 'EOD'
        else:
            printedDeadline =str(self.__deadline)

        return 'Package ID: ' + format(self.__packageID) + \
               '\n\tAddress: ' + format(self.__streetAdr) + \
               '\n\t\t\t ' + format(self.__city) + ', ' + format(self.__state) + ' '+ format(self.__zip)+ \
               '\n\tDeadline: ' + printedDeadline + \
               '\n\tWeight: ' + format(self.__weight) + \
               '\n\tNote: ' + format(self.__note)


