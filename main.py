#Caroline Pinheiro 011035475

import truck
import hashtable
import packages
import custTime
from greedy_algorithm import *

# Runtime complexity of O(n^2), nested for loop
#prints 2darray
def print2d(table2d):     #debugging table check
    for i in range(len(table2d)):
        for j in range(len(table2d)):
            if j == 26: print(f'\n')
            else:
                print(table2d[i][j], end = '  ||  ')

# Runtime complexity of O(n)
#cleans up lines from file
def ingestCleanUp(intake_list):       #cleans up the data by removing the empty list items
    while len(intake_list[-1]) == 0:  #while the last item in the intake list empty
        del intake_list[-1]


# Runtime complexity of O(n)
#reads "packages.csv" which is just the excel given, just saved as a csv: fills hash table with package info
def csvReaderPackage(packageHashT):
    #packageHashT = hashtable.HashTable()
    files = "packages.csv"  #packages.csv is the "WGUPS Package File" excel sheet that has has been saved as a csv
    #files = input('Enter a restore filename (should end with .csv) or QUIT to stop:\n')
    #             previous code where user entered file name
    if files.upper() == 'QUIT':
        return None
    else:
        try:

            opened = open(files,  'r')
            for _ in range(11):  #skips the first few visual parts of the csv
                next(opened)
            for line in opened:
                line = line.strip()
                line = line.split(',')
                ingestCleanUp(line)
                #if line[0] == '14':
                    #print(line[7])
                package = packages.Package(int(line[0]),line[1],line[2],line[3],line[4],line[5],int(line[6]))
                if len(line) >= 8:
                    package.set_note(line[7].strip('"'))
                packageHashT.hashInsert(package.get_packageID(), package)

            opened.close()
        except FileNotFoundError:
            print(f'Could not open.')
    return packageHashT

# Runtime complexity of O(n^2), nested for loop
#reads "distancetable.csv" which is just the excel given, just saved as a csv, fills out distanceTable and addressDictionary
def csvReaderDistance(distanceTable, dictOfAddresses):
    files = "distancetable.csv"  #packages.csv is the "WGUPS Package File" excel sheet that has has been saved as a csv
    #files = input('Enter a restore filename (should end with .csv) or QUIT to stop:\n') #previous code where user entered file name

    if files.upper() == 'QUIT':
        return None
    else:
        try:
            opened = open(files,  'r')
            for _ in range(36):  #skips the first few visual parts of the csv
                next(opened)
            count = 0
            dictPlace = 0
            saved = 'test'
            extraQuote = '"'
            for line in opened:
                count += 1
                line = line.strip()
                line = line.split(',')
                ingestCleanUp(line)
                if len(line) == 2:    #pulls out the complete street address line
                    line[1] = line[1][2:]
                    saved = line[1]
                #if line[0][0].isdigit():
                    #if line[0][-1].endswith(extraQuote):
                        #line[0] = line[0][:-1]
                    #saved = line[0]
                if count % 3 == 0: #gets the distance values
                    if line[2] == ' HUB':   #specifically for ingesting the HUB line, as it is the only distance row that does not fit the usual array format
                        line = line[2:]
                        saved = line[0][1:]
                    line[0] = saved  #places address into the first element of a row with that addresses's distances
                    #print(line)  #debugging print row
                    dictOfAddresses[line[0]] = dictPlace
                    line = line[1:]
                    for i, items in enumerate(line):
                        distanceTable[dictPlace][i] = float(line[i])
                        #print(f'{dictPlace} = row number, column number {i} is {distanceTable[dictPlace][i]}')    #debugging print check
                    dictPlace += 1
            opened.close()
        except FileNotFoundError:
            print(f'Could not open.')
    return distanceTable, dictOfAddresses

# Runtime complexity of O(n)
# displays package information to user, all of the packages
def displayPackages(HT,time):
    status = ''
    nullTime = custTime.customTime()
    for i in range(1, HT.get_size()+1):

        print(HT.lookup(i))
        #print(f'Picked up at {HT.lookup(i).get_timestampLeftHub()} and delivered at {HT.lookup(i).get_timestampDelivered()}')

        if time <= HT.lookup(i).get_timestampLeftHub() :
            #print(f'{HT.lookup(i).get_timestampLeftHub()} <= {time} is {HT.lookup(i).get_timestampLeftHub() < time}')
            status = 'At Hub.'
            print(f'\tStatus: {status}')
        elif time > HT.lookup(i).get_timestampLeftHub() and time <= HT.lookup(i).get_timestampDelivered():
            status = 'En Route.'
            print(f'\tStatus: {status} Package was picked up at {HT.lookup(i).get_timestampLeftHub()}')
        else:
            status = 'Delivered.'
            print(f'\tStatus: {status} Package was delivered at {HT.lookup(i).get_timestampDelivered()}')

def displayPackagesCondensed(HT,time):
    status = ''
    nullTime = custTime.customTime()
    for i in range(1, HT.get_size()+1):

        print('Package id:' + format(i), end = '\t')
        #print(f'Picked up at {HT.lookup(i).get_timestampLeftHub()} and delivered at {HT.lookup(i).get_timestampDelivered()}')

        if time <= HT.lookup(i).get_timestampLeftHub() :
            #print(f'{HT.lookup(i).get_timestampLeftHub()} <= {time} is {HT.lookup(i).get_timestampLeftHub() < time}')
            status = 'At Hub.'
            print(f'\tStatus: {status}')
        elif time > HT.lookup(i).get_timestampLeftHub() and time <= HT.lookup(i).get_timestampDelivered():
            status = 'En Route.'
            print(f'\tStatus: {status} Package was picked up at {HT.lookup(i).get_timestampLeftHub()}')
        else:
            status = 'Delivered.'
            print(f'\tStatus: {status} Package was delivered at {HT.lookup(i).get_timestampDelivered()}')

# Runtime complexity of O(n)
# displays package information to user, only the packages with deadlines
def displayDeadlinePackages(HT,time):
    status = ''
    nullTime = custTime.customTime()
    for i in range(1, HT.get_size()+1):
        if HT.lookup(i).get_deadline() > nullTime:

            print(HT.lookup(i))
            #print(f'Picked up at {HT.lookup(i).get_timestampLeftHub()} and delivered at {HT.lookup(i).get_timestampDelivered()}')

            if time <= HT.lookup(i).get_timestampLeftHub() :
                #print(f'{HT.lookup(i).get_timestampLeftHub()} <= {time} is {HT.lookup(i).get_timestampLeftHub() < time}')
                status = 'At Hub.'
                print(f'\tStatus: {status}')
            elif time > HT.lookup(i).get_timestampLeftHub() and time <= HT.lookup(i).get_timestampDelivered():
                status = 'En Route.'
                print(f'\tStatus: {status} Package was picked up at {HT.lookup(i).get_timestampLeftHub()}')
            else:
                status = 'Delivered.'
                print(f'\tStatus: {status} Package was delivered at {HT.lookup(i).get_timestampDelivered()}')

# Runtime complexity of O(1)
# displays package information to user
def displayPackage(HT, packageNumber, time):
    nullTime = custTime.customTime()
    print(HT.lookup(packageNumber))
    status = ''
    #print(f'Picked up at {HT.lookup(packageNumber).get_timestampLeftHub()} and delivered at {HT.lookup(packageNumber).get_timestampDelivered()}')
    if HT.lookup(packageNumber).get_timestampLeftHub() == nullTime and HT.lookup(packageNumber).get_timestampDelivered() == nullTime:
        status = 'At Hub'
    elif time <= HT.lookup(packageNumber).get_timestampLeftHub() :
        status = 'At Hub'
        print(f'\tStatus: {status}')
    elif time > HT.lookup(packageNumber).get_timestampLeftHub() and time <= HT.lookup(packageNumber).get_timestampDelivered():
        status = 'En Route.'
        print(f'\tStatus: {status} Package was picked up at {HT.lookup(packageNumber).get_timestampLeftHub()}')
    else:
        status = 'Delivered.'
        print(f'\tStatus: {status} Package was delivered at {HT.lookup(packageNumber).get_timestampDelivered()}')
    return None



# runtime complexity of O(n^3), while loop calls truck.Drive() method which is O(n^2)
#main body
def main():
    hashtableSize = 40
    packageHashT = hashtable.HashTable(hashtableSize)                                   #initiates hash table with hashtableSize
    finalHT = csvReaderPackage(packageHashT)                                            #sends initialized hash table to csvReaderPackage to populate hashtable
    totalAdrs = 27                                                                      #total number of addresses in the distancetable
    utahDistanceTable = [[0 for i in range(totalAdrs)] for j in range(totalAdrs)]       #learned a valuable lesson: do not initialize with [[None]*27] *27], don't do it.
    utahAdrDict = {}                                                                    #initializes address dictionary, will be used like a phone book
    utahDistanceTable, utahAdrDict = csvReaderDistance(utahDistanceTable, utahAdrDict)  #populates 2d array of distances and the dictionary that will be used to help navigate the 2darray

    finalHT.lookup(25).set_streetAdr('5383 S 900 East #104')  #address was the only one who was recorded as "south" instead of S, so i changed it S to fit the address dictionary
    finalHT.lookup(26).set_streetAdr('5383 S 900 East #104')  #address was the only one who was recorded as "south" instead of S, so i changed it S to fit the address dictionary

    truck1 = truck.Truck()                                          #initialize truck 1
    truck2 = truck.Truck()                                          #initialize truck 2
    truck2.set_TruckID(2)
    truck2.set_time(9,5,True)                                       #truck 2 will be delayed to recieve the packages delayed by the flight

    nullTime = custTime.customTime()                                #sets null time, basically 000AM
    totalPackagesLeft = 0

    for i in range(1, finalHT.get_size()+1):
        if finalHT.lookup(i).get_timestampLeftHub() == nullTime:
            totalPackagesLeft += 1
    while totalPackagesLeft > 0:                                    #while there are still packages to deliver, run the following code
        loadTruck(truck1, finalHT)                                  #load truck1 with the packages for the trip
        loadTruck(truck2, finalHT)                                  #load truck2 with the packages for the trip
        truck1.Drive(finalHT, utahAdrDict, utahDistanceTable)       #have truck1 deliver its packages
        truck2.Drive(finalHT, utahAdrDict, utahDistanceTable)       #have truck2 deliver its packages
        totalPackagesLeft = 0                                       #the following lines check to see if there is a package that has not been picked up yet, AKA its "picked up" timestamp is still null (000AM)
        for i in range(1, finalHT.get_size()+1):
            if finalHT.lookup(i).get_timestampLeftHub() == nullTime:
                #print(finalHT.lookup(i))
                totalPackagesLeft += 1
                #print(totalPackagesLeft)
    #--------------------------------------------------------------------------------------
    #USER MENU
    #-------------------------------------------------------------------------------------
    print("--------------------------------------------------------------------------")
    print('Welcome to the WGUPS Terminal! Please select from the following menu: \n'
            '\t1) Print all package information of all packages at a specific time\n '
            '\t2) Print the information of one package at a specified time \n'
            '\t3) Print all information of all packages with a specified deadline at a specified time\n'
            '\t4) Print Truck Info\n'
            '\t5) All Packages Summary\n'
             '\t0) Quit\n')
    userTime = custTime.customTime()
    userInput = input('Enter number option: \n')
    while userInput != '0':
        if userInput.isdigit() == False:
            print('Bad entry: enter a number')
        elif int(userInput) > 5 or int(userInput) < 0:
            print('Bad entry: enter a number 0 through 5')
        elif int(userInput) == 1:
            print('Enter the time you want to check: \n')
            h = input('Enter hour: \n')
            m = input('Enter minute: \n')
            strisAM = input('Is this AM? Enter yes for AM: \n')
            if strisAM == 'yes':
                isAM = True
            else:
                isAM = False
            if h.isdigit() is False or int(h) > 12 or int(h) < 1 or m.isdigit() is False or int(m) > 60 or int(m) < 0:
                print('Invalid Time')
            else:
                userTime.setTime(int(h), int(m), isAM)
                displayPackages(finalHT,userTime)
        elif int(userInput) == 2:
            packageNumber = input('Enter the package ID of the package you want to check the status of: \n')
            print('Enter the time you want to check: \n')
            h = input('Enter hour: \n')
            m = input('Enter minute: \n')
            strisAM = input('Is this AM? Enter yes for AM: \n')
            if strisAM == 'yes':
                isAM = True
            else:
                isAM = False
            if h.isdigit() is False or int(h) > 12 or int(h) < 1 or m.isdigit() is False or int(m) > 60 or int(m) < 0:
                print('Invalid Time')
            elif packageNumber.isdigit() is False or int(packageNumber) > 40 or int(packageNumber) < 0:
                print('Invalid Package Number')
            else:
                userTime.setTime(int(h), int(m), isAM)
                displayPackage(finalHT, int(packageNumber), userTime)
        elif int(userInput) == 3:
            print('Enter the time you want to check: \n')
            h = input('Enter hour: \n')
            m = input('Enter minute: \n')
            strisAM = input('Is this AM? Enter yes for AM: \n')
            if strisAM == 'yes':
                isAM = True
            else:
                isAM = False
            if h.isdigit() is False or int(h) > 12 or int(h) < 1 or m.isdigit() is False or int(m) > 60 or int(m) < 0:
                print('Invalid Time')
            else:
                userTime.setTime(int(h), int(m), isAM)
                displayDeadlinePackages(finalHT, userTime)
        elif int(userInput) ==4:
            print(f'Truck 1 delivered {truck1.get_deliveredPackages()} packages and drove {truck1.get_milesDriven():.2f} miles')
            print(f'Truck 2 delivered {truck2.get_deliveredPackages()} packages and drove {truck2.get_milesDriven():.2f} miles')
            print(f'Total packages delivered: {truck1.get_deliveredPackages()+truck2.get_deliveredPackages()}\tTotal miles driven: {truck1.get_milesDriven()+truck2.get_milesDriven():.2f}\n\n')
        elif int(userInput) == 5:
            print('Enter the time you want to check: \n')
            h = input('Enter hour: \n')
            m = input('Enter minute: \n')
            strisAM = input('Is this AM? Enter yes for AM: \n')
            if strisAM == 'yes':
                isAM = True
            else:
                isAM = False
            if h.isdigit() is False or int(h) > 12 or int(h) < 1 or m.isdigit() is False or int(m) > 60 or int(m) < 0:
                print('Invalid Time')
            else:
                userTime.setTime(int(h), int(m), isAM)
                displayPackagesCondensed(finalHT, userTime)
        print('Welcome to the WGUPS Terminal! Please select from the following menu: \n'
              '\t1) Print all package information of all packages at a specific time\n '
              '\t2) Print the information of one package at a specified time \n'
              '\t3) Print all information of all packages with a specified deadline at a specified time\n'
              '\t4) Print Truck Info\n'
              '\t5) All Packages Summary\n'
              '\t0) Quit\n')
        userInput = input('Enter number option: \n')
    print('---------------------Thank you for using the WGUPS Terminal. Have a nice day!-----------------------------------------')

    #-----------------------------ALL DEBUGGING CODE I USED IN MAIN-----------------------------------------------------------------
    #may this serve as "good places to check" to the next individual who edits this code and creates bugs/breaks
    # print(f'{truck1} \n {truck2}')
    # utahAdrDict.get(1)
    # tempAdr1 = finalHT.lookup(1).get_streetAdr()
    # tempAdr2 = finalHT.lookup(3).get_streetAdr()
    # print(f'{tempAdr1} has the distance array location of  {utahAdrDict.get(tempAdr1)}')
    # print(f'{tempAdr2} has the distance array location of  {utahAdrDict.get(tempAdr2)}')
    # testPackage = finalHT.lookup(2)
    # print(testPackage.get_streetAdr())
    # print(f'The distance between {tempAdr1} and {tempAdr2} is {findDistance(utahAdrDict.get(tempAdr1),utahAdrDict.get(tempAdr2),utahDistanceTable)}')
    # print(f'the closest address is ')
    # print(pathfinder(truck1packs,finalHT,utahAdrDict,utahDistanceTable,'6351 South 900 East'))
    # print(newTime, otherTime)
    # print(finalHT.lookup(6).get_deadline()>otherTime)
    # truck1.set_packages(truck1packs)
    # print(utahAdrDict)  #debugging code
    # print2d(utahDistanceTable) #debugging code
    # exampleTime = custTime.customTime()
    # displayPackages(finalHT,exampleTime)
    # displayPackage(finalHT, 16,exampleTime)






main()


