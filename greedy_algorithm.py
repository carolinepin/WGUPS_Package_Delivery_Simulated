import packages
import hashtable
import truck
import custTime

#Runtime complexity of O(n), calls multiple for loops, but no for loop nests
def loadTruck(truck, HT):
    time1 = custTime.customTime()                   #deadline#1
    time1.setTime(9,0,True)
    time2 = custTime.customTime()                   #deadline#2
    time2.setTime(10, 30, True)
    nullTime = custTime.customTime()                #time 000AM, usually means time was not set
    priority = []                                   #list of package ids in their prioritized order
    inspection = []                                 #list of package ids that have notes on them and must be inspected
    truck2Only = []                                 #list of package ids that can only be on truck 2
    packagesToRemove =[]                            #list of package ids to remove from another list, garbage disposal

    for i in range(1, HT.get_size()+1):             #go through every item of the hashTable
        #print(HT.lookup(i).get_deadline())         #debugging code
        if HT.lookup(i).get_timestampLeftHub() > nullTime:                                      #if the package has been picked up (has a leftHub timestamp, ignore it
            continue
        elif i == 13 or i == 19:                                                                #these 2 packages are part of the special group of packages, but don't have notes for some reason
            priority.append((1,i))
        elif HT.lookup(i).get_note() != '':                                                     #if the package has a note, move it to the inspection list
            inspection.append(i)
        elif HT.lookup(i).get_deadline() <= time1 and HT.lookup(i).get_deadline() > nullTime:   #if the package deadline is on or before the first deadline (and not EOD/Nulltime), assign it the highest priority
            priority.append((0, i))
        elif HT.lookup(i).get_deadline() <= time2 and HT.lookup(i).get_deadline() > time1:      #if the package deadline is between deadline 1 and deadline 2, assign it priority 2
            priority.append((2, i))
        else:
            priority.append((3, i))                                                             #assign all remaining package baseline priority
    priority.sort()
    #print(priority)                                                #debugging code
    adminInspection(HT, inspection, truck2Only, priority)           #runs "administrator simulation", aka it "reads" the notes and has the final say on all lists
    #print(priority)
    if truck.get_TruckID() == 2:                                        #loads truck2 from the truck2Only list
        for i in truck2Only:                                                #go through all the package ids in truck2Only
            #print(f'packages in queue {truck2Only}')
            if len(truck.get_packages()) <= truck.get_maxPackages():        #if the truck is not full, keep piling on the packages
                #print(i)
                packagesToRemove.append(i)                                  #keeps track of which packages need to be removed
                h,m,isAM = truck.packagePickup(i)                           #adds packageid to truck, save time of pickup
                HT.lookup(i).set_timestampLeftHub(h,m,isAM)                 #stamp pick up on package

                #print(f'packages on truck{truck.get_packages()}')
    #print(truck2Only)
    for i in packagesToRemove:  #note, here I could have just reinitialized the array, but some time in the future the truck2only list could be bigger than just 1 pickup
        truck2Only.remove(i)
    packagesToRemove = []
    for i in priority:                                                  #go through all the package ids in priority IN ORDER (higher priority goes first)
        if len(truck.get_packages()) < truck.get_maxPackages():             #if the truck is not full, keep piling on the packages
            h, m, isAM = truck.packagePickup((i[1]))                        #load truck with package id,save time of pickup
            HT.lookup(i[1]).set_timestampLeftHub(h, m, isAM)                #stamp the pickup on package
            packagesToRemove.append(i)                                      #add package id to be erased from priority list

    for i in packagesToRemove:  #note, here I could have just reinitialized the array, but I wanted to build it with size in mind, meaning some time in the future the truck2only list could be bigger than just 1 pickup
        priority.remove(i)
    #print(priority)
    #print(f'Number of boxes loaded is {count}')
    return None

#Runtime complexity of O(n)
def adminInspection(HT, inspectionList, truck2Only, priority):
    for i in inspectionList:
        #print(HT.lookup(i).get_note())                 #debugging code
        if HT.lookup(i).get_note() == 'Delayed on flight---will not arrive to depot until 9:05 am':     #insert delayed packages onto truck 2 list
            truck2Only.insert(0, i)
            #print(HT.lookup(i).get_note())
        elif HT.lookup(i).get_note() == 'Can only be on truck 2':                                       #insert truck 2 only packages to truck2 only list
            truck2Only.append(i)
            #print(HT.lookup(i).get_note())
        elif HT.lookup(i).get_note() == 'Wrong address listed':                                         #correct wrong address'd package and send it to the back of the priority list
            #print(HT.lookup(i).get_streetAdr())
            HT.lookup(i).set_streetAdr('410 S State St')
            priority.append((4, i))
            #print(HT.lookup(i).get_streetAdr())
            #print(HT.lookup(i).get_note())
        else:                                                                                           #the only other type of note it can be is the special grouping note
            #print(i)
            priority.append((1,i))                                                                      #priority 1 is the "grouped up" packages' priority
            #print(HT.lookup(i).get_note())
    #print(truck2Only)
    priority.sort()                                                                                     #can't forget to sort
    #print(priority)
    return None

#Runtime complexity of O(1) no loops
#given the location's location on the 2darray and the destination's location on the 2darray, return the distance from the distance table 2darray
def findDistance(location, destination, distanceTable):
    if location > len(distanceTable) or destination > len(distanceTable):
        print("bad location in distance table")
        return 0
    if location == destination:
        #print('truck is already there')        #debugging code
        return 0
    #print(f'checking to see if row ',{location}, ' is bigger than column ',{destination})  #debugging check
    if location < destination:                   #distance table is half empty, only bottom left is filled, thus this ensures it is always reaching into a slot with a value and not empty
        temp = location
        location = destination
        destination = temp
    return distanceTable[location][destination]

#Runtime complexity of O(n), calls single for loop
#NEAREST NEIGHBOR ALGORITHM
def pathfinder(listofPackageIDs, packageHashTable, adrDict, distanceT, currentLocation):
    bestAdress = ''
    distance = 100.0
    localNum = adrDict.get(currentLocation)                                                 #gets the 2dDistanceTable index for the current truck location
    bestPackage = 0
    for i in listofPackageIDs:                                                              #go through all the package ids on the truck's package list
        #print(f'PackageID {i} is going to {packageHashTable.lookup(i).get_streetAdr()}')       #debugging code
        destNum = adrDict.get(packageHashTable.lookup(i).get_streetAdr())                   #gets the 2dDistanceTable index for the package's destination
        #print(f'package number {i} has the destinationnumber type {type(destNum)}')               #debugging code
        if distance > findDistance(localNum,destNum,distanceT):                             #the following code check to see if the distance return is the smallest  +
            distance = findDistance(localNum,destNum,distanceT)                             #distance encountered. if so, it saves the distance (to be checked in the futher) +
            bestAdress = packageHashTable.lookup(i).get_streetAdr()                         #the package ID number, and the package address that produced the shortest distance
            bestPackage = int(i)
    #print(f'package numver {i} is the nearest drop off and it is {distance}  miles away') #debugging, code check
    return bestAdress, bestPackage,distance