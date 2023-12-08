import custTime
import hashtable
from greedy_algorithm import *
class Truck(object):
    # Runtime complexity of O(1)
    def __init__(self):
        self._TruckID = 1
        self.__milesDriven = 0
        self.__availability = True
        self.__mph = 18
        self.__maxPackages = 16
        self.__packages = []
        self.__priorityPackages = []
        self.__currentDestination = 'HUB'
        self.__lastLocation = 'HUB'
        self.__deliveredPackages = 0
        self.__time = custTime.customTime()
        self.__time.setTime(8,0,True)

    # INT IS DEPRECATED NOW USE INIT THIS TOOK ME 2 HOURS TO FIND I THOUGHT I WAS LOSING MY MIND
    # also init now doesn't allow multiple initiators

    #GETTERS START
    # Runtime complexity of O(1)
    def get_TruckID(self):
        return self._TruckID

    # Runtime complexity of O(1)
    def get_milesDriven(self):
        return self.__milesDriven

    # Runtime complexity of O(1)
    def get_availability(self):
        return self.__availability

    # Runtime complexity of O(1)
    def get_mph(self):
        return self.__mph

    # Runtime complexity of O(1)
    def get_maxPackages(self):
        return self.__maxPackages

    # Runtime complexity of O(1)
    def get_packages(self):
        return self.__packages

    # Runtime complexity of O(1)
    def get_currentDestination(self):
        return self.__currentDestination

    # Runtime complexity of O(1)
    def get_lastLocation(self):
        return self.__lastLocation

    # Runtime complexity of O(1)
    def get_deliveredPackages(self):
        return self.__deliveredPackages

    #GETTERS END


    #when truck object is printed, it wil return all info about the truck
    # Runtime complexity of O(1)
    def __str__(self):
        return 'Truck ID: ' + format(self._TruckID) + \
               '\n\tMiles Driven: ' + format(self.__milesDriven) + \
               '\n\tAvailability: ' + format(self.__availability) + \
               '\n\tMph: ' + format(self.__mph) + \
               '\n\tMax Number of Packages: ' + format(self.__maxPackages) + \
               '\n\tCurrent Destination: ' + format(self.__currentDestination) + \
               '\n\tLast Location: ' + format(self.__lastLocation) + \
               '\n\tUndelivered Packages: ' + format(self.__deliveredPackages)

    #SETTERS START
    # Runtime complexity of O(1)
    def set_TruckID(self, TruckID):
        self._TruckID = TruckID

    # Runtime complexity of O(1)
    def set_milesDriven(self, milesDriven):
        self.__milesDriven = milesDriven

    # Runtime complexity of O(1)
    def set_availability(self, availability):
        self.__availability = availability

    # Runtime complexity of O(1)
    def set_mph(self, mph):
        self.__mph = mph

    # Runtime complexity of O(1)
    def set_maxPackages(self, maxPackages):
        self.__maxPackages = maxPackages

    # Runtime complexity of O(n)
    def set_packages(self, packages):
        i = 0
        while len(self.__packages) <= self.__maxPackages:
            self.__packages[i] = packages[i]
            i += 1

    # Runtime complexity of O(1)
    def set_currentDestination(self, currentDestination):
        self.__currentDestination = currentDestination

    # Runtime complexity of O(1)
    def set_lastLocation(self, lastLocation):
        self.__lastLocation = lastLocation

    # Runtime complexity of O(1)
    def set_deliveredPackages(self, deliveredPackages):
        self.__deliveredPackages = deliveredPackages

    # Runtime complexity of O(1)
    def set_time(self, h, min, isAM):
        self.__time.setTime(h,min,isAM)

    #SETTERS END

    #Truck Tasks Start

    # Runtime complexity of O(1)
    def packagePickup(self, packageID):
        self.__packages.append(packageID)
        h,m,isAM = self.__time.getTime()
        #print(f'Truck {self._TruckID} is picking up package {packageID} at {self.__time}')
        return h,m,isAM

    # Runtime complexity of O(1)
    def packageDropOff(self, packageID):
        self.__packages.remove(packageID)
        #print(f'Truck {self._TruckID} is dropping off package {packageID} at {self.__time}')
        return None

    #Runtime complexity of O(n^2) because while look here calls pathfinder which has a for loop
    def Drive(self, HT, adrDict, distanceT):
        speed = self.__mph /60                                                                      #sets speed to miles per minute instead of hour
        dropoffTime = custTime.customTime()
        while len(self.__packages) > 0:                                             #while the package list is not empty, keep driving
            self.__lastLocation, nextDelivery, distance = \
                pathfinder(self.__packages,HT,adrDict,distanceT, self.__lastLocation)               #find the package with the shortest distance from the current location
            #print(nextDelivery)                                                                    #debugging code
            self.__milesDriven += distance                                                          #adds distance to miles driven
            travelTime = int((distance/speed) )                                                     #keeps track of how long the drive to the next location took
            #print(f'travel time is {travelTime}')                                                  #debugging code
            self.__time.addMinutes(travelTime)                                                      #changes truck's time to the arrival time at the new location
            #print(self.__time)                                                                     #debugging code
            #print(self.__time.getTime())
            h,m,isAM = self.__time.getTime()                                                        #saves time of arrival to stamp onto delivery
            self.packageDropOff(nextDelivery)                                                       #drops off package
            self.__deliveredPackages += 1                                                           #increments how many packages the truck delivered
            HT.lookup(nextDelivery).set_timestampDelivered(h,m,isAM)                                #stamps delivered package
            #print(HT.lookup(nextDelivery).get_timestampDelivered())                                #debugging code
                                                                                    #going back to hub now
        #print(f'truck going to HUB at time {self.__time}')                                         #debugging code
        distance = findDistance(adrDict.get(self.__lastLocation), 0, distanceT)                     #saves distance it took to drive to the hub
        travelTime = int(distance/speed)                                                            #the travel time from last drop off to hub
        self.__time.addMinutes(travelTime)                                                          #changes truck's time to reflect how long the trip back to the hub took
        self.__lastLocation = 'HUB'                                                                 #changes location back to hub while it picks up packages
        #print(self.__time)
        return None

    #Truck Tasks End
