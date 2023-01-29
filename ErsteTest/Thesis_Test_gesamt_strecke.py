#Name: Darien Latjandu
#Matr.-Nr.: 928543

# libraries import
import numpy as np
from numpy.linalg import inv
import json
import csv
import simplekml

###############################################################################
#############DEFINE MATRIX AND VECTOR################
###############################################################################

# Create e matrices for the covariance matrix. The data was collected and calculated using Thesis_DataSort_Calc_Gesamt_Strecke.py
# the matrix for the first trip is as follows
# [0.00000229469  -0.000011469  0.00502192  -0.00310989]
# [-0.000011469   0.0000649524  -0.0205333  0.0426504]
# [0.00502192     -0.0205333    24.0854     46.6082]
# [-0.00310989    0.0426504     46.6082     944.473]

covMatrix1 = np.array([[0.00000229469, -0.000011469, 0.00502192, -0.00310989], 
                       [-0.000011469, 0.0000649524, -0.0205333, 0.0426504], 
                       [0.00502192, -0.0205333, 24.0854, 46.6082], 
                       [-0.00310989, 0.0426504, 46.6082, 944.473]])

# the matrix for the second trip is as follows
# [0.00000769667  -0.0000360365  0.0142871   -0.0134106]
# [-0.0000360365  0.000169001    -0.0665042  0.0668494]
# [0.0142871      -0.0665042     38.4563     28.6191]
# [-0.0134106     0.0668494      28.6191     3405.32]

covMatrix2 = np.array([[0.00000769667, -0.0000360365, 0.0142871, -0.0134106], 
                       [-0.0000360365, 0.000169001, -0.0665042, 0.0668494], 
                       [0.0142871, -0.0665042, 38.4563, 28.6191], 
                       [-0.0134106, 0.0668494, 28.6191, 3405.32]])

# the matrix for the third trip is as follows
# [0.00000276113  -0.0000141773  0.00284479  -0.10022]
# [-0.0000141773  0.0000908039   -0.0110684  0.357468]
# [0.00284479     -0.0110684     20.8935     60.805]
# [-0.10022       0.357468       60.805      34764.6]

covMatrix3 = np.array([[0.00000276113, -0.0000141773, 0.00284479, -0.10022], 
                       [-0.0000141773, 0.0000908039, -0.0110684, 0.357468], 
                       [0.00284479, -0.0110684, 20.8935, 60.805], 
                       [-0.10022, 0.357468, 60.805, 34764.6]])

# create 3 vectors for the mean vector. The data was collected and calculated using Thesis_DataSort_Calc_Gesamt_Strecke.py
# the vector for the first trip is as follows
# [54.3313]
# [10.1681]
# [11.0545]
# [99.7204]

mVector1 = np.array([54.3313, 10.1681, 11.0545, 99.7204])

# the vector for the second trip is as follows
# [54.3286]
# [10.181]
# [6.0379]
# [105.37]

mVector2 = np.array([54.3286, 10.181, 6.0379, 105.37])

# the vector for the third trip is as follows
# [54.3309]
# [10.1689]
# [10.7408]
# [272.536]

mVector3 = np.array([54.3309, 10.1689, 10.7408, 272.536])

###############################################################################
###################FUNCTIONS##################
###############################################################################

def getVektor(trip):
    global mVector1
    global mVector2
    global mVector3
    if trip == 1:
        return mVector1
    elif trip == 2:
        return mVector2
    elif trip == 3:
        return mVector3
    else:
        return "Trip unknown"

def getMatrix(trip):
    global covMatrix1
    global covMatrix2
    global covMatrix3
    if trip == 1:
        return covMatrix1
    elif trip == 2:
        return covMatrix2
    elif trip == 3:
        return covMatrix3
    else:
        return "Trip unknown"

# the calculation of the Mahalanobis-Distance
def calculateMahalanobis(trip, lan, lon, spd, head):
    mVector = np.array(getVektor(trip))
    covMatrix = np.asmatrix(getMatrix(trip))
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

def sortToTripAndDetectAnomaly():
    
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
                                mDist = calculateMahalanobis(trip, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                if detectAnomaly(mDist):
                                    reportAnomaly(tempList[prevstopend][5], mDist, tempList[prevstopend][0], tempList[prevstopend][1])
                                prevstopend += 1
                            prevstopend = row  
                            
                        elif trip == 2:
                            while prevstopend < stopstart:
                                FH_Geomar = compileTo(FH_Geomar, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                mDist = calculateMahalanobis(trip, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                if detectAnomaly(mDist):
                                    reportAnomaly(tempList[prevstopend][5], mDist, tempList[prevstopend][0], tempList[prevstopend][1])
                                prevstopend += 1
                            prevstopend = row

                        elif trip == 3:
                            while prevstopend < stopstart:
                                Geomar_Landtag = compileTo(Geomar_Landtag, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3], tempList[prevstopend][5])
                                mDist = calculateMahalanobis(trip, tempList[prevstopend][0], tempList[prevstopend][1], tempList[prevstopend][2], tempList[prevstopend][3])
                                if detectAnomaly(mDist):
                                    reportAnomaly(tempList[prevstopend][5], mDist, tempList[prevstopend][0], tempList[prevstopend][1])
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

###############################################################################
################# MAIN ########################################################
###############################################################################

Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []
unknown = []
Anomaly = []
Anomaly_Coord = []

tempList = []
row = 0

# declare constant chiSquaredValue
# for critical value:
    # 0.99999 = 28.4733
    # 0.9999 = 23.5127 (gathered by using Excel function =CHIINV(0.0001,4))
    # 0.999 = 18.467
    # 0.99  = 13.277
    # 0.975 = 11.143
chiSquaredValue = 28.4733


month = 6
for day in range (18, 27):
    for time in range(23):
        comp(generatePath(month, day, time + 1))
    sortToTripAndDetectAnomaly()
    tempList = []

###############################################################################
###############SAVE AS KML AND CSV###################
###############################################################################

# save file as csv

# with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Point_kiwo_gesamt.csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(Anomaly)

# with open("C://Users//darie//Documents//FH//BA//Anomaly//Landtag_FH_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(Landtag_FH)

# with open("C://Users//darie//Documents//FH//BA//Anomaly//FH_Geomar_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(FH_Geomar)
    
# with open("C://Users//darie//Documents//FH//BA//Anomaly//Geomar_Landtag_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(Geomar_Landtag)
    
# with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Trip_" + str(day) + "-" + str(month) + ".csv", 'w') as f:
#     mywriter = csv.writer(f, delimiter=',')
#     mywriter.writerows(unknown)
    
# save as kml

kml1 = simplekml.Kml()
kml2 = simplekml.Kml()
kml3 = simplekml.Kml()
kml4 = simplekml.Kml()
kml_anomaly = simplekml.Kml()

for i in range(len(Landtag_FH)):
    kml1.newpoint(coords=[(Landtag_FH[i][1], Landtag_FH[i][0])])
    
kml1.save("C://Users//darie//Documents//FH//BA//Anomaly//Landtag_FH_KIWO_ges.kml")

for i in range(len(FH_Geomar)):
    kml2.newpoint(coords=[(FH_Geomar[i][1], FH_Geomar[i][0])])
    
kml2.save("C://Users//darie//Documents//FH//BA//Anomaly//FH_Geomar_KIWO_ges.kml")

for i in range(len(Geomar_Landtag)):
    kml3.newpoint(coords=[(Geomar_Landtag[i][1], Geomar_Landtag[i][0])])
    
kml3.save("C://Users//darie//Documents//FH//BA//Anomaly//Geomar_Landtag_KIWO_ges.kml")

for i in range(len(unknown)):
    kml4.newpoint(coords=[(unknown[i][1], unknown[i][0])])
    
kml4.save("C://Users//darie//Documents//FH//BA//Anomaly//unknown_KIWO_ges.kml")

for i in range(len(Anomaly_Coord)):
    kml_anomaly.newpoint(coords=[(Anomaly_Coord[i][1], Anomaly_Coord[i][0])])
kml_anomaly.save("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_KIWO_ges.kml")    
