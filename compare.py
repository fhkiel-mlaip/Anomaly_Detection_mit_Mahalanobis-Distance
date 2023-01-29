#Name: Darien Latjandu
#Matr.-Nr.: 928543

## import libraries
# import json
import simplekml
import csv
import numpy as np
# from numpy.linalg import inv
# import torch
# import torch.nn as nn
# import math

###############################################################################
#################################IMPORT DATA###################################
###############################################################################

testexAnomalyPoint = []
testexAnomalyMean = []
testexAnomalyTime = []
AnomalyPoint = []
AnomalyMean = []
AnomalyTime = []


with open("C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Point_kiwo_100m.csv") as f:
    myreader = csv.reader(f)
    testexAnomalyPoint = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Mean_kiwo_100m.csv") as f:
    myreader = csv.reader(f)
    testexAnomalyMean = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//Anomaly//testex_Anomaly_Time_kiwo.csv") as f:
    myreader = csv.reader(f)
    testexAnomalyTime = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Point_kiwo_100m.csv") as f:
    myreader = csv.reader(f)
    AnomalyPoint = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Mean_kiwo_100m.csv") as f:
    myreader = csv.reader(f)
    AnomalyMean = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//Anomaly//Anomaly_Time_kiwo.csv") as f:
    myreader = csv.reader(f)
    AnomalyTime = list(myreader)
    
def removeNonAnomaly(anomalyList):
    tempList = []
    for i in range(len(anomalyList)):
        if len(anomalyList[i]) != 0:
            if len(tempList) == 0:
                tempList = [anomalyList[i]]
            else:
                tempList.append(anomalyList[i])
    return tempList

testexAnomalyPoint = removeNonAnomaly(testexAnomalyPoint)
testexAnomalyMean = removeNonAnomaly(testexAnomalyMean)
testexAnomalyTime = removeNonAnomaly(testexAnomalyTime)
AnomalyPoint = removeNonAnomaly(AnomalyPoint)
AnomalyMean = removeNonAnomaly(AnomalyMean)
AnomalyTime = removeNonAnomaly(AnomalyTime)