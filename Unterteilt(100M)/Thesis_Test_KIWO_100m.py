#Name: Darien Latjandu
#Matr.-Nr.: 928543

# libraries import
import numpy as np
from numpy.linalg import inv
import json
import csv
import simplekml

###############################################################################
###########LOAD MATRIX AND VECTORS############
###############################################################################
smeanVectorLF = []
smeanVectorGL = []
scovMatLF = []
scovMatGL = []

with open("C://Users//darie//Documents//FH//BA//ShortTrip//meanVectors_Landtag_FH.csv") as f:
    myreader = csv.reader(f)
    smeanVectorLF = list(myreader)
with open("C://Users//darie//Documents//FH//BA//ShortTrip//meanVectors_Geomar_Landtag.csv") as f:
    myreader = csv.reader(f)
    smeanVectorGL = list(myreader)
with open("C://Users//darie//Documents//FH//BA//ShortTrip//Matrix_Landtag_FH.csv") as f:
    myreader = csv.reader(f)
    scovMatLF = list(myreader)
with open("C://Users//darie//Documents//FH//BA//ShortTrip//Matrix_Geomar_Landtag.csv") as f:
    myreader = csv.reader(f)
    scovMatGL = list(myreader)
    
# convert the input data back into numpy array
meanVectorLF = []
meanVectorGL = []
covMatLF = []
covMatGL = []

for i in range(len(smeanVectorGL)):
    if len(smeanVectorGL[i]) == 4:
        if len(meanVectorGL) == 0:
            meanVectorGL = [np.array([float(smeanVectorGL[i][0]), float(smeanVectorGL[i][1]), float(smeanVectorGL[i][2]), float(smeanVectorGL[i][3])])]
        else:
            meanVectorGL.append(np.array([float(smeanVectorGL[i][0]), float(smeanVectorGL[i][1]), float(smeanVectorGL[i][2]), float(smeanVectorGL[i][3])]))

for i in range(len(smeanVectorLF)):
    if len(smeanVectorLF[i]) == 4:
        if len(meanVectorLF) == 0:
            meanVectorLF = [np.array([float(smeanVectorLF[i][0]), float(smeanVectorLF[i][1]), float(smeanVectorLF[i][2]), float(smeanVectorLF[i][3])])]
        else:
            meanVectorLF.append(np.array([float(smeanVectorLF[i][0]), float(smeanVectorLF[i][1]), float(smeanVectorLF[i][2]), float(smeanVectorLF[i][3])]))

for i in range(len(scovMatGL)):
    if len(scovMatGL[i]) == 4:
        if len(covMatGL) == 0:
            covMatGL = [np.array([[float(scovMatGL[i][0][1:16]), float(scovMatGL[i][0][17:32]), float(scovMatGL[i][0][33:48]), float(scovMatGL[i][0][49:-1])],
                                  [float(scovMatGL[i][1][1:16]), float(scovMatGL[i][1][17:32]), float(scovMatGL[i][1][33:48]), float(scovMatGL[i][1][49:-1])],
                                  [float(scovMatGL[i][2][1:16]), float(scovMatGL[i][2][17:32]), float(scovMatGL[i][2][33:48]), float(scovMatGL[i][2][49:-1])],
                                  [float(scovMatGL[i][3][1:16]), float(scovMatGL[i][3][17:32]), float(scovMatGL[i][3][33:48]), float(scovMatGL[i][3][49:-1])]])]
        else:
            covMatGL.append(np.array([[float(scovMatGL[i][0][1:16]), float(scovMatGL[i][0][17:32]), float(scovMatGL[i][0][33:48]), float(scovMatGL[i][0][49:-1])],
                                      [float(scovMatGL[i][1][1:16]), float(scovMatGL[i][1][17:32]), float(scovMatGL[i][1][33:48]), float(scovMatGL[i][1][49:-1])],
                                      [float(scovMatGL[i][2][1:16]), float(scovMatGL[i][2][17:32]), float(scovMatGL[i][2][33:48]), float(scovMatGL[i][2][49:-1])],
                                      [float(scovMatGL[i][3][1:16]), float(scovMatGL[i][3][17:32]), float(scovMatGL[i][3][33:48]), float(scovMatGL[i][3][49:-1])]]))

for i in range(len(scovMatLF)):
    if len(scovMatLF[i]) == 4:
        if len(covMatLF) == 0:
            covMatLF = [np.array([[float(scovMatLF[i][0][1:16]), float(scovMatLF[i][0][17:32]), float(scovMatLF[i][0][33:48]), float(scovMatLF[i][0][49:-1])],
                                  [float(scovMatLF[i][1][1:16]), float(scovMatLF[i][1][17:32]), float(scovMatLF[i][1][33:48]), float(scovMatLF[i][1][49:-1])],
                                  [float(scovMatLF[i][2][1:16]), float(scovMatLF[i][2][17:32]), float(scovMatLF[i][2][33:48]), float(scovMatLF[i][2][49:-1])],
                                  [float(scovMatLF[i][3][1:16]), float(scovMatLF[i][3][17:32]), float(scovMatLF[i][3][33:48]), float(scovMatLF[i][3][49:-1])]])]
        else:
            covMatLF.append(np.array([[float(scovMatLF[i][0][1:16]), float(scovMatLF[i][0][17:32]), float(scovMatLF[i][0][33:48]), float(scovMatLF[i][0][49:-1])],
                                      [float(scovMatLF[i][1][1:16]), float(scovMatLF[i][1][17:32]), float(scovMatLF[i][1][33:48]), float(scovMatLF[i][1][49:-1])],
                                      [float(scovMatLF[i][2][1:16]), float(scovMatLF[i][2][17:32]), float(scovMatLF[i][2][33:48]), float(scovMatLF[i][2][49:-1])],
                                      [float(scovMatLF[i][3][1:16]), float(scovMatLF[i][3][17:32]), float(scovMatLF[i][3][33:48]), float(scovMatLF[i][3][49:-1])]]))            

# free unused list
smeanVectorLF = []
smeanVectorGL = []
scovMatLF = []
scovMatGL = []

# the trip between Fachhochschule and Geomar is not split into smaller distance
# since it is a relatively small trip
# data taken from calculation done with Thesis_DataSort_Calc_Gesamt_Strecke.py

covMatFG = np.array([[0.00000769667, -0.0000360365, 0.0142871, -0.0134106], 
                     [-0.0000360365, 0.000169001, -0.0665042, 0.0668494], 
                     [0.0142871, -0.0665042, 38.4563, 28.6191], 
                     [-0.0134106, 0.0668494, 28.6191, 3405.32]])


meanVectorFG = np.array([54.3286, 10.181, 6.0379, 105.37])
###############################################################################
##################FUNCTIONS##################
###############################################################################

# import functions to get the test data
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
                                Landtag_FH = compileTo(Landtag_FH, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                prevstopend += 1
                            prevstopend = row  
                            
                        elif trip == 2:
                            while prevstopend < stopstart:
                                FH_Geomar = compileTo(FH_Geomar, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                prevstopend += 1
                            prevstopend = row

                        elif trip == 3:
                            while prevstopend < stopstart:
                                Geomar_Landtag = compileTo(Geomar_Landtag, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                prevstopend += 1
                            prevstopend = row

                        else:
                            while prevstopend < stopstart:
                                unknown = compileTo(unknown, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
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


def compileTo(List, lat, lon, spd, head, strTime):
    if len(List) == 0:
        List = [[lat, lon, spd, head, strTime]]
    else:
        List.append([lat, lon, spd, head, strTime])
    return List

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

    for i in range(len(Landtag_FH)):
        if Landtag_FH[i][1] < 10.154722:
            LF01 = compileTo(LF01, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.156111:
            LF02 = compileTo(LF02, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.157778:
            LF03 = compileTo(LF03, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.159167:
            LF04 = compileTo(LF04, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.160833:
            LF05 = compileTo(LF05, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.162222:
            LF06 = compileTo(LF06, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.163611:
            LF07 = compileTo(LF07, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.165278:
            LF08 = compileTo(LF08, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])        
        elif Landtag_FH[i][1] < 10.166667:
            LF09 = compileTo(LF09, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.168056:
            LF10 = compileTo(LF10, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.169722:
            LF11 = compileTo(LF11, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.171111:
            LF12 = compileTo(LF12, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])
        elif Landtag_FH[i][1] < 10.172778:
            LF13 = compileTo(LF13, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])            
        elif Landtag_FH[i][1] < 10.174167:
            LF14 = compileTo(LF14, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])            
        elif Landtag_FH[i][1] < 10.175556:
            LF15 = compileTo(LF15, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])            
        elif Landtag_FH[i][1] < 10.177222:
            LF16 = compileTo(LF16, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])            
        else:
            LF17 = compileTo(LF17, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3], Landtag_FH[i][4])      

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
     
    for i in range(len(Geomar_Landtag)):
        if Geomar_Landtag[i][1] < 10.154722:
            GL01 = compileTo(GL01, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.156111:
            GL02 = compileTo(GL02, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.157778:
            GL03 = compileTo(GL03, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.159167:
            GL04 = compileTo(GL04, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.160556:
            GL05 = compileTo(GL05, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.162222:
            GL06 = compileTo(GL06, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.163611:
            GL07 = compileTo(GL07, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.165000:
            GL08 = compileTo(GL08, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])        
        elif Geomar_Landtag[i][1] < 10.166667:
            GL09 = compileTo(GL09, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.168056:
            GL10 = compileTo(GL10, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.169444:
            GL11 = compileTo(GL11, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.171111:
            GL12 = compileTo(GL12, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.172500:
            GL13 = compileTo(GL13, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])            
        elif Geomar_Landtag[i][1] < 10.173889:
            GL14 = compileTo(GL14, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])            
        elif Geomar_Landtag[i][1] < 10.175278:
            GL15 = compileTo(GL15, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])            
        elif Geomar_Landtag[i][1] < 10.176944:
            GL16 = compileTo(GL16, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.178333:
            GL17 = compileTo(GL17, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.179722:
            GL18 = compileTo(GL18, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
        elif Geomar_Landtag[i][1] < 10.181389:
            GL19 = compileTo(GL19, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])            
        else:
            GL20 = compileTo(GL20, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3], Geomar_Landtag[i][4])
    GL = [GL01, GL02, GL03, GL04, GL05, GL06, GL07, GL08, GL09, GL10, GL11, GL12, GL13, GL14, GL15, GL16, GL17, GL18, GL19, GL20]

# the calculation of the Mahalanobis-Distance
def calculateMahalanobis(mVector, covMatrix, lan, lon, spd, head):
    testValue = np.array([lan, lon, spd, head])
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

def reportAnomaly(strTime, mDistance, lat, lon):
    global Anomaly
    global Anomaly_Coord
    print("Anomaly detected at: " + str(strTime))
    if len(Anomaly) == 0:
        Anomaly = [[strTime, float(mDistance)]]
    else:
        Anomaly.append([strTime, float(mDistance)])
    if len(Anomaly_Coord) == 0:
        Anomaly_Coord = [[lat, lon]]
    else:
        Anomaly_Coord.append([lat, lon])
###############################################################################
##############DECLARE VARIABLES#############
###############################################################################

# declare constant chiSquaredValue
# for critical value:
    # 0.99999 = 28.4733
    # 0.9999 = 23.5127 (gathered by using Excel function =CHIINV(0.0001,4))
    # 0.999 = 18.467
    # 0.99  = 13.277
    # 0.975 = 11.143
chiSquaredValue = 28.4733

tempList = []

Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []
unknown = []
LF = []
GL = []

row = 0
trip = 0

Anomaly = []
Anomaly_Coord = []

mDist = 0

###############################################################################
################# MAIN ########################################################
###############################################################################

month = 6
for day in range (18, 27):
    for time in range(23):
        comp(generatePath(month, day, time + 1))
    sortToTrip()
    tempList = []

sortLandtag_FH()
sortGeomar_Landtag()

for i in range(len(LF)):
    for j in range(len(LF[i])):
        mDist = calculateMahalanobis(meanVectorLF[i], covMatLF[i], LF[i][j][0], LF[i][j][1], LF[i][j][2], LF[i][j][3])
        if detectAnomaly(mDist):
            reportAnomaly(LF[i][j][4], mDist, LF[i][j][0], LF[i][j][1])

for i in range(len(GL)):
    for j in range(len(GL[i])):
        mDist = calculateMahalanobis(meanVectorGL[i], covMatGL[i], GL[i][j][0], GL[i][j][1], GL[i][j][2], GL[i][j][3])
        if detectAnomaly(mDist):
            reportAnomaly(GL[i][j][4], mDist, GL[i][j][0], GL[i][j][1])

if i in range(len(FH_Geomar)):
    mDist = calculateMahalanobis(meanVectorFG, covMatFG, FH_Geomar[i][0], FH_Geomar[i][1], FH_Geomar[i][2], FH_Geomar[i][3])
    if detectAnomaly(mDist):
        reportAnomaly(FH_Geomar[i][4], mDist, FH_Geomar[i][0], FH_Geomar[i][1])

###############################################################################
###############SAVE AS KML AND CSV###################
###############################################################################

with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Point_kiwo_100m.csv", 'w') as f:
    mywriter = csv.writer(f, delimiter=',')
    mywriter.writerows(Anomaly)


kml_anomaly = simplekml.Kml()

for i in range(len(Anomaly_Coord)):
    kml_anomaly.newpoint(coords=[(Anomaly_Coord[i][1], Anomaly_Coord[i][0])])
kml_anomaly.save("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_KIWO_100m.kml")

# # save file as csv
  
# # with open("C://Users//darie//Documents//FH//BA//Anomaly//Landtag_FH_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
# #     mywriter = csv.writer(f, delimiter=',')
# #     mywriter.writerows(Landtag_FH)

# # with open("C://Users//darie//Documents//FH//BA//Anomaly//FH_Geomar_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
# #     mywriter = csv.writer(f, delimiter=',')
# #     mywriter.writerows(FH_Geomar)
    
# # with open("C://Users//darie//Documents//FH//BA//Anomaly//Geomar_Landtag_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
# #     mywriter = csv.writer(f, delimiter=',')
# #     mywriter.writerows(Geomar_Landtag)
    
# # with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Trip_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
# #     mywriter = csv.writer(f, delimiter=',')
# #     mywriter.writerows(unknown)
    
# # save as kml

# kml1 = simplekml.Kml()
# kml2 = simplekml.Kml()
# kml3 = simplekml.Kml()
# kml4 = simplekml.Kml()

# for i in range(len(Landtag_FH)):
#     kml1.newpoint(coords=[(Landtag_FH[i][1], Landtag_FH[i][0])])
    
# kml1.save("C://Users//darie//Documents//FH//BA//Anomaly//Landtag_FH_KIWO_ges.kml")

# for i in range(len(FH_Geomar)):
#     kml2.newpoint(coords=[(FH_Geomar[i][1], FH_Geomar[i][0])])
    
# kml2.save("C://Users//darie//Documents//FH//BA//Anomaly//FH_Geomar_KIWO_ges.kml")

# for i in range(len(Geomar_Landtag)):
#     kml3.newpoint(coords=[(Geomar_Landtag[i][1], Geomar_Landtag[i][0])])
    
# kml3.save("C://Users//darie//Documents//FH//BA//Anomaly//Geomar_Landtag_KIWO_ges.kml")

# for i in range(len(unknown)):
#     kml4.newpoint(coords=[(unknown[i][1], unknown[i][0])])
    
# kml4.save("C://Users//darie//Documents//FH//BA//Anomaly//unknown_KIWO_ges.kml")

