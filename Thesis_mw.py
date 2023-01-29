#Name: Darien Latjandu
#Matr.-Nr.: 928543

## import libraries
import json
import simplekml
import csv
import numpy as np
from numpy.linalg import inv
# import torch
# import torch.nn as nn
# import math

###############################################################################
###############FUNCTIONS###################
###############################################################################

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
    

def comp(filepath):
    global row, tempList    
    try:
        with open(filepath) as fh:
            for line in fh:
                
                tempjsonline = json.loads(line)
                # print (tempjsonline)
                strTime = tempjsonline['internal-time']
                
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
                    tempList = [[lat, lon, speed, heading, time, strTime]]
                else:
                    tempList.append([lat, lon, speed, heading, time, strTime])
                
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
    triptime = 0
    global Landtag_FH
    global FH_Geomar
    global Geomar_Landtag
    global unknown
    global tempList
    global Time10pLF
    global Time25pLF
    global Time50pLF
    global Time75pLF
    global Time90pLF
    global Time10pGL
    global Time25pGL
    global Time50pGL
    global Time75pGL
    global Time90pGL
    global Time10pFG
    global Time25pFG
    global Time50pFG
    global Time75pFG
    global Time90pFG
    temp10p = []
    temp25p = []
    temp50p = []
    temp75p = []
    temp90p = []
    temp = []
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
                        else:
                            triptime = tempList[stopstart][4] - tempList[prevstopend][4]
                            T10 = int(0.1 * triptime) + tempList[prevstopend][4]
                            T25 = int(0.25 * triptime) + tempList[prevstopend][4]
                            T50 = int(0.5 * triptime) + tempList[prevstopend][4]
                            T75 = int(0.75 * triptime) + tempList[prevstopend][4]
                            T90 = int(0.9 * triptime) + tempList[prevstopend][4]
                            while prevstopend < stopstart:
                                temp = compileToNoString(temp, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                if tempList[prevstopend][4] == T10:
                                    temp10p = compileToNoString(temp10p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                elif tempList[prevstopend][4] == T25:
                                    temp25p = compileToNoString(temp25p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                elif tempList[prevstopend][4] == T50:
                                    temp50p = compileToNoString(temp50p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                elif tempList[prevstopend][4] == T75:
                                    temp75p = compileToNoString(temp75p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                elif tempList[prevstopend][4] == T90:
                                    temp90p = compileToNoString(temp90p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                prevstopend += 1

                            if trip == 1:
                                Landtag_FH = compile3D(Landtag_FH, temp)
                                Time10pLF = compile3D(Time10pLF, temp10p)
                                Time25pLF = compile3D(Time25pLF, temp25p)
                                Time50pLF = compile3D(Time50pLF, temp50p)
                                Time75pLF = compile3D(Time75pLF, temp75p)
                                Time90pLF = compile3D(Time90pLF, temp90p)
                            elif trip == 2:
                                FH_Geomar = compile3D(FH_Geomar, temp)
                                Time10pFG = compile3D(Time10pFG, temp10p)
                                Time25pFG = compile3D(Time25pFG, temp25p)
                                Time50pFG = compile3D(Time50pFG, temp50p)
                                Time75pFG = compile3D(Time75pFG, temp75p)
                                Time90pFG = compile3D(Time90pFG, temp90p)
                            elif trip == 3:
                                Geomar_Landtag = compile3D(Geomar_Landtag, temp)
                                Time10pGL = compile3D(Time10pGL, temp10p)
                                Time25pGL = compile3D(Time25pGL, temp25p)
                                Time50pGL = compile3D(Time50pGL, temp50p)
                                Time75pGL = compile3D(Time75pGL, temp75p)
                                Time90pGL = compile3D(Time90pGL, temp90p)
                            else:
                                unknown = compile3D(unknown, temp)
                                    
                            prevstopend = row
                        temp10p = []
                        temp25p = []
                        temp50p = []
                        temp75p = []
                        temp90p = []
                        temp = []
                        stopflag = 0
                        
def sortToTripTest():
    
    stopstart = 0
    stopflag = 0
    prevstopend = 0
    stopflag = 0
    triptime = 0
    global Landtag_FH
    global FH_Geomar
    global Geomar_Landtag
    global unknown
    global tempList
    global Time10pLF
    global Time25pLF
    global Time50pLF
    global Time75pLF
    global Time90pLF
    global Time10pGL
    global Time25pGL
    global Time50pGL
    global Time75pGL
    global Time90pGL
    global Time10pFG
    global Time25pFG
    global Time50pFG
    global Time75pFG
    global Time90pFG
    temp10p = []
    temp25p = []
    temp50p = []
    temp75p = []
    temp90p = []
    temp = []
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
                        else:
                            triptime = tempList[stopstart][4] - tempList[prevstopend][4]
                            T10 = int(0.1 * triptime) + tempList[prevstopend][4]
                            T25 = int(0.25 * triptime) + tempList[prevstopend][4]
                            T50 = int(0.5 * triptime) + tempList[prevstopend][4]
                            T75 = int(0.75 * triptime) + tempList[prevstopend][4]
                            T90 = int(0.9 * triptime) + tempList[prevstopend][4]
                            while prevstopend < stopstart:
                                temp = compileTo(temp, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                if tempList[prevstopend][4] == T10:
                                    temp10p = compileTo(temp10p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                elif tempList[prevstopend][4] == T25:
                                    temp25p = compileTo(temp25p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                elif tempList[prevstopend][4] == T50:
                                    temp50p = compileTo(temp50p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                elif tempList[prevstopend][4] == T75:
                                    temp75p = compileTo(temp75p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                elif tempList[prevstopend][4] == T90:
                                    temp90p = compileTo(temp90p, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                prevstopend += 1

                            if trip == 1:
                                Landtag_FH = compile3D(Landtag_FH, temp)
                                Time10pLF = compile3D(Time10pLF, temp10p)
                                Time25pLF = compile3D(Time25pLF, temp25p)
                                Time50pLF = compile3D(Time50pLF, temp50p)
                                Time75pLF = compile3D(Time75pLF, temp75p)
                                Time90pLF = compile3D(Time90pLF, temp90p)
                            elif trip == 2:
                                FH_Geomar = compile3D(FH_Geomar, temp)
                                Time10pFG = compile3D(Time10pFG, temp10p)
                                Time25pFG = compile3D(Time25pFG, temp25p)
                                Time50pFG = compile3D(Time50pFG, temp50p)
                                Time75pFG = compile3D(Time75pFG, temp75p)
                                Time90pFG = compile3D(Time90pFG, temp90p)
                            elif trip == 3:
                                Geomar_Landtag = compile3D(Geomar_Landtag, temp)
                                Time10pGL = compile3D(Time10pGL, temp10p)
                                Time25pGL = compile3D(Time25pGL, temp25p)
                                Time50pGL = compile3D(Time50pGL, temp50p)
                                Time75pGL = compile3D(Time75pGL, temp75p)
                                Time90pGL = compile3D(Time90pGL, temp90p)
                            else:
                                unknown = compile3D(unknown, temp)
                                    
                            prevstopend = row
                        temp10p = []
                        temp25p = []
                        temp50p = []
                        temp75p = []
                        temp90p = []
                        temp = []
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


def compileTo(List, lat, lon, spd, head, strTime):
    if len(List) == 0:
        List = [[lat, lon, spd, head, strTime]]
    else:
        List.append([lat, lon, spd, head, strTime])
    return List

def compileToNoString(List, lat, lon, spd, head):
    if len(List) == 0:
        List = [[lat, lon, spd, head]]
    else:
        List.append([lat, lon, spd, head])
    return List

def compile3D(targetList, toAddList):
    if len(targetList) == 0:
        targetList = [toAddList]
    else:
        targetList.append(toAddList)
    return targetList

def sortLandtag_FH():
    global Landtag_FH, LF
    
    LF01 = []
    LF02 = []
    LF03 = []
    LF04 = []
    LF05 = []
    LF06 = []
    LF07 = []
    LF08 = []
    LF09 = []
    LF10 = []
    LF11 = []
    LF12 = []
    LF13 = []
    LF14 = []
    LF15 = []
    LF16 = []
    LF17 = []
    
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    temp05 = []
    temp06 = []
    temp07 = []
    temp08 = []
    temp09 = []
    temp10 = []
    temp11 = []
    temp12 = []
    temp13 = []
    temp14 = []
    temp15 = []
    temp16 = []
    temp17 = []

    for i in range(len(Landtag_FH)):
        for j in range(len(Landtag_FH[i])):
            if Landtag_FH[i][j][1] < 10.154722:    
                temp01 = compileToNoString(temp01, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.156111:
                temp02 = compileToNoString(temp02, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.157778:
                temp03 = compileToNoString(temp03, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.159167:
                temp04 = compileToNoString(temp04, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.160833:
                temp05 = compileToNoString(temp05, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.162222:
                temp06 = compileToNoString(temp06, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.163611:
                temp07 = compileToNoString(temp07, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.165278:
                temp08 = compileToNoString(temp08, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.166667:  
                temp09 = compileToNoString(temp09, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.168056:
                temp10 = compileToNoString(temp10, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.169722:
                temp11 = compileToNoString(temp11, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.171111:
                temp12 = compileToNoString(temp12, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
            elif Landtag_FH[i][j][1] < 10.172778:
                temp13 = compileToNoString(temp13, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])            
            elif Landtag_FH[i][j][1] < 10.174167:
                temp14 = compileToNoString(temp14, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])            
            elif Landtag_FH[i][j][1] < 10.175556:
                temp15 = compileToNoString(temp15, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])            
            elif Landtag_FH[i][j][1] < 10.177222:
                temp16 = compileToNoString(temp16, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])            
            else:
                temp17 = compileToNoString(temp17, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3])
        
        LF01 = compile3D(LF01, temp01)
        LF02 = compile3D(LF02, temp02)
        LF03 = compile3D(LF03, temp03)
        LF04 = compile3D(LF04, temp04)
        LF05 = compile3D(LF05, temp05)
        LF06 = compile3D(LF06, temp06)
        LF07 = compile3D(LF07, temp07)
        LF08 = compile3D(LF08, temp08)
        LF09 = compile3D(LF09, temp09)
        LF10 = compile3D(LF10, temp10)
        LF11 = compile3D(LF11, temp11)
        LF12 = compile3D(LF12, temp12)
        LF13 = compile3D(LF13, temp13)
        LF14 = compile3D(LF14, temp14)
        LF15 = compile3D(LF15, temp15)
        LF16 = compile3D(LF16, temp16)
        LF17 = compile3D(LF17, temp17)

        temp01 = []
        temp02 = []
        temp03 = []
        temp04 = []
        temp05 = []
        temp06 = []
        temp07 = []
        temp08 = []
        temp09 = []
        temp10 = []
        temp11 = []
        temp12 = []
        temp13 = []
        temp14 = []
        temp15 = []
        temp16 = []
        temp17 = []
        
    LF = [LF01, LF02, LF03, LF04, LF05, LF06, LF07, LF08, LF09, LF10, LF11, LF12, LF13, LF14, LF15, LF16, LF17]
        
def sortGeomar_Landtag():
    global Geomar_Landtag, GL
    
    GL01 = []
    GL02 = []
    GL03 = []
    GL04 = []
    GL05 = []
    GL06 = []
    GL07 = []
    GL08 = []
    GL09 = []
    GL10 = []
    GL11 = []
    GL12 = []
    GL13 = []
    GL14 = []
    GL15 = []
    GL16 = []
    GL17 = []
    GL18 = []
    GL19 = []
    GL20 = []
    
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    temp05 = []
    temp06 = []
    temp07 = []
    temp08 = []
    temp09 = []
    temp10 = []
    temp11 = []
    temp12 = []
    temp13 = []
    temp14 = []
    temp15 = []
    temp16 = []
    temp17 = []
    temp18 = []
    temp19 = []
    temp20 = []
     
    for i in range(len(Geomar_Landtag)):
        for j in range(len(Geomar_Landtag[i])):
            if Geomar_Landtag[i][j][1] < 10.154722:
                temp01 = compileToNoString(temp01, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.156111:
                temp02 = compileToNoString(temp02, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.157778:
                temp03 = compileToNoString(temp03, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.159167:
                temp04 = compileToNoString(temp04, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.160556:
                temp05 = compileToNoString(temp05, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.162222:
                temp06 = compileToNoString(temp06, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.163611:
                temp07 = compileToNoString(temp07, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.165000:
                temp08 = compileToNoString(temp08, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])        
            elif Geomar_Landtag[i][j][1] < 10.166667:
                temp09 = compileToNoString(temp09, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.168056:
                temp10 = compileToNoString(temp10, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.169444:
                temp11 = compileToNoString(temp11, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.171111:
                temp12 = compileToNoString(temp12, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.172500:
                temp13 = compileToNoString(temp13, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])            
            elif Geomar_Landtag[i][j][1] < 10.173889:
                temp14 = compileToNoString(temp14, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])            
            elif Geomar_Landtag[i][j][1] < 10.175278:
                temp15 = compileToNoString(temp15, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])            
            elif Geomar_Landtag[i][j][1] < 10.176944:
                temp16 = compileToNoString(temp16, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.178333:
                temp17 = compileToNoString(temp17, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.179722:
                temp18 = compileToNoString(temp18, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
            elif Geomar_Landtag[i][j][1] < 10.181389:
                temp19 = compileToNoString(temp19, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])            
            else:
                temp20 = compileToNoString(temp20, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3])
                
        GL01 = compile3D(GL01, temp01)
        GL02 = compile3D(GL02, temp02)
        GL03 = compile3D(GL03, temp03)
        GL04 = compile3D(GL04, temp04)
        GL05 = compile3D(GL05, temp05)
        GL06 = compile3D(GL06, temp06)
        GL07 = compile3D(GL07, temp07)
        GL08 = compile3D(GL08, temp08)
        GL09 = compile3D(GL09, temp09)
        GL10 = compile3D(GL10, temp10)
        GL11 = compile3D(GL11, temp11)
        GL12 = compile3D(GL12, temp12)
        GL13 = compile3D(GL13, temp13)
        GL14 = compile3D(GL14, temp14)
        GL15 = compile3D(GL15, temp15)
        GL16 = compile3D(GL16, temp16)
        GL17 = compile3D(GL17, temp17)
        GL18 = compile3D(GL18, temp18)
        GL19 = compile3D(GL19, temp19)
        GL20 = compile3D(GL20, temp20)
        
        temp01 = []
        temp02 = []
        temp03 = []
        temp04 = []
        temp05 = []
        temp06 = []
        temp07 = []
        temp08 = []
        temp09 = []
        temp10 = []
        temp11 = []
        temp12 = []
        temp13 = []
        temp14 = []
        temp15 = []
        temp16 = []
        temp17 = []
        temp18 = []
        temp19 = []
        temp20 = []
        
    GL = [GL01, GL02, GL03, GL04, GL05, GL06, GL07, GL08, GL09, GL10, GL11, GL12, GL13, GL14, GL15, GL16, GL17, GL18, GL19, GL20]

def sortLandtag_FHwithString():
    global Landtag_FH, LF
    
    LF01 = []
    LF02 = []
    LF03 = []
    LF04 = []
    LF05 = []
    LF06 = []
    LF07 = []
    LF08 = []
    LF09 = []
    LF10 = []
    LF11 = []
    LF12 = []
    LF13 = []
    LF14 = []
    LF15 = []
    LF16 = []
    LF17 = []
    
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    temp05 = []
    temp06 = []
    temp07 = []
    temp08 = []
    temp09 = []
    temp10 = []
    temp11 = []
    temp12 = []
    temp13 = []
    temp14 = []
    temp15 = []
    temp16 = []
    temp17 = []

    for i in range(len(Landtag_FH)):
        for j in range(len(Landtag_FH[i])):
            if Landtag_FH[i][j][1] < 10.154722:    
                temp01 = compileTo(temp01, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.156111:
                temp02 = compileTo(temp02, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.157778:
                temp03 = compileTo(temp03, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.159167:
                temp04 = compileTo(temp04, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.160833:
                temp05 = compileTo(temp05, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.162222:
                temp06 = compileTo(temp06, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.163611:
                temp07 = compileTo(temp07, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.165278:
                temp08 = compileTo(temp08, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.166667:  
                temp09 = compileTo(temp09, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.168056:
                temp10 = compileTo(temp10, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.169722:
                temp11 = compileTo(temp11, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.171111:
                temp12 = compileTo(temp12, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.172778:
                temp13 = compileTo(temp13, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])            
            elif Landtag_FH[i][j][1] < 10.174167:
                temp14 = compileTo(temp14, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
            elif Landtag_FH[i][j][1] < 10.175556:
                temp15 = compileTo(temp15, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])            
            elif Landtag_FH[i][j][1] < 10.177222:
                temp16 = compileTo(temp16, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])            
            else:
                temp17 = compileTo(temp17, Landtag_FH[i][j][0], Landtag_FH[i][j][1], Landtag_FH[i][j][2], Landtag_FH[i][j][3], Landtag_FH[i][j][4])
        
        LF01 = compile3D(LF01, temp01)
        LF02 = compile3D(LF02, temp02)
        LF03 = compile3D(LF03, temp03)
        LF04 = compile3D(LF04, temp04)
        LF05 = compile3D(LF05, temp05)
        LF06 = compile3D(LF06, temp06)
        LF07 = compile3D(LF07, temp07)
        LF08 = compile3D(LF08, temp08)
        LF09 = compile3D(LF09, temp09)
        LF10 = compile3D(LF10, temp10)
        LF11 = compile3D(LF11, temp11)
        LF12 = compile3D(LF12, temp12)
        LF13 = compile3D(LF13, temp13)
        LF14 = compile3D(LF14, temp14)
        LF15 = compile3D(LF15, temp15)
        LF16 = compile3D(LF16, temp16)
        LF17 = compile3D(LF17, temp17)

        temp01 = []
        temp02 = []
        temp03 = []
        temp04 = []
        temp05 = []
        temp06 = []
        temp07 = []
        temp08 = []
        temp09 = []
        temp10 = []
        temp11 = []
        temp12 = []
        temp13 = []
        temp14 = []
        temp15 = []
        temp16 = []
        temp17 = []
        
    LF = [LF01, LF02, LF03, LF04, LF05, LF06, LF07, LF08, LF09, LF10, LF11, LF12, LF13, LF14, LF15, LF16, LF17]
        
def sortGeomar_LandtagwithString():
    global Geomar_Landtag, GL
    
    GL01 = []
    GL02 = []
    GL03 = []
    GL04 = []
    GL05 = []
    GL06 = []
    GL07 = []
    GL08 = []
    GL09 = []
    GL10 = []
    GL11 = []
    GL12 = []
    GL13 = []
    GL14 = []
    GL15 = []
    GL16 = []
    GL17 = []
    GL18 = []
    GL19 = []
    GL20 = []
    
    temp01 = []
    temp02 = []
    temp03 = []
    temp04 = []
    temp05 = []
    temp06 = []
    temp07 = []
    temp08 = []
    temp09 = []
    temp10 = []
    temp11 = []
    temp12 = []
    temp13 = []
    temp14 = []
    temp15 = []
    temp16 = []
    temp17 = []
    temp18 = []
    temp19 = []
    temp20 = []
     
    for i in range(len(Geomar_Landtag)):
        for j in range(len(Geomar_Landtag[i])):
            if Geomar_Landtag[i][j][1] < 10.154722:
                temp01 = compileTo(temp01, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.156111:
                temp02 = compileTo(temp02, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.157778:
                temp03 = compileTo(temp03, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.159167:
                temp04 = compileTo(temp04, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.160556:
                temp05 = compileTo(temp05, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.162222:
                temp06 = compileTo(temp06, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.163611:
                temp07 = compileTo(temp07, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.165000:
                temp08 = compileTo(temp08, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])        
            elif Geomar_Landtag[i][j][1] < 10.166667:
                temp09 = compileTo(temp09, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.168056:
                temp10 = compileTo(temp10, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.169444:
                temp11 = compileTo(temp11, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.171111:
                temp12 = compileTo(temp12, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.172500:
                temp13 = compileTo(temp13, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])            
            elif Geomar_Landtag[i][j][1] < 10.173889:
                temp14 = compileTo(temp14, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])            
            elif Geomar_Landtag[i][j][1] < 10.175278:
                temp15 = compileTo(temp15, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])            
            elif Geomar_Landtag[i][j][1] < 10.176944:
                temp16 = compileTo(temp16, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.178333:
                temp17 = compileTo(temp17, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.179722:
                temp18 = compileTo(temp18, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
            elif Geomar_Landtag[i][j][1] < 10.181389:
                temp19 = compileTo(temp19, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])            
            else:
                temp20 = compileTo(temp20, Geomar_Landtag[i][j][0], Geomar_Landtag[i][j][1], Geomar_Landtag[i][j][2], Geomar_Landtag[i][j][3], Geomar_Landtag[i][j][4])
                
        GL01 = compile3D(GL01, temp01)
        GL02 = compile3D(GL02, temp02)
        GL03 = compile3D(GL03, temp03)
        GL04 = compile3D(GL04, temp04)
        GL05 = compile3D(GL05, temp05)
        GL06 = compile3D(GL06, temp06)
        GL07 = compile3D(GL07, temp07)
        GL08 = compile3D(GL08, temp08)
        GL09 = compile3D(GL09, temp09)
        GL10 = compile3D(GL10, temp10)
        GL11 = compile3D(GL11, temp11)
        GL12 = compile3D(GL12, temp12)
        GL13 = compile3D(GL13, temp13)
        GL14 = compile3D(GL14, temp14)
        GL15 = compile3D(GL15, temp15)
        GL16 = compile3D(GL16, temp16)
        GL17 = compile3D(GL17, temp17)
        GL18 = compile3D(GL18, temp18)
        GL19 = compile3D(GL19, temp19)
        GL20 = compile3D(GL20, temp20)
        
        temp01 = []
        temp02 = []
        temp03 = []
        temp04 = []
        temp05 = []
        temp06 = []
        temp07 = []
        temp08 = []
        temp09 = []
        temp10 = []
        temp11 = []
        temp12 = []
        temp13 = []
        temp14 = []
        temp15 = []
        temp16 = []
        temp17 = []
        temp18 = []
        temp19 = []
        temp20 = []
        
    GL = [GL01, GL02, GL03, GL04, GL05, GL06, GL07, GL08, GL09, GL10, GL11, GL12, GL13, GL14, GL15, GL16, GL17, GL18, GL19, GL20]


def meanVector(List):
    sumLat = 0
    sumLon = 0
    sumSpd = 0
    sumHead = 0
    counter = 0
    for i in range(len(List)):
        for j in range(len(List[i])):
            sumLat += List[i][j][0]
            sumLon += List[i][j][1]
            sumSpd += List[i][j][2]
            sumHead += List[i][j][3]
            counter += 1
    meanLat = sumLat / float(counter) 
    meanLon = sumLon / float(counter)
    meanSpd = sumSpd / float(counter)
    meanHead = sumHead / float(counter)
    
    return np.array([meanLat, meanLon, meanSpd, meanHead])

def cov(stdList, var1, var2):
    sumvar1var2 = 0
    for i in range(len(stdList)):
        sumvar1var2 += (stdList[i][var1 - 1] * stdList[i][var2 - 1])
    return (sumvar1var2 / (len(stdList)) - 1)

def covMatrix(stdList):
    return np.array([[cov(stdList,1,1), cov(stdList,1,2), cov(stdList,1,3), cov(stdList,1,4)], 
                     [cov(stdList,2,1), cov(stdList,2,2), cov(stdList,2,3), cov(stdList,2,4)], 
                     [cov(stdList,3,1), cov(stdList,3,2), cov(stdList,3,3), cov(stdList,3,4)], 
                     [cov(stdList,4,1), cov(stdList,4,2), cov(stdList,4,3), cov(stdList,4,4)]])

def meanList(List):
    sumLat = 0
    sumLon = 0
    sumSpd = 0
    sumHead = 0
    resuiltList = []

    for i in range(len(List)):
        for j in range(len(List[i])):
            sumLat += List[i][j][0]
            sumLon += List[i][j][1]
            sumSpd += List[i][j][2]
            sumHead += List[i][j][3]
            
        if len(List[i]) != 0:
            meanLat = sumLat / float(len(List[i])) 
            meanLon = sumLon / float(len(List[i]))
            meanSpd = sumSpd / float(len(List[i]))
            meanHead = sumHead / float(len(List[i]))
        
        sumLat = 0
        sumLon = 0
        sumSpd = 0
        sumHead = 0
        
        resuiltList = compile3D(resuiltList, np.array([meanLat, meanLon, meanSpd, meanHead]))
    
    return resuiltList

def meanListwithString(List):
    sumLat = 0
    sumLon = 0
    sumSpd = 0
    sumHead = 0
    meanTimeStr = ""
    resuiltList = []

    for i in range(len(List)):
        for j in range(len(List[i])):
            sumLat += List[i][j][0]
            sumLon += List[i][j][1]
            sumSpd += List[i][j][2]
            sumHead += List[i][j][3]
            
        if len(List[i]) != 0:
            meanLat = sumLat / float(len(List[i])) 
            meanLon = sumLon / float(len(List[i]))
            meanSpd = sumSpd / float(len(List[i]))
            meanHead = sumHead / float(len(List[i]))
        
        sumLat = 0
        sumLon = 0
        sumSpd = 0
        sumHead = 0
        meanTimeStr = str(List[i][0][4])
        
        resuiltList = compile3D(resuiltList, [meanLat, meanLon, meanSpd, meanHead, meanTimeStr])
    
    return resuiltList

def meanVectorNP(List):
    sumVec = np.array([float(0), float(0), float(0), float(0)])
    for i in range(len(List)):
        sumVec += List[i]
    return (sumVec / len(List))

def meanVectorfrom3DList(List):
    sumLat = 0
    sumLon = 0
    sumSpd = 0
    sumHead = 0
    gesLen = 0
    
    for i in range(len(List)):
        for j in range(len(List[i])):
            sumLat += List[i][j][0]
            sumLon += List[i][j][1]
            sumSpd += List[i][j][2]
            sumHead += List[i][j][3]
        gesLen += len(List[i])
    
    meanLat = sumLat / gesLen 
    meanLon = sumLon / gesLen
    meanSpd = sumSpd / gesLen
    meanHead = sumHead / gesLen
    
    return np.array([meanLat, meanLon, meanSpd, meanHead])
    
def covTime(standardList, var1, var2):
    sumvar1var2 = 0
    for i in range(len(standardList)):
        sumvar1var2 += (standardList[i][var1 - 1] * standardList[i][var2 - 1])
    return (sumvar1var2 / (len(standardList)) - 1)

def covMatrixTime(stdList):
    return np.array([[covTime(stdList,1,1), covTime(stdList,1,2), covTime(stdList,1,3), covTime(stdList,1,4)], 
                     [covTime(stdList,2,1), covTime(stdList,2,2), covTime(stdList,2,3), covTime(stdList,2,4)], 
                     [covTime(stdList,3,1), covTime(stdList,3,2), covTime(stdList,3,3), covTime(stdList,3,4)], 
                     [covTime(stdList,4,1), covTime(stdList,4,2), covTime(stdList,4,3), covTime(stdList,4,4)]])

def covMean(stdMeanList, var1, var2):
    sumvar1var2 = 0
    for i in range(len(stdMeanList)):
        sumvar1var2 += (stdMeanList[i][var1 - 1] * stdMeanList[i][var2 - 1])
    return (sumvar1var2 / (len(stdMeanList)) - 1)

def covMatrixMean(stdMeanList):
    return np.array([[covMean(stdMeanList,1,1), covMean(stdMeanList,1,2), covMean(stdMeanList,1,3), covMean(stdMeanList,1,4)], 
                     [covMean(stdMeanList,2,1), covMean(stdMeanList,2,2), covMean(stdMeanList,2,3), covMean(stdMeanList,2,4)], 
                     [covMean(stdMeanList,3,1), covMean(stdMeanList,3,2), covMean(stdMeanList,3,3), covMean(stdMeanList,3,4)], 
                     [covMean(stdMeanList,4,1), covMean(stdMeanList,4,2), covMean(stdMeanList,4,3), covMean(stdMeanList,4,4)]])

# the calculation of the Mahalanobis-Distance
def calculateMahalanobis(mVector, covMatrix, variableValue):
    testValue = np.array([variableValue[0], variableValue[1], variableValue[2], variableValue[3]])
    dValue = testValue - mVector
    mDist = (dValue.T.dot(inv(covMatrix))).dot(dValue)
    return mDist
    
# detect anomalie
def detectAnomaly(mDistance):
    global chiSquaredValue
    if mDistance > chiSquaredValue:
        return True
    else:
        return False

def reportAnomalyTo(AnomalyList, strTime, mDistance):
    print("Anomaly detected at: " + str(strTime))
    if len(AnomalyList) == 0:
        AnomalyList = [[strTime, float(mDistance)]]
    else:
        AnomalyList.append([strTime, float(mDistance)])
    return AnomalyList

def addAnomalyCoordTo(targetList, lat, lon):
    if len(targetList) == 0:
        targetList = [[lat, lon]]
    else:
        targetList.append([lat, lon])
    return targetList
        
def savecsv(sourceList, path):
    with open(str(path), 'w') as f:
        mywriter = csv.writer(f, delimiter=',')
        mywriter.writerows(sourceList)

def saveincsvkml(sourceListCSV, sourceListKML, path):
    kml = simplekml.Kml()
    for i in range(len(sourceListKML)):
        for j in range(len(sourceListKML[i])):
            kml.newpoint(coords=[(sourceListKML[i][j][1], sourceListKML[i][j][0])])
        kml.save(str(path) + "_" + str(i) + ".kml")
        kml = simplekml.Kml()
        
    with open(str(path) + ".csv", 'w') as f:
        mywriter = csv.writer(f, delimiter=',')
        mywriter.writerows(sourceListCSV)

###############################################################################
###############DEFINE VARIABELS##################
###############################################################################

tempList = []
Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []
unknown = []
Time10pLF = []
Time25pLF = []
Time50pLF = []
Time75pLF = []
Time90pLF = []
Time10pFG = []
Time25pFG = []
Time50pFG = []
Time75pFG = []
Time90pFG = []
Time10pGL = []
Time25pGL = []
Time50pGL = []
Time75pGL = []
Time90pGL = []
LF = []
GL = []
temp = []
standardList = []
stdMeanList =  []
meanVectorLF = []
meanVectorFG = []
meanVectorGL = []
covMatLF = []
covMatFG = []
covMatGL = []
mvListLF = []
mvListFG = []
mvListGL = []
mVecLF = []
mVecFG = []
mVecGL = []
covMatrixMeanLF = []
covMatrixMeanFG = []
covMatrixMeanGL = []
tempTime = []
timeVectorLF = []
timeVectorFG = []
timeVectorGL = []
meanVectorTimeLF = []
meanVectorTimeGL = []
meanVectorTimeFG = []
covMatrixTimeLF = []
covMatrixTimeFG = []
covMatrixTimeGL = []


# declare constant chiSquaredValue
# for critical value:
    # 0.99999 = 28.4733
    # 0.9999 = 23.5127 (gathered by using Excel function =CHIINV(0.0001,4))
    # 0.999 = 18.467
    # 0.99  = 13.277
    # 0.975 = 11.143
chiSquaredValue = 28.4733

row = 0
trip = 0
mDist = 0

###############################################################################
############MAIN SORTING TRAINING#############
###############################################################################

# compile the whole list for training
for month in range(12):
    for day in range(31):
        for time in range(23):
            comp(generatePath(month + 1, day + 1, time + 1))
    sortToTrip()
    tempList = []

# # compile the whole list for training without test bias
# for month in range(12):
#     for day in range(31):
#         for time in range(23):
#             if (month != 6):
#                 comp(generatePath(month + 1, day + 1, time + 1))
#             else:
#                 if (day > 16) and (day < 26):
#                     comp(generatePath(month + 1, day + 1, time + 1))
#     sortToTrip()
#     tempList = []
    
#sort the data to smaller part in a trip
sortLandtag_FH()
sortGeomar_Landtag()

###############################################################################
######PREPARING THE DATA FOR TRIP 1 - Landtag_FH#######    
###############################################################################

# prototype calculation (calculation agains each datapoint)

for i in range(len(LF)):
    temp = meanVectorfrom3DList(LF[i])
    meanVectorLF = compile3D(meanVectorLF, temp)
    temp = []

for i in range(len(LF)):
    for j in range(len(LF[i])):
        for k in range(len(LF[i][j])):
            temp = compileToNoString(temp, LF[i][j][k][0] - meanVectorLF[i][0], LF[i][j][k][1] - meanVectorLF[i][1], LF[i][j][k][2] - meanVectorLF[i][2], LF[i][j][k][3] - meanVectorLF[i][3])
    standardList = compile3D(standardList, temp)
    temp = []

for i in range(len(standardList)):
    covMatLF = compile3D(covMatLF, covMatrix(standardList[i]))
standardList = []

# calculation agains the mean of a whole trip
for i in range(len(LF)):
    mvListLF = compile3D(mvListLF, meanList(LF[i]))
for i in range(len(mvListLF)):
    mVecLF = compile3D(mVecLF, meanVectorNP(mvListLF[i]))
for i in range(len(mvListLF)):
    for j in range(len(mvListLF[i])):
        temp = compile3D(temp, (mvListLF[i][j] - mVecLF[i]))
    stdMeanList = compile3D(stdMeanList, temp)
    covMatrixMeanLF = compile3D(covMatrixMeanLF, covMatrixMean(stdMeanList[i]))
    temp = []
stdMeanList = []

# calculation against time
timeVectorLF = [Time10pLF, Time25pLF, Time50pLF, Time75pLF, Time90pLF]
meanVectorTimeLF = [meanVector(Time10pLF), meanVector(Time25pLF), meanVector(Time50pLF), meanVector(Time75pLF), meanVector(Time90pLF)]
for i in range(len(timeVectorLF)):
    for j in range(len(timeVectorLF[i])):
        for k in range(len(timeVectorLF[i][j])):
            tempTime = compileToNoString(tempTime, timeVectorLF[i][j][k][0] - meanVectorTimeLF[i][0], timeVectorLF[i][j][k][1] - meanVectorTimeLF[i][1], timeVectorLF[i][j][k][2] - meanVectorTimeLF[i][2], timeVectorLF[i][j][k][3] - meanVectorTimeLF[i][3])
    standardList = compile3D(standardList, tempTime)
    tempTime =  []
    
for i in range(len(standardList)):
    tempTime = covMatrixTime(standardList[i])
    covMatrixTimeLF = compile3D(covMatrixTimeLF, tempTime)
    tempTime = []
        
standardList = []

###############################################################################
######PREPARING THE DATA FOR TRIP 2 - FH_Geomar#######    
###############################################################################

# prototype calculation (calculation agains each datapoint)

meanVectorFG = meanVectorfrom3DList(FH_Geomar)

for i in range(len(FH_Geomar)):
    for j in range(len(FH_Geomar[i])):
        standardList = compileToNoString(standardList, FH_Geomar[i][j][0] - meanVectorFG[0], FH_Geomar[i][j][1] - meanVectorFG[1], FH_Geomar[i][j][2] - meanVectorFG[2], FH_Geomar[i][j][3] - meanVectorFG[3])
covMatFG = covMatrix(standardList)
standardList = []

# calculation agains the mean of a whole trip
mvListFG = [meanList(FH_Geomar)]
mVecFG = meanVectorNP(mvListFG[0])
for i in range(len(mvListFG[0])):
    if len(stdMeanList) == 0:
        stdMeanList = [mvListFG[0][i] - mVecFG]
    else:
        stdMeanList.append(mvListFG[0][i] - meanVectorFG)
covMatrixMeanFG = covMatrixMean(stdMeanList)
stdMeanList = []

# calculation against time
timeVectorFG = [Time10pFG, Time25pFG, Time50pFG, Time75pFG, Time90pFG]
meanVectorTimeFG = [meanVector(Time10pFG), meanVector(Time25pFG), meanVector(Time50pFG), meanVector(Time75pFG), meanVector(Time90pFG)]
for i in range(len(timeVectorFG)):
    for j in range(len(timeVectorFG[i])):
        for k in range(len(timeVectorFG[i][j])):
            tempTime = compileToNoString(tempTime, timeVectorFG[i][j][k][0] - meanVectorTimeFG[i][0], timeVectorFG[i][j][k][1] - meanVectorTimeFG[i][1], timeVectorFG[i][j][k][2] - meanVectorTimeFG[i][2], timeVectorFG[i][j][k][3] - meanVectorTimeFG[i][3])
    standardList = compile3D(standardList, tempTime)
    tempTime =  []
    
for i in range(len(standardList)):
    tempTime = covMatrixTime(standardList[i])
    covMatrixTimeFG = compile3D(covMatrixTimeFG, tempTime)
    tempTime = []
    
standardList = []

###############################################################################
######PREPARING THE DATA FOR TRIP 3 - Geomar-Landtag#######    
###############################################################################

# prototype calculation (calculation agains each datapoint)

for i in range(len(GL)):
    temp = meanVectorfrom3DList(GL[i])
    meanVectorGL = compile3D(meanVectorGL, temp)
    temp = []

for i in range(len(GL)):
    for j in range(len(GL[i])):
        for k in range(len(GL[i][j])):
            temp = compileToNoString(temp, GL[i][j][k][0] - meanVectorGL[i][0], GL[i][j][k][1] - meanVectorGL[i][1], GL[i][j][k][2] - meanVectorGL[i][2], GL[i][j][k][3] - meanVectorGL[i][3])
    standardList = compile3D(standardList, temp)
    temp = []

for i in range(len(standardList)):
    covMatGL = compile3D(covMatGL, covMatrix(standardList[i]))
standardList = []

# calculation agains the mean of a whole trip
for i in range(len(GL)):
    mvListGL = compile3D(mvListGL, meanList(GL[i]))
for i in range(len(mvListGL)):
    mVecGL = compile3D(mVecGL, meanVectorNP(mvListGL[i]))

for i in range(len(mvListGL)):
    for j in range(len(mvListGL[i])):
        temp = compile3D(temp, (mvListGL[i][j] - mVecGL[i]))
    stdMeanList = compile3D(stdMeanList, temp)
    covMatrixMeanGL = compile3D(covMatrixMeanGL, covMatrixMean(stdMeanList[i]))
    temp = []
stdMeanList = []

# calculation against time
timeVectorGL = [Time10pGL, Time25pGL, Time50pGL, Time75pGL, Time90pGL]
meanVectorTimeGL = [meanVector(Time10pGL), meanVector(Time25pGL), meanVector(Time50pGL), meanVector(Time75pGL), meanVector(Time90pGL)]
for i in range(len(timeVectorGL)):
    for j in range(len(timeVectorGL[i])):
        for k in range(len(timeVectorGL[i][j])):
            tempTime = compileToNoString(tempTime, timeVectorGL[i][j][k][0] - meanVectorTimeGL[i][0], timeVectorGL[i][j][k][1] - meanVectorTimeGL[i][1], timeVectorGL[i][j][k][2] - meanVectorTimeGL[i][2], timeVectorGL[i][j][k][3] - meanVectorTimeGL[i][3])
    standardList = compile3D(standardList, tempTime)
    tempTime =  []
    
for i in range(len(standardList)):
    tempTime = covMatrixTime(standardList[i])
    covMatrixTimeGL = compile3D(covMatrixTimeGL, tempTime)
    tempTime = []
        
standardList = []

# ###############################################################################
# ###########SAVE THE MATRIX AND VECTOR AS CSV##############
# ###############################################################################

# # since after importing the matrix, the numpy.array type object for matrix will
# # be complicated as it is not going to be comma seperated, the matrix is 
# # converted into a list
# tempMat = []
# exMatLF = []
# exMatFG = []
# exMatGL = []

# # Prototyp

# for i in range(len(covMatLF)):
#     for j in range(len(covMatLF[i])):
#         tempMat = compileToNoString(tempMat, covMatLF[i][j][0], covMatLF[i][j][1], covMatLF[i][j][2], covMatLF[i][j][3])
#     exMatLF = compile3D(exMatLF, tempMat)
#     tempMat = []
    
# for i in range(len(covMatFG)):
#     exMatFG = compileToNoString(exMatFG, covMatFG[i][0], covMatFG[i][1], covMatFG[i][2], covMatFG[i][3])

# for i in range(len(covMatGL)):
#     for j in range(len(covMatGL[i])):
#         tempMat = compileToNoString(tempMat, covMatGL[i][j][0], covMatGL[i][j][1], covMatGL[i][j][2], covMatGL[i][j][3])
#     exMatGL = compile3D(exMatGL, tempMat)
#     tempMat = []

# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Landtag_FH_point.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_FH_Geomar_point.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Geomar_Landtag_point.csv")
# savecsv(meanVectorLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Landtag_FH_point.csv")
# savecsv([meanVectorFG], "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_FH_Geomar_point.csv")
# savecsv(meanVectorGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Geomar_Landtag_point.csv")

# for test without bias
# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Landtag_FH_point.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_FH_Geomar_point.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Geomar_Landtag_point.csv")
# savecsv(meanVectorLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Landtag_FH_point.csv")
# savecsv([meanVectorFG], "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_FH_Geomar_point.csv")
# savecsv(meanVectorGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Geomar_Landtag_point.csv")

# exMatLF = []
# exMatFG = []
# exMatGL = []

# # Against mean of a trip

# for i in range(len(covMatrixMeanLF)):
#     for j in range(len(covMatrixMeanLF[i])):
#         tempMat = compileToNoString(tempMat, covMatrixMeanLF[i][j][0], covMatrixMeanLF[i][j][1], covMatrixMeanLF[i][j][2], covMatrixMeanLF[i][j][3])
#     exMatLF = compile3D(exMatLF, tempMat)
#     tempMat = []
    
# for i in range(len(covMatrixMeanFG)):
#     exMatFG = compileToNoString(exMatFG, covMatrixMeanFG[i][0], covMatrixMeanFG[i][1], covMatrixMeanFG[i][2], covMatrixMeanFG[i][3])

# for i in range(len(covMatrixMeanGL)):
#     for j in range(len(covMatrixMeanGL[i])):
#         tempMat = compileToNoString(tempMat, covMatrixMeanGL[i][j][0], covMatrixMeanGL[i][j][1], covMatrixMeanGL[i][j][2], covMatrixMeanGL[i][j][3])
#     exMatGL = compile3D(exMatGL, tempMat)
#     tempMat = []
 
# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Landtag_FH_mean.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_FH_Geomar_mean.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Geomar_Landtag_mean.csv")
# savecsv(mVecLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Landtag_FH_mean.csv")
# savecsv([mVecFG], "C://Users//darie//Documents//FH//BA//Matrix_Vector//_Vector_FH_Geomar_mean.csv")
# savecsv(mVecGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Geomar_Landtag_mean.csv")
   
# for test without bias
# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Landtag_FH_mean.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_FH_Geomar_mean.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Geomar_Landtag_mean.csv")
# savecsv(mVecLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Landtag_FH_mean.csv")
# savecsv([mVecFG], "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_FH_Geomar_mean.csv")
# savecsv(mVecGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Geomar_Landtag_mean.csv")

# exMatLF = []
# exMatFG = []
# exMatGL = []

# # Against Time
# for i in range(len(covMatrixTimeLF)):
#     for j in range(len(covMatrixTimeLF[i])):
#         tempMat = compileToNoString(tempMat, covMatrixTimeLF[i][j][0], covMatrixTimeLF[i][j][1], covMatrixTimeLF[i][j][2], covMatrixTimeLF[i][j][3])
#     exMatLF = compile3D(exMatLF, tempMat)
#     tempMat = []
    
# for i in range(len(covMatrixTimeFG)):
#     for j in range(len(covMatrixTimeFG[i])):
#         tempMat = compileToNoString(tempMat, covMatrixTimeFG[i][j][0], covMatrixTimeFG[i][j][1], covMatrixTimeFG[i][j][2], covMatrixTimeFG[i][j][3])
#     exMatFG = compile3D(exMatFG, tempMat)
#     tempMat = []

# for i in range(len(covMatrixTimeGL)):
#     for j in range(len(covMatrixTimeGL[i])):
#         tempMat = compileToNoString(tempMat, covMatrixTimeGL[i][j][0], covMatrixTimeGL[i][j][1], covMatrixTimeGL[i][j][2], covMatrixTimeGL[i][j][3])
#     exMatGL = compile3D(exMatGL, tempMat)
#     tempMat = []

# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Landtag_FH_time.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_FH_Geomar_time.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Matrix_Geomar_Landtag_time.csv")
# savecsv(meanVectorTimeLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Landtag_FH_time.csv")
# savecsv(meanVectorTimeFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_FH_Geomar_time.csv")
# savecsv(meanVectorTimeGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//Vector_Geomar_Landtag_time.csv")

# for test without bias
# savecsv(exMatLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Landtag_FH_time.csv")
# savecsv(exMatFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_FH_Geomar_time.csv")
# savecsv(exMatGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Matrix_Geomar_Landtag_time.csv")
# savecsv(meanVectorTimeLF, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Landtag_FH_time.csv")
# savecsv(meanVectorTimeFG, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_FH_Geomar_time.csv")
# savecsv(meanVectorTimeGL, "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_Geomar_Landtag_time.csv")

# exMatLF = []
# exMatFG = []
# exMatGL = []

###############################################################################
######REINITIALIZE VARIABLES FOR TEST#######    
###############################################################################

tempList = []
Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []
unknown = []
Time10pLF = []
Time25pLF = []
Time50pLF = []
Time75pLF = []
Time90pLF = []
Time10pFG = []
Time25pFG = []
Time50pFG = []
Time75pFG = []
Time90pFG = []
Time10pGL = []
Time25pGL = []
Time50pGL = []
Time75pGL = []
Time90pGL = []
LF = []
GL = []

mvListLF = []
mvListFG = []
mvListGL = []

row = 0
mDist = 0

Anomaly_point = []
Anomaly_mean = []
# Anomaly_mean_with_pointMV = []
Anomaly_Time = []

tempCoord = []
Anomaly_Coord_point = []
Anomaly_Coord_mean = []
# Anomaly_Coord_mean_with_pointMV = []
Anomaly_Coord_Time = []

###############################################################################
######MAIN FUNCTION TEST#######    
###############################################################################

# gather test datapoins

month = 6
for day in range (18, 27):
    for time in range(23):
        comp(generatePath(month, day, time + 1))
    sortToTripTest()
    tempList = []


sortLandtag_FHwithString()
sortGeomar_LandtagwithString()


# reset the meanList for calculation against mean

for i in range(len(LF)):
    mvListLF = compile3D(mvListLF, meanListwithString(LF[i]))

mvListFG = [meanListwithString(FH_Geomar)]

for i in range(len(GL)):
    mvListGL = compile3D(mvListGL, meanListwithString(GL[i]))

# reset the list for time calculation

timeVectorLF = []
timeVectorFG = []
timeVectorGL = []

timeVectorLF = [Time10pLF, Time25pLF, Time50pLF, Time75pLF, Time90pLF]
timeVectorFG = [Time10pFG, Time25pFG, Time50pFG, Time75pFG, Time90pFG]
timeVectorGL = [Time10pGL, Time25pGL, Time50pGL, Time75pGL, Time90pGL]

# calculate distance and detect anomaly

# distance from mean to point
for i in range(len(LF)):
    for j in range(len(LF[i])):
        for k in range(len(LF[i][j])):
            mDist = calculateMahalanobis(meanVectorLF[i], covMatLF[i], LF[i][j][k])
            if detectAnomaly(mDist):
                tempList = reportAnomalyTo(tempList, LF[i][j][k][4], mDist)
                tempCoord = addAnomalyCoordTo(tempCoord, LF[i][j][k][0], LF[i][j][k][1])
        Anomaly_point = compile3D(Anomaly_point, tempList)
        tempList = []
Anomaly_Coord_point = compile3D(Anomaly_Coord_point, tempCoord)
tempCoord = []
        
for i in range(len(FH_Geomar)):
    for j in range(len(FH_Geomar[i])):
        mDist = calculateMahalanobis(meanVectorFG, covMatFG, FH_Geomar[i][j])
        if detectAnomaly(mDist):
            tempList = reportAnomalyTo(tempList, FH_Geomar[i][j][4], mDist)
            tempCoord = addAnomalyCoordTo(tempCoord, FH_Geomar[i][j][0], FH_Geomar[i][j][1])
        Anomaly_point = compile3D(Anomaly_point, tempList)
        tempList = []
Anomaly_Coord_point = compile3D(Anomaly_Coord_point, tempCoord)
tempCoord = []

for i in range(len(GL)):
    for j in range(len(GL[i])):
        for k in range(len(GL[i][j])):
            mDist = calculateMahalanobis(meanVectorGL[i], covMatGL[i], GL[i][j][k])
            if detectAnomaly(mDist):
                tempList = reportAnomalyTo(tempList, GL[i][j][k][4], mDist)
                tempCoord = addAnomalyCoordTo(tempCoord, GL[i][j][k][0], GL[i][j][k][1])
        Anomaly_point = compile3D(Anomaly_point, tempList)
        tempList = []
Anomaly_Coord_point = compile3D(Anomaly_Coord_point, tempCoord)
tempCoord = []
# distance to mean of a trip (need to add the string somehow)

for i in range(len(mvListLF)):
    for j in range(len(mvListLF[i])):
        mDist = calculateMahalanobis(mVecLF[i], covMatrixMeanLF[i], mvListLF[i][j])
        if detectAnomaly(mDist):
            tempList = reportAnomalyTo(tempList, mvListLF[i][j][4], mDist)
            tempCoord = addAnomalyCoordTo(tempCoord, mvListLF[i][j][0], mvListLF[i][j][1])
    Anomaly_mean = compile3D(Anomaly_mean, tempList)
    tempList = []
Anomaly_Coord_mean = compile3D(Anomaly_Coord_mean, tempCoord)
tempCoord = []
    
for i in range(len(mvListFG)):
    for j in range(len(mvListFG[i])):
        mDist = calculateMahalanobis(mVecFG, covMatrixMeanFG, mvListFG[i][j])
        if detectAnomaly(mDist):
            tempList = reportAnomalyTo(tempList, mvListFG[i][j][4], mDist)
            tempCoord = addAnomalyCoordTo(tempCoord, mvListFG[i][j][0], mvListFG[i][j][1])
    Anomaly_mean = compile3D(Anomaly_mean, tempList)
    tempList = []
Anomaly_Coord_mean = compile3D(Anomaly_Coord_mean, tempCoord)
tempCoord = []
    
for i in range(len(mvListGL)):
    for j in range(len(mvListGL[i])):
        mDist = calculateMahalanobis(mVecGL[i], covMatrixMeanGL[i], mvListGL[i][j])
        if detectAnomaly(mDist):
            tempList = reportAnomalyTo(tempList, mvListGL[i][j][4], mDist)
            tempCoord = addAnomalyCoordTo(tempCoord, mvListGL[i][j][0], mvListGL[i][j][1])
    Anomaly_mean = compile3D(Anomaly_mean, tempList)
    tempList = []
Anomaly_Coord_mean = compile3D(Anomaly_Coord_mean, tempCoord)
tempCoord = []
# distance at time

for i in range(len(timeVectorLF)):
    for j in range(len(timeVectorLF[i])):
        for k in range(len(timeVectorLF[i][j])):
            mDist = calculateMahalanobis(meanVectorTimeLF[i], covMatrixTimeLF[i], timeVectorLF[i][j][k])
            if detectAnomaly(mDist):
                tempList = reportAnomalyTo(tempList, timeVectorLF[i][j][k][4], mDist)
                tempCoord = addAnomalyCoordTo(tempCoord, timeVectorLF[i][j][k][0], timeVectorLF[i][j][k][1])
    Anomaly_Time = compile3D(Anomaly_Time, tempList)
    tempList = []
Anomaly_Coord_Time = compile3D(Anomaly_Coord_Time, tempCoord)
tempCoord = []
    
for i in range(len(timeVectorFG)):
    for j in range(len(timeVectorFG[i])):
        for k in range(len(timeVectorFG[i][j])):
            mDist = calculateMahalanobis(meanVectorTimeFG[i], covMatrixTimeFG[i], timeVectorFG[i][j][k])
            if detectAnomaly(mDist):
                tempList = reportAnomalyTo(tempList, timeVectorFG[i][j][k][4], mDist)
                tempCoord = addAnomalyCoordTo(tempCoord, timeVectorFG[i][j][k][0], timeVectorFG[i][j][k][1])
    Anomaly_Time = compile3D(Anomaly_Time, tempList)
    tempList = []
Anomaly_Coord_Time = compile3D(Anomaly_Coord_Time, tempCoord)
tempCoord = []
    
for i in range(len(timeVectorGL)):
    for j in range(len(timeVectorGL[i])):
        for k in range(len(timeVectorGL[i][j])):
            mDist = calculateMahalanobis(meanVectorTimeGL[i], covMatrixTimeGL[i], timeVectorGL[i][j][k])
            if detectAnomaly(mDist):
                tempList = reportAnomalyTo(tempList, timeVectorGL[i][j][k][4], mDist)
                tempCoord = addAnomalyCoordTo(tempCoord, timeVectorGL[i][j][k][0], timeVectorGL[i][j][k][1])
    Anomaly_Time = compile3D(Anomaly_Time, tempList)
    tempList = []
Anomaly_Coord_Time = compile3D(Anomaly_Coord_Time, tempCoord)
tempCoord = []

###############################################################################
###################SAVE ANOMALY######################
###############################################################################

saveincsvkml(Anomaly_point, Anomaly_Coord_point, "C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Point_kiwo_100m")
saveincsvkml(Anomaly_mean, Anomaly_Coord_mean, "C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Mean_kiwo_100m")
saveincsvkml(Anomaly_Time, Anomaly_Coord_Time, "C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Time_kiwo")

# for non biased test
# saveincsvkml(Anomaly_point, Anomaly_Coord_point, "C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Point_kiwo_100m")
# saveincsvkml(Anomaly_mean, Anomaly_Coord_mean, "C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Mean_kiwo_100m")
# saveincsvkml(Anomaly_Time, Anomaly_Coord_Time, "C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Time_kiwo")