#Name: Darien Latjandu
#Matr.-Nr.: 928543

## import libraries
# import json
import csv
import numpy as np
# import torch
# import torch.nn as nn
# import math

###############################################################################
######IMPORT DATA##########
###############################################################################
sLF = []
sGL = []

# # open the sorted dataset
for i in range(17):
    if i < 9:
        with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF0" + str(i + 1) + ".csv") as f:
            myreader = csv.reader(f)
            if len(sLF) == 0:
                sLF = [list(myreader)]
            else:
                sLF.append(list(myreader))
    else:
        with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF" + str(i + 1) + ".csv") as f:
            myreader = csv.reader(f)
            if len(sLF) == 0:
                sLF = [list(myreader)]
            else:
                sLF.append(list(myreader))

for i in range(20):
    if i < 9:
        with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL0" + str(i + 1) + ".csv") as f:
            myreader = csv.reader(f)
            if len(sGL) == 0:
                sGL = [list(myreader)]
            else:
                sGL.append(list(myreader))
    else:
        with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL" + str(i + 1) + ".csv") as f:
            myreader = csv.reader(f)
            if len(sGL) == 0:
                sGL = [list(myreader)]
            else:
                sGL.append(list(myreader))

###############################################################################
###############FUNCTIONS###################
###############################################################################

# functions is directly copied from Thesis_DataSort_Calc_Gesamt_Strecke.py

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

def savecsv(sourceList, path):
    with open(str(path), 'w') as f:
        mywriter = csv.writer(f, delimiter=',')
        mywriter.writerows(sourceList)

###############################################################################
###############DEFINE VARIABELS##################
###############################################################################

LF = []
GL = []
temp = []
standardList = []
meanVectorLF = []
meanVectorGL = []
covMatLF = []
covMatGL = []

###############################################################################
############MAIN#############
###############################################################################

# Cast the List component into float
# some of the line will be empty so check if the length of the row is 4
for i in range(len(sLF)):
    for j in range(len(sLF[i])):
        if len(sLF[i][j]) == 4:
            if len(temp) == 0:
                temp = [[float(sLF[i][j][0]), float(sLF[i][j][1]), float(sLF[i][j][2]), float(sLF[i][j][3])]]
            else:
                temp.append([float(sLF[i][j][0]), float(sLF[i][j][1]), float(sLF[i][j][2]), float(sLF[i][j][3])])
    if len(LF) == 0:
        LF = [temp]
    else:
        LF.append(temp)
    temp = []

for i in range(len(sGL)):
    for j in range(len(sGL[i])):
        if len(sGL[i][j]) == 4:
            if len(temp) == 0:
                temp = [[float(sGL[i][j][0]), float(sGL[i][j][1]), float(sGL[i][j][2]), float(sGL[i][j][3])]]
            else:
                temp.append([float(sGL[i][j][0]), float(sGL[i][j][1]), float(sGL[i][j][2]), float(sGL[i][j][3])])
    if len(GL) == 0:
        GL = [temp]
    else:
        GL.append(temp)
    temp = []

# free memory of unused lists
sLF = []
sGL = []

###############################################################################
##############CALCULATE THE MEAN VECTOR AND COVARIANCE MATRIX##################
###############################################################################

for i in range(len(LF)):
    if len(meanVectorLF) == 0:
        meanVectorLF = [meanVector(LF[i])]
    else:
        meanVectorLF.append(meanVector(LF[i]))
        
    for j in range(len(LF[i])):
        standardList = compileTo(standardList, LF[i][j][0] - meanVectorLF[i][0], LF[i][j][1] - meanVectorLF[i][1], LF[i][j][2] - meanVectorLF[i][2], LF[i][j][3] - meanVectorLF[i][3])
        
    if len(covMatLF) == 0:
        covMatLF = [covMatrix()]
    else:
        covMatLF.append(covMatrix())
    
    standardList = []

for i in range(len(GL)):
    if len(meanVectorGL) == 0:
        meanVectorGL = [meanVector(GL[i])]
    else:
        meanVectorGL.append(meanVector(GL[i]))
    
    for j in range(len(GL[i])):
        standardList = compileTo(standardList, GL[i][j][0] - meanVectorGL[i][0], GL[i][j][1] - meanVectorGL[i][1], GL[i][j][2] - meanVectorGL[i][2], GL[i][j][3] - meanVectorGL[i][3])
        
    if len(covMatGL) == 0:
        covMatGL = [covMatrix()]
    else:
        covMatGL.append(covMatrix())
    
    standardList = []

###############################################################################
#############SAVE INTO AND CS######################
###############################################################################

savecsv(meanVectorLF, "C://Users//darie//Documents//FH//BA//ShortTrip//meanVectors_Landtag_FH.csv")
savecsv(meanVectorGL, "C://Users//darie//Documents//FH//BA//ShortTrip//meanVectors_Geomar_Landtag.csv")
savecsv(covMatLF, "C://Users//darie//Documents//FH//BA//ShortTrip//Matrix_Landtag_FH.csv")
savecsv(covMatGL, "C://Users//darie//Documents//FH//BA//ShortTrip//Matrix_Geomar_Landtag.csv")

###############################################################################
#############OBSOLETE######################
###############################################################################

# the program was having 17 Variables for Landtag_FH and 20 Var for Geomar_Landtag
# the new program is using a List so that the file can be iterated 

# sLF01 = []
# sLF02 = []
# sLF03 = []
# sLF04 = []
# sLF05 = []
# sLF06 = []
# sLF07 = []
# sLF08 = []
# sLF09 = []
# sLF10 = []
# sLF11 = []
# sLF12 = []
# sLF13 = []
# sLF14 = []
# sLF15 = []
# sLF16 = []
# sLF17 = []

# sGL01 = []
# sGL02 = []
# sGL03 = []
# sGL04 = []
# sGL05 = []
# sGL06 = []
# sGL07 = []
# sGL08 = []
# sGL09 = []
# sGL10 = []
# sGL11 = []
# sGL12 = []
# sGL13 = []
# sGL14 = []
# sGL15 = []
# sGL16 = []
# sGL17 = []
# sGL18 = []
# sGL19 = []
# sGL20 = []

# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF01.csv") as f:
#     myreader = csv.reader(f)
#     sLF01 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF02.csv") as f:
#     myreader = csv.reader(f)
#     sLF02 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF03.csv") as f:
#     myreader = csv.reader(f)
#     sLF03 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF04.csv") as f:
#     myreader = csv.reader(f)
#     sLF04 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF05.csv") as f:
#     myreader = csv.reader(f)
#     sLF05 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF06.csv") as f:
#     myreader = csv.reader(f)
#     sLF06 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF07.csv") as f:
#     myreader = csv.reader(f)
#     sLF07 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF08.csv") as f:
#     myreader = csv.reader(f)
#     sLF08 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF09.csv") as f:
#     myreader = csv.reader(f)
#     sLF09 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF10.csv") as f:
#     myreader = csv.reader(f)
#     sLF10 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF11.csv") as f:
#     myreader = csv.reader(f)
#     sLF11 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF12.csv") as f:
#     myreader = csv.reader(f)
#     sLF12 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF13.csv") as f:
#     myreader = csv.reader(f)
#     sLF13 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF14.csv") as f:
#     myreader = csv.reader(f)
#     sLF14 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF15.csv") as f:
#     myreader = csv.reader(f)
#     sLF15 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF16.csv") as f:
#     myreader = csv.reader(f)
#     sLF16 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//LF17.csv") as f:
#     myreader = csv.reader(f)
#     sLF17 = list(myreader)

# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL01.csv") as f:
#     myreader = csv.reader(f)
#     sGL01 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL02.csv") as f:
#     myreader = csv.reader(f)
#     sGL02 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL03.csv") as f:
#     myreader = csv.reader(f)
#     sGL03 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL04.csv") as f:
#     myreader = csv.reader(f)
#     sGL04 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL05.csv") as f:
#     myreader = csv.reader(f)
#     sGL05 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL06.csv") as f:
#     myreader = csv.reader(f)
#     sGL06 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL07.csv") as f:
#     myreader = csv.reader(f)
#     sGL07 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL08.csv") as f:
#     myreader = csv.reader(f)
#     sGL08 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL09.csv") as f:
#     myreader = csv.reader(f)
#     sGL09 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL10.csv") as f:
#     myreader = csv.reader(f)
#     sGL10 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL11.csv") as f:
#     myreader = csv.reader(f)
#     sGL11 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL12.csv") as f:
#     myreader = csv.reader(f)
#     sGL12 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL13.csv") as f:
#     myreader = csv.reader(f)
#     sGL13 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL14.csv") as f:
#     myreader = csv.reader(f)
#     sGL14 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL15.csv") as f:
#     myreader = csv.reader(f)
#     sGL15 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL16.csv") as f:
#     myreader = csv.reader(f)
#     sGL16 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL17.csv") as f:
#     myreader = csv.reader(f)
#     sGL17 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL18.csv") as f:
#     myreader = csv.reader(f)
#     sGL18 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL19.csv") as f:
#     myreader = csv.reader(f)
#     sGL19 = list(myreader)
# with open("C://Users//darie//Documents//FH//BA//ShortTrip//GL20.csv") as f:
#     myreader = csv.reader(f)
#     sGL20 = list(myreader)


# LF01 = []
# LF02 = []
# LF03 = []
# LF04 = []
# LF05 = []
# LF06 = []
# LF07 = []
# LF08 = []
# LF09 = []
# LF10 = []
# LF11 = []
# LF12 = []
# LF13 = []
# LF14 = []
# LF15 = []
# LF16 = []
# LF17 = []

# GL01 = []
# GL02 = []
# GL03 = []
# GL04 = []
# GL05 = []
# GL06 = []
# GL07 = []
# GL08 = []
# GL09 = []
# GL10 = []
# GL11 = []
# GL12 = []
# GL13 = []
# GL14 = []
# GL15 = []
# GL16 = []
# GL17 = []
# GL18 = []
# GL19 = []
# GL20 = []

# for i in range(len(sLF01)):
#     if len(sLF01[i]) == 4:
#         LF01 = compileTo(LF01, float(sLF01[i][0]), float(sLF01[i][1]), float(sLF01[i][2]), float(sLF01[i][3]))
# for i in range(len(sLF02)):
#     if len(sLF02[i]) == 4:
#         LF02 = compileTo(LF02, float(sLF02[i][0]), float(sLF02[i][1]), float(sLF02[i][2]), float(sLF02[i][3]))
# for i in range(len(sLF03)):
#     if len(sLF03[i]) == 4:
#         LF03 = compileTo(LF03, float(sLF03[i][0]), float(sLF03[i][1]), float(sLF03[i][2]), float(sLF03[i][3]))
# for i in range(len(sLF04)):
#     if len(sLF04[i]) == 4:
#         LF04 = compileTo(LF04, float(sLF04[i][0]), float(sLF04[i][1]), float(sLF04[i][2]), float(sLF04[i][3]))
# for i in range(len(sLF05)):
#     if len(sLF05[i]) == 4:
#         LF05 = compileTo(LF05, float(sLF05[i][0]), float(sLF05[i][1]), float(sLF05[i][2]), float(sLF05[i][3]))
# for i in range(len(sLF06)):
#     if len(sLF06[i]) == 4:
#         LF06 = compileTo(LF06, float(sLF06[i][0]), float(sLF06[i][1]), float(sLF06[i][2]), float(sLF06[i][3]))
# for i in range(len(sLF07)):
#     if len(sLF07[i]) == 4:
#         LF07 = compileTo(LF07, float(sLF07[i][0]), float(sLF07[i][1]), float(sLF07[i][2]), float(sLF07[i][3]))
# for i in range(len(sLF08)):
#     if len(sLF08[i]) == 4:
#         LF08 = compileTo(LF08, float(sLF08[i][0]), float(sLF08[i][1]), float(sLF08[i][2]), float(sLF08[i][3]))
# for i in range(len(sLF09)):
#     if len(sLF09[i]) == 4:
#         LF09 = compileTo(LF09, float(sLF09[i][0]), float(sLF09[i][1]), float(sLF09[i][2]), float(sLF09[i][3]))
# for i in range(len(sLF10)):
#     if len(sLF10[i]) == 4:
#         LF10 = compileTo(LF10, float(sLF10[i][0]), float(sLF10[i][1]), float(sLF10[i][2]), float(sLF10[i][3]))
# for i in range(len(sLF11)):
#     if len(sLF11[i]) == 4:
#         LF11 = compileTo(LF11, float(sLF11[i][0]), float(sLF11[i][1]), float(sLF11[i][2]), float(sLF11[i][3]))
# for i in range(len(sLF12)):
#     if len(sLF12[i]) == 4:
#         LF12 = compileTo(LF12, float(sLF12[i][0]), float(sLF12[i][1]), float(sLF12[i][2]), float(sLF12[i][3]))
# for i in range(len(sLF13)):
#     if len(sLF13[i]) == 4:
#         LF13 = compileTo(LF13, float(sLF13[i][0]), float(sLF13[i][1]), float(sLF13[i][2]), float(sLF13[i][3]))
# for i in range(len(sLF14)):
#     if len(sLF14[i]) == 4:
#         LF14 = compileTo(LF14, float(sLF14[i][0]), float(sLF14[i][1]), float(sLF14[i][2]), float(sLF14[i][3]))
# for i in range(len(sLF15)):
#     if len(sLF15[i]) == 4:
#         LF15 = compileTo(LF15, float(sLF15[i][0]), float(sLF15[i][1]), float(sLF15[i][2]), float(sLF15[i][3]))
# for i in range(len(sLF16)):
#     if len(sLF16[i]) == 4:
#         LF16 = compileTo(LF16, float(sLF16[i][0]), float(sLF16[i][1]), float(sLF16[i][2]), float(sLF16[i][3]))
# for i in range(len(sLF17)):
#     if len(sLF17[i]) == 4:
#         LF17 = compileTo(LF17, float(sLF17[i][0]), float(sLF17[i][1]), float(sLF17[i][2]), float(sLF17[i][3]))

    
# for i in range(len(sGL01)):
#     if len(sGL01[i]) == 4:
#         GL01 = compileTo(GL01, float(sGL01[i][0]), float(sGL01[i][1]), float(sGL01[i][2]), float(sGL01[i][3]))
# for i in range(len(sGL02)):
#     if len(sGL02[i]) == 4:
#         GL02 = compileTo(GL02, float(sGL02[i][0]), float(sGL02[i][1]), float(sGL02[i][2]), float(sGL02[i][3]))
# for i in range(len(sGL03)):
#     if len(sGL03[i]) == 4:
#         GL03 = compileTo(GL03, float(sGL03[i][0]), float(sGL03[i][1]), float(sGL03[i][2]), float(sGL03[i][3]))
# for i in range(len(sGL04)):
#     if len(sGL04[i]) == 4:
#         GL04 = compileTo(GL04, float(sGL04[i][0]), float(sGL04[i][1]), float(sGL04[i][2]), float(sGL04[i][3]))
# for i in range(len(sGL05)):
#     if len(sGL05[i]) == 4:
#         GL05 = compileTo(GL05, float(sGL05[i][0]), float(sGL05[i][1]), float(sGL05[i][2]), float(sGL05[i][3]))
# for i in range(len(sGL06)):
#     if len(sGL06[i]) == 4:
#         GL06 = compileTo(GL06, float(sGL06[i][0]), float(sGL06[i][1]), float(sGL06[i][2]), float(sGL06[i][3]))
# for i in range(len(sGL07)):
#     if len(sGL07[i]) == 4:
#         GL07 = compileTo(GL07, float(sGL07[i][0]), float(sGL07[i][1]), float(sGL07[i][2]), float(sGL07[i][3]))
# for i in range(len(sGL08)):
#     if len(sGL08[i]) == 4:
#         GL08 = compileTo(GL08, float(sGL08[i][0]), float(sGL08[i][1]), float(sGL08[i][2]), float(sGL08[i][3]))
# for i in range(len(sGL09)):
#     if len(sGL09[i]) == 4:
#         GL09 = compileTo(GL09, float(sGL09[i][0]), float(sGL09[i][1]), float(sGL09[i][2]), float(sGL09[i][3]))
# for i in range(len(sGL10)):
#     if len(sGL10[i]) == 4:
#         GL10 = compileTo(GL10, float(sGL10[i][0]), float(sGL10[i][1]), float(sGL10[i][2]), float(sGL10[i][3]))
# for i in range(len(sGL11)):
#     if len(sGL11[i]) == 4:
#         GL11 = compileTo(GL11, float(sGL11[i][0]), float(sGL11[i][1]), float(sGL11[i][2]), float(sGL11[i][3]))
# for i in range(len(sGL12)):
#     if len(sGL12[i]) == 4:
#         GL12 = compileTo(GL12, float(sGL12[i][0]), float(sGL12[i][1]), float(sGL12[i][2]), float(sGL12[i][3]))
# for i in range(len(sGL13)):
#     if len(sGL13[i]) == 4:
#         GL13 = compileTo(GL13, float(sGL13[i][0]), float(sGL13[i][1]), float(sGL13[i][2]), float(sGL13[i][3]))
# for i in range(len(sGL14)):
#     if len(sGL14[i]) == 4:
#         GL14 = compileTo(GL14, float(sGL14[i][0]), float(sGL14[i][1]), float(sGL14[i][2]), float(sGL14[i][3]))
# for i in range(len(sGL15)):
#     if len(sGL15[i]) == 4:
#         GL15 = compileTo(GL15, float(sGL15[i][0]), float(sGL15[i][1]), float(sGL15[i][2]), float(sGL15[i][3]))
# for i in range(len(sGL16)):
#     if len(sGL16[i]) == 4:
#         GL16 = compileTo(GL16, float(sGL16[i][0]), float(sGL16[i][1]), float(sGL16[i][2]), float(sGL16[i][3]))
# for i in range(len(sGL17)):
#     if len(sGL17[i]) == 4:
#         GL17 = compileTo(GL17, float(sGL17[i][0]), float(sGL17[i][1]), float(sGL17[i][2]), float(sGL17[i][3]))
# for i in range(len(sGL18)):
#     if len(sGL18[i]) == 4:
#         GL18 = compileTo(GL18, float(sGL18[i][0]), float(sGL18[i][1]), float(sGL18[i][2]), float(sGL18[i][3]))
# for i in range(len(sGL19)):
#     if len(sGL19[i]) == 4:
#         GL19 = compileTo(GL19, float(sGL19[i][0]), float(sGL19[i][1]), float(sGL19[i][2]), float(sGL19[i][3]))
# for i in range(len(sGL20)):
#     if len(sGL20[i]) == 4:
#         GL20 = compileTo(GL20, float(sGL20[i][0]), float(sGL20[i][1]), float(sGL20[i][2]), float(sGL20[i][3]))
