#Name: Darien Latjandu
#Matr.-Nr.: 928543

## import libraries
import json
import simplekml
import csv
import numpy as np
# import torch
# import torch.nn as nn
# import math

row = 0

def generatePath(month, day, time):
    if month < 10:
        smonth = "0" + str(month)
    else:
        smonth = str(month)
    
    if day < 10:
        sday = "0" + str(month)
    else:
        sday = str(day)
    
    if time < 10:
        stime = "0" + str(time)
    else:
        stime = str(time)
    filepath = "C://Users//darie//Documents//FH//2022//" + smonth + "//" + sday + "//2022-" + smonth + "-" + sday + "-" + stime + ".txt"
    
    return filepath
    

def comp(month, day, time):
    global row, tempList
    
    filepath = generatePath(month, day, time)
    try:
        with open(filepath) as fh:
            for line in fh:
                
                tempjsonline = json.loads(line)
                # print (tempjsonline)
                hour = int(tempjsonline['internal-time'][11:13])
                if hour == 0:
                    hour = 24
                # print(hour)
                minute = int(tempjsonline['internal-time'][14:16])
                # print(minute)
                second = int(tempjsonline['internal-time'][17:19])
                # print(second)
                if hour == 1 and minute == 0 and second == 0:
                    time = 25 * 60 * 60
                else:
                    time = second + ((hour * 60 + minute) * 60)    
                # print(time)
                
                jsonline = tempjsonline['gps']
                # print(jsonline)
                lat = float(jsonline['lat'])
                # print(lat)
                lon = float(jsonline['lon'])
                # print(lon)
                # in the file, speed and heading is written with the unit 
                # which can be ignored here
                speed = float(jsonline['speed'][:-5])
                # print(speed)
                heading = float(jsonline['heading'][:-10])
                # print(heading)
                
                if row == 0:
                    tempList = [[lat, lon, speed, heading, time]]
                else:
                    tempList.append([lat, lon, speed, heading, time])
                
                
                row += 1
    except:
        print(filepath + " did not exist so skip")

def between(val, upperLimit, lowerLimit):
    return val < upperLimit and val > lowerLimit

def sortToTrip():
    
    stopstart = 0
    stopflag = 0
    prevstopend = 0
    stopflag = 0
    global Landtag_FH
    global FH_Geomar
    global Geomar_Landtag
    global unknown
    global tempList
    # # sort the data into the three trips + trip to hbf + unknown
    for row in range(len(tempList)):
        if row > 0:
            if stopflag == 0:
                if tempList[row-1][2] < 0.6:
                    stopstart = row - 1
                    stopflag = 1
            else:
                if tempList[row][2] >= 0.6:
                    # if fake stop
                    if (tempList[row][4] - tempList[stopstart][4]) < 60 and (tempList[row][4] - tempList[stopstart][4]) >= 0:
                        stopflag = 0
                    # if true stop
                    else:
                        #determine trip
                        trip = getTrip(tempList[prevstopend][0], tempList[prevstopend][1], tempList[stopstart][0], tempList[stopstart][1])
                        if trip == 0:
                            prevstopend = row
                            
                        elif trip == 1:
                            while prevstopend < stopstart:
                                Landtag_FH = compileTo(Landtag_FH, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                prevstopend += 1
                            prevstopend = row  
                            
                        elif trip == 2:
                            while prevstopend < stopstart:
                                FH_Geomar = compileTo(FH_Geomar, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                prevstopend += 1
                            prevstopend = row

                        elif trip == 3:
                            while prevstopend < stopstart:
                                Geomar_Landtag = compileTo(Geomar_Landtag, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                prevstopend += 1
                            prevstopend = row

                        else:
                            while prevstopend < stopstart:
                                unknown = compileTo(unknown, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                prevstopend += 1
                            prevstopend = row
                        
                        stopflag = 0

def getTrip(latStart, lonStart, latStop, lonStop):

    # near Landtag will be defined as
    # Lat between 54.334000 to 54.332000
    # Lon between 10.154000 to 10.152000
    # near FH will be defined as
    # Lat 54.329500 to 54.328900
    # Lon 10.178900 to 10.177800
    # near Geomar is defined as
    # Lat 54.328400 to 54.327500
    # Lon 10.183000 to 10.181500
    # near HBF is defined as
    # Lat 54.315800 to 54.315400
    # Lon 10.135000 to 10.134700

    # if starting position is near Landtag
    if between(latStart, 54.334, 54.332) and between(lonStart, 10.154, 10.152):
        # check stop position
        # if stop position near HBF then trip 0
        # if stop position near FH then trip 1
        # if stop position near Geomar then trip 3        
        # else trip 4
        if between(latStop, 54.3158, 54.3154) and between(lonStop, 10.135, 10.1347):
            trip = 0
        elif between(latStop, 54.3295, 54.3289) and between(lonStop, 10.1789, 10.1778):
            trip = 1
        # elif between(latStop, 54.3284, 54.3275) and between(lonStop, 10.183, 10.1815):
        #     trip = 3
        else:
            trip = 4
    # if starting position is near FH
    elif between(latStart, 54.3295, 54.3289) and between(lonStart, 10.1789, 10.1778):
        # if stopping position near Geomar then trip 2
        # if stopping position near Landtag then trip 1
        # else trip 4
        if between(latStop, 54.3284, 54.3275) and between(lonStop, 10.183, 10.1815):
            trip = 2
        # elif between(latStop, 54.334, 54.332) and between(lonStop, 10.154, 10.152):
        #     trip = 1
        else:
            trip = 4
    #if starting position near Geomar
    elif between(latStart, 54.3284, 54.3275) and between(lonStart, 10.183, 10.1815):
        # if stopping position near Landtag then trip 3
        # if stopping position near FH then trip 2
        # else trip 4
        if between(latStop, 54.334, 54.332) and between(lonStop, 10.154, 10.152):
            trip = 3
        # elif between(latStop, 54.3295, 54.3289) and between(lonStop, 10.1789, 10.1778):
            # trip = 2
        else:
            trip = 4
    # elif between(latStart, 54.3158, 54.3154) and between(lonStart, 10.135, 10.1347):
    # else meaning starting position near HBF then trip 0
    else:
        trip = 0

    return trip


def compileTo(List, lat, lon, spd, head):
    if len(List) == 0:
        List = [[lat, lon, spd, head]]
    else:
        List.append([lat, lon, spd, head])
    return List

def meanVector(List):
    sumLat = 0
    sumLon = 0
    sumSpd = 0
    sumHead = 0

    for i in range(len(List)):
        sumLat += List[i][0]
        sumLon += List[i][1]
        sumSpd += List[i][2]
        sumHead += List[i][3]

    meanLat = sumLat / float(len(List)) 
    meanLon = sumLon / float(len(List))
    meanSpd = sumSpd / float(len(List))
    meanHead = sumHead / float(len(List))
    
    return np.array([meanLat, meanLon, meanSpd, meanHead])

# def calculateStandardList(List, meanVector):
#     global standardList
#     for i in range(len(List)):
#         if len(standardList) == 0:
#             standardList = [[List[i][0] - meanVector[0], List[i][1] - meanVector[1], List[i][2] - meanVector[2], List[i][3] - meanVector[3]]]
#         else:
#             standardList.append([List[i][0] - meanVector[0], List[i][1] - meanVector[1], List[i][2] - meanVector[2], List[i][3] - meanVector[3]])
#         return standardList
    
# the cov() function automatically uses the List standardList to calculate the covariance
def cov(var1, var2):
    global standardList
    sumvar1var2 = 0
    for i in range(len(standardList)):
        sumvar1var2 += (standardList[i][var1 - 1] * standardList[i][var2 - 1])
    return (sumvar1var2 / (len(standardList) - 1))

def covMatrix():
    return np.array([[cov(1,1), cov(1,2), cov(1,3), cov(1,4)], 
                     [cov(2,1), cov(2,2), cov(2,3), cov(2,4)], 
                     [cov(3,1), cov(3,2), cov(3,3), cov(3,4)], 
                     [cov(4,1), cov(4,2), cov(4,3), cov(4,4)]])

###############################################################################
####MAIN FUNCTION####
###############################################################################

tempList = []

Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []
unknown = []

row = 0

# trip is a variable to determine direction of trip
# # 0 is Hauptbahnhof to Landtag or Landtag to Hauptbahnhof
# # 1 is Landtag to FH
# # 2 is FH to Geomar
# # 3 is Geomar to Landtag
# # 4 is for unknown(error)
# is set to 0 at the beginning since the first trip is from Hauptbahnhof
trip = 0

#compile the data into a 2D-Array
for month in range(12):
    for day in range(31):
        for time in range(23):
            comp(month + 1, day + 1, time + 1)
    sortToTrip()
    tempList = []

# print(tempList)
# print(Landtag_FH)
# print(FH_Geomar)
# print(Geomar_Landtag)

###############################################################################
# Save result as kml for visual and csv for future use
###############################################################################

# # kml1 = simplekml.Kml()
# # kml2 = simplekml.Kml()
# # kml3 = simplekml.Kml()
# # kml4 = simplekml.Kml()

# # # coords input is [(lon, lat)]
# # for i in range(len(Landtag_FH)):
# #     kml1.newpoint(coords=[(Landtag_FH[i][1], Landtag_FH[i][0])])
    
# # kml1.save("C://Users//darie//Documents//FH//BA//12//Landtag_FH.kml")

# with open("C://Users//darie//Documents//FH//BA//12//Landtag_FH.csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(Landtag_FH)
                            
# # for i in range(len(FH_Geomar)):
# #     kml2.newpoint(coords=[(FH_Geomar[i][1], FH_Geomar[i][0])])
    
# # kml2.save("C://Users//darie//Documents//FH//BA//12//FH_Geomar.kml")

# with open("C://Users//darie//Documents//FH//BA//12//FH_Geomar.csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(FH_Geomar)

# # for i in range(len(Geomar_Landtag)):
# #     kml3.newpoint(coords=[(Geomar_Landtag[i][1], Geomar_Landtag[i][0])])
    
# # kml3.save("C://Users//darie//Documents//FH//BA//12//Geomar_Landtag.kml")
                                                  
# with open("C://Users//darie//Documents//FH//BA//12//Geomar_Landtag.csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(Geomar_Landtag)                 

# # for i in range(len(unknown)):
# #     kml4.newpoint(coords=[(unknown[i][1], unknown[i][0])])
    
# # kml4.save("C://Users//darie//Documents//FH//BA//12//unknown.kml")
                                                  
# with open("C://Users//darie//Documents//FH//BA//12//unknown.csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(unknown)

###############################################################################
#####PREPARING THE DATA FOR TRIP 1 - Landtag_FH#####    
###############################################################################
# standardList = []

# meanVector1 = meanVector(Landtag_FH)

# # to calculate the variance and covariance, the difference between the current 
# # value and the mean will be calculated and stored in a list called standardList
# for i in range(len(Landtag_FH)):
#     standardList = compileTo(standardList, Landtag_FH[i][0] - meanVector1[0], Landtag_FH[i][1] - meanVector1[1], Landtag_FH[i][2] - meanVector1[2], Landtag_FH[i][3] - meanVector1[3])

# # the variance covariance matrix will then be calculated using a function
# varcovarMatrix1 = covMatrix()

# for the other Trip, the same calculation is done with different List

###############################################################################
#####PREPARING THE DATA FOR TRIP 2 - FH_Geomar#####    
###############################################################################

#standardList have to be emptied since it will be used again
# standardList = []

# meanVector2 = meanVector(FH_Geomar)

# # to calculate the variance and covariance, the difference between the current 
# # value and the mean will be calculated and stored in a list called standardList
# for i in range(len(FH_Geomar)):
#     standardList = compileTo(standardList, FH_Geomar[i][0] - meanVector2[0], FH_Geomar[i][1] - meanVector2[1], FH_Geomar[i][2] - meanVector2[2], FH_Geomar[i][3] - meanVector2[3])

# # the variance covariance matrix will then be calculated using a function
# varcovarMatrix2 = covMatrix()

###############################################################################
#####PREPARING THE DATA FOR TRIP 3 - Geomar_Landtag#####    
###############################################################################

#standardList have to be emptied since it will be used again
# standardList = []

# meanVector3 = meanVector(Geomar_Landtag)

# # to calculate the variance and covariance, the difference between the current 
# # value and the mean will be calculated and stored in a list called standardList
# for i in range(len(Geomar_Landtag)):
#     standardList = compileTo(standardList, Geomar_Landtag[i][0] - meanVector3[0], Geomar_Landtag[i][1] - meanVector3[1], Geomar_Landtag[i][2] - meanVector3[2], Geomar_Landtag[i][3] - meanVector3[3])

# # the variance covariance matrix will then be calculated using a function
# varcovarMatrix3 = covMatrix()


###############################################################################
######Old Code######
###############################################################################

# getting the filepath. Replaced with generatePath()
    # if month < 10:
    #     filepath = "C://Users//darie//Documents//FH//BA//12//12//2022-0" + str(month) + "-"
    # else:
    #     filepath = "C://Users//darie//Documents//FH//BA//12//12//2022-" + str(month) + "-"
    
    # if day < 10:
    #     filepath = filepath + "0" + str(day) + "-"
    # else:
    #     filepath = filepath + str(day) + "-"
    
    # if time < 10:
    #     filepath = filepath + "0" + str(time) + ".txt"
    # else:
    #     filepath = filepath + str(time) + ".txt"
        

#Append into a list. Replaced with function compileTo()

# if len(Landtag_FH) == 0:
#     Landtag_FH = [[tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3]]]
# else:
#     Landtag_FH.append([tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3]])
# prevstopend += 1

#not necessary

# if trip is too long meaning the ship did not stop at a certain stop
# in the manualy compiled data from midnight to 6 AM, the longest trip is ca 10 minutes between Geomar and Landtag.
# too long is defined as longer than 12 minutes or 720 seconds
# if the time difference is negative, the trip is overnight
# elif (tempList[stopstart][4] - tempList[prevstopend][4]) < 0 and (tempList[stopstart][4] - tempList[prevstopend][4]) > 660:
#     stopflag = 0
#     #compile it into unknown
#     while prevstopend < stopstart:
#         unknown = compileTo(unknown, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
#         prevstopend += 1
#     prevstopend = row

# requirement of stop and start. the heading term is not necessary

# if math.isclose(tempList[row][3], tempList[row-1][3], rel_tol=1e-6) and tempList[row-1][2] < 0.6:
# if (not math.isclose(tempList[row][3], tempList[row-1][3], rel_tol=1e-6)) or tempList[row][2] >= 0.6:
