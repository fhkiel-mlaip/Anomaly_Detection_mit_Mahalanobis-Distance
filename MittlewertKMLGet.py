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
###############FUNCTIONS###################
###############################################################################

def getPath(Trip, Type):
    path = "C://Users//darie//Documents//FH//BA//Matrix_Vector//testex_Vector_"
    
    if Trip == 0:
        path += "Landtag_FH_"
    elif Trip == 1:
        path += "FH_Geomar_"
    elif Trip == 2:
        path += "Geomar_Landtag_"
    
    if Type == 0:
        path += "point"
    elif Type == 1:
        path += "mean"
    elif Type == 2:
        path += "time"
        
    return path


def convertcsvkml(path):
    tempMeanVector = []
    meanVector = []
    
    with open(str(path) + ".csv") as f:
        myreader = csv.reader(f)
        tempMeanVector = list(myreader)
       
    for i in range(len(tempMeanVector)):
        if len(tempMeanVector[i]) == 4:
            if len(meanVector) == 0:
                meanVector = [np.array([float(tempMeanVector[i][0]), float(tempMeanVector[i][1]), float(tempMeanVector[i][2]), float(tempMeanVector[i][3])])]
            else:
                meanVector.append(np.array([float(tempMeanVector[i][0]), float(tempMeanVector[i][1]), float(tempMeanVector[i][2]), float(tempMeanVector[i][3])]))
    
    savekml(meanVector, path)

def savekml(List, path):    
    kml = simplekml.Kml()
    
    for i in range(len(List)):
        kml.newpoint(coords=[(List[i][1], List[i][0])])
        
    kml.save(str(path) + ".kml")


###############################################################################
############MAIN#############
###############################################################################

for Type in range(3):
    for Trip in range(3):
        convertcsvkml(getPath(Trip, Type))