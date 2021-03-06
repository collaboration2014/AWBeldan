#For use with JBSS Bahn v3.80 and up
#Created February 2021 by Allan Beldan
#Version 0.1.3 of this program

import time
starttime = time.time()
import math
import xml.etree.ElementTree as ET
import os


#Set map origin point. Map radius is 250 kilometers
xOrigin = -79.381815
yOrigin = 43.652522

#Set desired scale in meters
scale = 15

#Enter version of BAHN you are using. Do NOT include the release number (e.g. 3.89r2 will cause errors, so instead just use 3.89)
BahnV = 3.89

#Enter whether you are using an OSM or an SHP file
FileV = "OSM"

#Enter number of elements expected (This portion to be automated in future)
ExpElem = 37

#Enter input file
InputFile = r'C:\Users\Allan\Documents\GIS DataBase\rhillrailways.gml'

#Enter Output location
OutputFile = r"C:\Users\Allan\Documents\GIS DataBase\rhillrails.bna"

#Set constants
pi = 3.14159265358979

elnum = 1

#Bahn Versioning
if BahnV >= 3.87:
    halfmap = 32768
elif BahnV >= 3.84:
    halfmap = 16384
elif BahnV >= 3.80:
    halfmap = 8192
else:
    print("Invalid version number. Aborting.")
    exit()
    
#Generate BNA file
tree = ET.parse(InputFile)
root = tree.getroot()
f = open(OutputFile, "x")
if BahnV == 3.80 or BahnV == 3.81:
    f.write('BNAFILEVERSION 3750\n')
elif BahnV == 3.82 or BahnV == 3.83:
    f.write('BNAFILEVERSION 3830\n')
else:
    f.write('BNAFILEVERSION 3840\n')

while elnum <= ExpElem:
    print("Element " + str(elnum))
    point = 0
    ftype = root[elnum][0][3].text
    if ftype == "Rail":
        f.write('LINEMODE T1\n')
    elif ftype == "cycleway" or ftype == "bridleway" or ftype == "footway" or ftype == "path"or ftype == "pedestrian" or ftype == "steps" or ftype == "track_grade1" or ftype == "track_grade2" or ftype == "track_grade3" or ftype == "track_grade4" or ftype == "track_grade5":
        f.write('LINEMODE P0\n')
    elif ftype == "track":
        f.write('LINEMODE N2\n')
    elif ftype == "motorway" or ftype == "motorway_link" or ftype == "trunk" or ftype == "trunk_link":
        f.write('LINEMODE M1\n')
    elif ftype == "primary" or ftype == "secondary" or ftype == "secondary_link":
        f.write('LINEMODE M0\n')
    elif ftype == "residential" or ftype == "service" or ftype == "tertiary" or ftype == "tertiary_link" or ftype == "unclassified" or ftype == "unknown":
        f.write('LINEMODE N0\n')
    elif ftype == "rail":
        f.write('LINEMODE T1\n')
    elif ftype == "tram":
        f.write('LINEMODE R0\n')
    elif ftype == "light_rail" or ftype == "subway" or ftype == "monorail":
        f.write('LINEMODE R1\n')
    elif ftype == "narrow_gauge" or ftype == "miniature_railway" or ftype == "funicular":
        f.write('LINEMODE T3\n')
    elif ftype == "canal" or ftype == "drain" or ftype == "river" or ftype == "stream":
        f.write('LINEMODE W1\n')
    
    coordinates = root[elnum][0][0][0][0][0][0].text
    coordinateList = coordinates.split(" ")
    for coordPair in coordinateList:
        if point == 0:
            xyList = coordPair.split(",")
            
            R = 6373000
            
            lat1 = xOrigin
            lon1 = yOrigin
            lat2 = float(xyList[0])
            lon2 = float(xyList[1])
         
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = ((pi * R * math.cos(lat2))/(180*math.sqrt(1-(0.0033528**2)*(math.sin(lat2)**2))))*dlon      
            b = dlat * 111000
            
            longDist = a/scale
            latDist = b/scale
            xorgtile = lat2
            yorgtile = lon2

        else:
            xyList = coordPair.split(",")
            
            R = 6373000
            
            lat1 = xorgtile
            lon1 = yorgtile
            lat2 = float(xyList[0])
            lon2 = float(xyList[1])
            
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            
            a = ((pi * R * math.cos(lat2))/(180*math.sqrt(1-(0.0033528**2)*(math.sin(lat2)**2))))*dlon         
            b = dlat * 111000
            
            longDist = a/scale
            latDist = b/scale
            xorgtile = lat2
            yorgtile = lon2

        if point == 0:
            if FileV == "SHP" and BahnV >= 3.84:
                if root[elnum][0][7].text == "T":
                    f.write("ORIGIN " + str(round(latDist)+halfmap) + "," + str(round(longDist)+halfmap) + ",-1\n")
                    point += 1                
                else:
                    f.write("ORIGIN " + str(round(latDist)+halfmap) + "," + str(round(longDist)+halfmap) + ",0\n")
                    point += 1
            else:
                if BahnV >= 3.84:
                    f.write("ORIGIN " + str(round(latDist)+halfmap) + "," + str(round(longDist)+halfmap) + ",0\n")
                    point += 1
                else:
                    f.write("ORIGIN " + str(round(latDist)+halfmap) + "," + str(round(longDist)+halfmap) + "\n")
                    point += 1                    
        else:
            f.write("LINEREL " + str(round(latDist)) + "," + str(round(longDist)) + "\n")
            point += 1
    elnum += 1
    os.system('cls')
f.write('END\n')
stoptime = time.time()
UserTimer = round((stoptime - starttime), 1)
print("Finished. Processed " + str(elnum-1) + " elements in " + str(UserTimer) + " seconds" )
exit()