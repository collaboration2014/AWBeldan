import math
import xml.etree.ElementTree as ET

xOrigin = -79.427886
yOrigin = 43.8447408
scale = 15
pi = 3.14159265358979

tree = ET.parse(r'C:\Users\Allan\Documents\GIS DataBase\rhillrailandroad.gml')

root = tree.getroot()

#Generate BNA file
f = open(r"C:\Users\Allan\Documents\GIS DataBase\testoutput.bna", "x")
f.write('BNAFILEVERSION 3830\n')

elnum = 1

while elnum <= 8527:
    point = 0
    ftype = root[elnum][0][3].text
    if ftype == "Rail":
        f.write('LINEMODE T1\n')
    elif ftype == "cycleway" or ftype == "footway" or ftype == "path"or ftype == "pedestrian" or ftype == "steps":
        f.write('LINEMODE P0\n')
    elif ftype == "track":
        f.write('LINEMODE N2\n')
    elif ftype == "motorway" or ftype == "motorway_link":
        f.write('LINEMODE M1\n')
    elif ftype == "primary" or ftype == "secondary" or ftype == "secondary_link":
        f.write('LINEMODE M0\n')
    elif ftype == "residential" or ftype == "service" or ftype == "tertiary" or ftype == "unclassified":
        f.write('LINEMODE N0\n')
    elif ftype == "Rail":
        f.write('LINEMODE T1\n')        
    
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
            f.write("ORIGIN " + str(int(latDist)+32768) + "," + str(int(longDist)+32768) + "\n")
            point += 1
        else:
            xtile = int(latDist)
            ytile = int(longDist)
            f.write("LINEREL " + str(xtile) + "," + str(ytile) + "\n")
            point += 1
    elnum += 1
f.write('END')
