import arcpy

workspace = raw_input()
if workspace == "d":
    workspace = r"C:\Users\awbel\Documents\FinalCollab\Collab2014RS\WaterInfrastructureNapervilleIllinois.gdb"

arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

listfiles = arcpy.ListFeatureClasses()
for obj in listfiles:
    shapefile = workspace + "\\" + obj
    print(shapefile)
    for shapefile in listfiles:
        fields = arcpy.ListFields(shapefile)    
        with arcpy.da.Editor(workspace) as edit:
                with arcpy.da.UpdateCursor(shapefile, "*") as update:
                    print(str(update))
                    for row in update:
                        update.deleteRow()