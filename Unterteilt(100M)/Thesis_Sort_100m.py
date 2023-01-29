#Name: Darien Latjandu
#Matr.-Nr.: 928543

## import libraries
# import json
import simplekml
import csv
import numpy as np
# import torch
# import torch.nn as nn
# import math

###############################################################################
######IMPORT DATA##########
###############################################################################
Landtag_FH_str = []
FH_Geomar_str = []
Geomar_Landtag_str = []

# open the sorted dataset
with open("C://Users//darie//Documents//FH//BA//12//Landtag_FH.csv") as f:
    myreader = csv.reader(f)
    Landtag_FH_str = list(myreader)

with open("C://Users//darie//Documents//FH//BA//12//FH_Geomar.csv") as f:
    myreader = csv.reader(f)
    FH_Geomar_str = list(myreader)
    
with open("C://Users//darie//Documents//FH//BA//12//Geomar_Landtag.csv") as f:
    myreader = csv.reader(f)
    Geomar_Landtag_str = list(myreader)

###############################################################################
###############FUNCTIONS###################
###############################################################################

# sort the trips to smaller parts according to its longitude 
# the trip will be split as follows
# Landtag_FH will be split into 17 part
# # below 10.154722
# # from 10.154722 to 10.156111
# # 10.156111 to 10.157778
# # 10.157778 to 10.159167
# # 10.159167 to 10.160833
# # 10.160833 to 10.162222
# # 10.162222 to 10.163611
# # 10.163611 to 10.165278 
# # 10.165278 to 10.166667
# # 10.166667 to 10.168056
# # 10.168056 to 10.169722
# # 10.169722 to 10.171111
# # 10.171111 to 10.172778
# # 10.172778 to 10.174167
# # 10.174167 to 10.175556
# # 10.175556 to 10.177222
# # above 10.177222
# to shorten name, the new List will be named LFxx with xx is the part in order above
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

def sortLandtag_FH():
    global Landtag_FH, LF01, LF02, LF03, LF04, LF05, LF06, LF07, LF08, LF09 
    global LF10, LF11, LF12, LF13, LF14, LF15, LF16, LF17
    for i in range(len(Landtag_FH)):
        if Landtag_FH[i][1] < 10.154722:
            LF01 = compileTo(LF01, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.156111:
            LF02 = compileTo(LF02, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.157778:
            LF03 = compileTo(LF03, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.159167:
            LF04 = compileTo(LF04, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.160833:
            LF05 = compileTo(LF05, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.162222:
            LF06 = compileTo(LF06, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.163611:
            LF07 = compileTo(LF07, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.165278:
            LF08 = compileTo(LF08, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])        
        elif Landtag_FH[i][1] < 10.166667:
            LF09 = compileTo(LF09, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.168056:
            LF10 = compileTo(LF10, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.169722:
            LF11 = compileTo(LF11, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.171111:
            LF12 = compileTo(LF12, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])
        elif Landtag_FH[i][1] < 10.172778:
            LF13 = compileTo(LF13, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])            
        elif Landtag_FH[i][1] < 10.174167:
            LF14 = compileTo(LF14, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])            
        elif Landtag_FH[i][1] < 10.175556:
            LF15 = compileTo(LF15, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])            
        elif Landtag_FH[i][1] < 10.177222:
            LF16 = compileTo(LF16, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])            
        else:
            LF17 = compileTo(LF17, Landtag_FH[i][0], Landtag_FH[i][1], Landtag_FH[i][2], Landtag_FH[i][3])            

def compileTo(List, lat, lon, spd, head):
    if len(List) == 0:
        List = [[lat, lon, spd, head]]
    else:
        List.append([lat, lon, spd, head])
    return List

# Geomar_Landtag will be split into 20 part
# # below 10.154722
# # from 10.154722 to 10.156111
# # 10.156111 to 10.157778
# # 10.157778 to 10.159167
# # 10.159167 to 10.160556
# # 10.160556 to 10.162222
# # 10.162222 to 10.163611
# # 10.163611 to 10.165000 
# # 10.165000 to 10.166667
# # 10.166667 to 10.168056
# # 10.168056 to 10.169444
# # 10.169444 to 10.171111
# # 10.171111 to 10.172500
# # 10.172500 to 10.173889
# # 10.173889 to 10.175278
# # 10.175278 to 10.176944
# # 10.176944 to 10.178333
# # 10.178333 to 10.179722
# # 10.179722 to 10.181389
# # above 10.181389

# to shorten name, the new List will be named GLxx with xx is the part in order above
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

def sortGeomar_Landtag():
    global Geomar_Landtag, GL01, GL02, GL03, GL04, GL05, GL06, GL07, GL08, GL09
    global GL10, GL11, GL12, GL13, GL14, GL15, GL16, GL17, GL18, GL19, GL20
    for i in range(len(Geomar_Landtag)):
        if Geomar_Landtag[i][1] < 10.154722:
            GL01 = compileTo(GL01, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.156111:
            GL02 = compileTo(GL02, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.157778:
            GL03 = compileTo(GL03, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.159167:
            GL04 = compileTo(GL04, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.160556:
            GL05 = compileTo(GL05, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.162222:
            GL06 = compileTo(GL06, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.163611:
            GL07 = compileTo(GL07, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.165000:
            GL08 = compileTo(GL08, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])        
        elif Geomar_Landtag[i][1] < 10.166667:
            GL09 = compileTo(GL09, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.168056:
            GL10 = compileTo(GL10, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.169444:
            GL11 = compileTo(GL11, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.171111:
            GL12 = compileTo(GL12, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.172500:
            GL13 = compileTo(GL13, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])            
        elif Geomar_Landtag[i][1] < 10.173889:
            GL14 = compileTo(GL14, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])            
        elif Geomar_Landtag[i][1] < 10.175278:
            GL15 = compileTo(GL15, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])            
        elif Geomar_Landtag[i][1] < 10.176944:
            GL16 = compileTo(GL16, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.178333:
            GL17 = compileTo(GL17, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.179722:
            GL18 = compileTo(GL18, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])
        elif Geomar_Landtag[i][1] < 10.181389:
            GL19 = compileTo(GL19, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])            
        else:
            GL20 = compileTo(GL20, Geomar_Landtag[i][0], Geomar_Landtag[i][1], Geomar_Landtag[i][2], Geomar_Landtag[i][3])

def saveincsvkml(sourceList, path):
    kml = simplekml.Kml()
    for i in range(len(sourceList)):
        kml.newpoint(coords=[(sourceList[i][1], sourceList[i][0])])
        
    kml.save(str(path) + ".kml")

    with open(str(path) + ".csv", 'w') as f:
        mywriter = csv.writer(f, delimiter=',')
        mywriter.writerows(sourceList)

###############################################################################
############MAIN#############
###############################################################################

Landtag_FH = []
FH_Geomar = []
Geomar_Landtag = []

# Cast the List component into float
# some of the line will be empty so check if the length of the row is 4
for i in range(len(Landtag_FH_str)):
    if len(Landtag_FH_str[i]) == 4:
        Landtag_FH = compileTo(Landtag_FH, float(Landtag_FH_str[i][0]), float(Landtag_FH_str[i][1]), float(Landtag_FH_str[i][2]), float(Landtag_FH_str[i][3]))
    
for i in range(len(Geomar_Landtag_str)):
    if len(Geomar_Landtag_str[i]) == 4:
        Geomar_Landtag = compileTo(Geomar_Landtag, float(Geomar_Landtag_str[i][0]), float(Geomar_Landtag_str[i][1]), float(Geomar_Landtag_str[i][2]), float(Geomar_Landtag_str[i][3]))

for i in range(len(FH_Geomar_str)):
    if len(FH_Geomar_str[i]) == 4:
        FH_Geomar = compileTo(FH_Geomar, float(FH_Geomar_str[i][0]), float(FH_Geomar_str[i][1]), float(FH_Geomar_str[i][2]), float(FH_Geomar_str[i][3]))


    
sortLandtag_FH()
sortGeomar_Landtag()

###############################################################################
#############SAVE INTO KML AND CS######################
###############################################################################
saveincsvkml(LF01, "C://Users//darie//Documents//FH//BA//ShortTrip//LF01")
saveincsvkml(LF02, "C://Users//darie//Documents//FH//BA//ShortTrip//LF02")
saveincsvkml(LF03, "C://Users//darie//Documents//FH//BA//ShortTrip//LF03")
saveincsvkml(LF04, "C://Users//darie//Documents//FH//BA//ShortTrip//LF04")
saveincsvkml(LF05, "C://Users//darie//Documents//FH//BA//ShortTrip//LF05")
saveincsvkml(LF06, "C://Users//darie//Documents//FH//BA//ShortTrip//LF06")
saveincsvkml(LF07, "C://Users//darie//Documents//FH//BA//ShortTrip//LF07")
saveincsvkml(LF08, "C://Users//darie//Documents//FH//BA//ShortTrip//LF08")
saveincsvkml(LF09, "C://Users//darie//Documents//FH//BA//ShortTrip//LF09")
saveincsvkml(LF10, "C://Users//darie//Documents//FH//BA//ShortTrip//LF10")
saveincsvkml(LF11, "C://Users//darie//Documents//FH//BA//ShortTrip//LF11")
saveincsvkml(LF12, "C://Users//darie//Documents//FH//BA//ShortTrip//LF12")
saveincsvkml(LF13, "C://Users//darie//Documents//FH//BA//ShortTrip//LF13")
saveincsvkml(LF14, "C://Users//darie//Documents//FH//BA//ShortTrip//LF14")
saveincsvkml(LF15, "C://Users//darie//Documents//FH//BA//ShortTrip//LF15")
saveincsvkml(LF16, "C://Users//darie//Documents//FH//BA//ShortTrip//LF16")
saveincsvkml(LF17, "C://Users//darie//Documents//FH//BA//ShortTrip//LF17")

saveincsvkml(GL01, "C://Users//darie//Documents//FH//BA//ShortTrip//GL01")
saveincsvkml(GL02, "C://Users//darie//Documents//FH//BA//ShortTrip//GL02")
saveincsvkml(GL03, "C://Users//darie//Documents//FH//BA//ShortTrip//GL03")
saveincsvkml(GL04, "C://Users//darie//Documents//FH//BA//ShortTrip//GL04")
saveincsvkml(GL05, "C://Users//darie//Documents//FH//BA//ShortTrip//GL05")
saveincsvkml(GL06, "C://Users//darie//Documents//FH//BA//ShortTrip//GL06")
saveincsvkml(GL07, "C://Users//darie//Documents//FH//BA//ShortTrip//GL07")
saveincsvkml(GL08, "C://Users//darie//Documents//FH//BA//ShortTrip//GL08")
saveincsvkml(GL09, "C://Users//darie//Documents//FH//BA//ShortTrip//GL09")
saveincsvkml(GL10, "C://Users//darie//Documents//FH//BA//ShortTrip//GL10")
saveincsvkml(GL11, "C://Users//darie//Documents//FH//BA//ShortTrip//GL11")
saveincsvkml(GL12, "C://Users//darie//Documents//FH//BA//ShortTrip//GL12")
saveincsvkml(GL13, "C://Users//darie//Documents//FH//BA//ShortTrip//GL13")
saveincsvkml(GL14, "C://Users//darie//Documents//FH//BA//ShortTrip//GL14")
saveincsvkml(GL15, "C://Users//darie//Documents//FH//BA//ShortTrip//GL15")
saveincsvkml(GL16, "C://Users//darie//Documents//FH//BA//ShortTrip//GL16")
saveincsvkml(GL17, "C://Users//darie//Documents//FH//BA//ShortTrip//GL17")
saveincsvkml(GL18, "C://Users//darie//Documents//FH//BA//ShortTrip//GL18")
saveincsvkml(GL19, "C://Users//darie//Documents//FH//BA//ShortTrip//GL19")
saveincsvkml(GL20, "C://Users//darie//Documents//FH//BA//ShortTrip//GL20")

