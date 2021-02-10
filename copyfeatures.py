print("Importing Packages")
import time
start=time.time()
startformat = time.localtime()

print("time imported")
import arcpy
print("arcpy imported")

print("Enter the location of the file folder. For the default location, press 'd'")

workspace = raw_input()
if workspace == "d":
    workspace = r"C:\Users\awbel\Documents\FinalCollab\GeoNet.gdb"

arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

Dataset = "WaterDistribution"
listfiles = arcpy.ListFeatureClasses("","ALL",Dataset)
exceptionsstr = []

print(str(listfiles))

originalReference=r"C:\Users\awbel\Documents\FinalCollab\Collab2014RS\NAD1983UTMZone18N.prj"
spatialReference=r"C:\Users\awbel\Documents\FinalCollab\Collab2014RS\WGS1984WebMercatorauxiliarysphere.prj"

for obj in listfiles:
    print("executing FOR loop")
    shapefile = workspace + "\\" + obj
    revision = "" #Enter name of revision here
    shapedesc = arcpy.Describe(shapefile) 
    outworkspace = "C:\\Users\\awbel\\Documents\\FinalCollab\\Collab2014RS\\ToExport.gdb\\"
    outProjworkspace = "C:\\Users\\awbel\\Documents\\FinalCollab\\Collab2014RS\\ToExportProjected.gdb\\"
    outlayer = obj + "rev"
    outlayerfull = outworkspace + outlayer
    typefeat = shapedesc.shapeType  
    arcpy.CreateFeatureclass_management(outworkspace, outlayer, typefeat, spatial_reference=originalReference)
    fields = arcpy.ListFields(shapefile)    
    fieldCount = len(fields)    
    
    newfields = arcpy.ListFields(outlayerfull)    
       
    fieldmaps = arcpy.FieldMappings()
    fieldmaps.addTable(outlayerfull)
       
    for field in fields:
        fldmap = arcpy.FieldMap()
        
        print field.baseName
        print field.type
        if str(field.type) != "OID" and str(field.type) != "Raster" and str(field.type) != "Guid" and str(field.type) != "Geometry" and str(field.baseName) != "OBJECTID" and str(field.baseName) != "SHAPE" and str(field.baseName) != "SHAPE_Length" and str(field.baseName) != "Shape_Length" and str(field.baseName) != "SHAPE_Area":
            fieldname = str(field.baseName) + revision
            fielddefault = str(field.defaultValue)
            fielddomain = str(field.domain)
            fieldtype = str(field.type)
            fieldlength = str(field.length)
            fieldrequired = "REQUIRED"
            fieldalias = str(field.aliasName)
            
            print(str(fielddefault))
            if fielddefault == "None":
                print("Assigning default to " + format(str(field.baseName)))
                if fieldtype == "String":
                    fielddefault = "NoValue"
                elif fieldtype == "Date":
                    fielddefault = "1900-01-01"
                else:
                    fielddefault = 1
    
            arcpy.AddField_management(outlayerfull, fieldname, fieldtype, fieldlength, "", fieldlength, fieldalias, "NON_NULLABLE", fieldrequired, fielddomain)
            fldmap.addInputField(outlayerfull, fieldname)
            fieldmapped = fldmap.outputField
            fieldmapped.name, fieldmapped.domain, fieldmapped.type, fieldmapped.length, fieldmapped. aliasName = fieldname, fielddomain, fieldtype, fieldlength, fieldalias
            fldmap.outputField = fieldmapped
            fieldmaps.addFieldMap(fldmap)
            
    with arcpy.da.Editor(workspace) as edit:
        with arcpy.da.UpdateCursor(shapefile, "*") as update:
            print(str(update))
            for row in update:
                rowU = row
                for field in range(fieldCount):
                    if fields[field] == None:
                        
                        #String domains
                        if fields[field].domain == "ControlValveType" or fields[field].domain == "FittingType" or fields[field].domain == "PipeMaterial":
                            rowU[field] = "UNK"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "SystemValveType" or fields[field].domain == "wHydrantManufacturer" or fields[field].domain == "wPumpType":
                            rowU[field] = "Unknown"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "wStructureType":
                            rowU[field] = "Other"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "wYesNo":
                            rowU[field] = "No"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))    
                        elif fields[field].domain == "WaterType":
                            rowU[field] = "Storm"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "LiningMethod":
                            rowU[field] = "NONE"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "LocationID":
                            rowU[field] = "Agency"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "PipeDiameter":
                            rowU[field] = "0"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "PipeUse":
                            rowU[field] = "ZZ"
                            update.updateRow(rowU)
                            print("Updated row " + str(row)) 
                        elif fields[field].domain == "ServiceType":
                            rowU[field] = "Domestic"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                        elif fields[field].domain == "wOperationlAreaType":
                            rowU[field] = "InspectionArea"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))   

                        #Date Domains                              
                        elif fields[field].type == "Date":
                            rowU[field] = "1900-01-01"
                            update.updateRow(rowU)
                            print("Updated row " + str(row))
                            
                        #Numerical domains
                        elif fields[field].domain == "AssetManager" or fields[field].domain == "AssetOwner":
                            rowU[field] = -2
                            update.updateRow(rowU)                        
                            print("Updated row " + str(row))
                        elif fields[field].domain == "AncillaryRoleDomain" or fields[field].domain == "BooleanDomain" or fields[field].domain == "FlowRate":
                            rowU[field] = 0
                            update.updateRow(rowU)                        
                            print("Updated row " + str(row))    
                            
                        #No domain assigned
                        else:
                            if fields[field].type == "String":
                                rowU[field] = "UNK"
                                update.updateRow(rowU)                        
                                print("Updated row " + str(row))                                    
                            else:
                                rowU[field] = "0"
                                update.updateRow(rowU)                        
                                print("Updated row " + str(row))                           
                            

        del update
    
    print("Created rows successfully")
    print("Feature is type " + str(typefeat))
    fieldslower = []
    for element in fields:
        fieldslower.append((element.baseName).lower())

    arcpy.Append_management(shapefile, outlayerfull, "NO_TEST", fieldmaps, "")
    
finish=time.time()
print("Program started at " + time.strftime("%H:%M:%S", startformat))
print("Program finished at " + time.strftime("%H:%M:%S"))
elapsed = finish-start
print("Time elapsed is " + str(elapsed) + " seconds")
        