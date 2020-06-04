#license = "GPL"
#version = "0.1"
#maintainer = "Lu Xin"
#email = "xinlu.nju@gmail.com"
#status = "Production"
#description = "delete error and connect river"

import arcpy,os,sys
from arcpy import env
from arcpy.sa import *

env.overwriteOutput=True
arcpy.CheckOutExtension("Spatial")
env.extent="MAXOF"
arcpy.env.workspace = "E:\gra_stu\paper2\data.gdb"  # make sure it is not too long


DEM = "DEM_modeled_drainage_network"  #the coordinate must be the same
RS_vector = "RS_mapped_river_network"  # RS vector river
RS_Raster = "RS_water_mask" # RS raster mask
cellsize = 10                                       
delete_length = 300  # area less than 300 m2 will be deleted

##delete error
buffer_DEM_clip = "buffer50_"+ DEM
arcpy.Buffer_analysis( DEM , buffer_DEM_clip , "50 Meters", "FULL", "ROUND", "ALL")
RS = "clip_" + RS_vector
arcpy.Intersect_analysis([RS_vector,buffer_DEM_clip],RS,"ALL","0","LINE")
#(RS_vector,buffer_DEM_clip,RS)
print "finish delete error"
                                                             
##snap DEM to RS
arcpy.Snap_edit(DEM , [[RS , "EDGE", "50 Meters"]])
print "finish snap"

##Get RS and DEM raster
buffer_DEM = "snaped_buffer50_"+ DEM
arcpy.Buffer_analysis( DEM , buffer_DEM , "50 Meters", "FULL", "ROUND", "ALL")
arcpy.AddField_management(buffer_DEM, "value", "LONG", "","")
arcpy.CalculateField_management(buffer_DEM,"value","2","PYTHON_9.3")

ToRaster_buffer_DEM = "To_Raster_" + buffer_DEM
arcpy.PolygonToRaster_conversion(buffer_DEM,"value",ToRaster_buffer_DEM,"CELL_CENTER","value",cellsize)
print "finish RS and DEM raster"


extract_RS_Raster  ="clip_" + RS_Raster
extract_RS_Raster1 = ExtractByMask(RS_Raster, buffer_DEM)
extract_RS_Raster1.save(extract_RS_Raster)
arcpy.CalculateStatistics_management(extract_RS_Raster)
arcpy.BuildPyramids_management(extract_RS_Raster)
print "finish clip RS"


##Get RS and DEM vector
cal_RS_Raster_DEM = Raster(ToRaster_buffer_DEM) + Raster(extract_RS_Raster)
con_cal_RS_Raster_DEM = Con(cal_RS_Raster_DEM>=3,3)


RS_Polygon = "RasterToPolygon" + RS
arcpy.RasterToPolygon_conversion(con_cal_RS_Raster_DEM,RS_Polygon,"SIMPLIFY")



layer3 = "delete_length" + RS_Polygon
arcpy.MakeFeatureLayer_management( RS_Polygon ,layer3 )
arcpy.SelectLayerByAttribute_management(layer3,"NEW_SELECTION",'"Shape_Area"<3000')   # you can modify this threshold
if int(arcpy.GetCount_management(layer3).getOutput(0)) > 0:
    arcpy.DeleteFeatures_management(layer3)
print "Get Raster to Polygon"


##Get Snapped DEM-modeled drainage network which coincided with RS-mapped river network 
DEM_coincidewith_RS = "coincide_" + DEM
arcpy.Clip_analysis(DEM,RS_Polygon,DEM_coincidewith_RS)
split_DEM_coincidewith_RS = "split_" + DEM_coincidewith_RS
arcpy.SplitLine_management(DEM_coincidewith_RS,split_DEM_coincidewith_RS)
unsplit_DEM_coincidewith_RS = "unsplit_" + split_DEM_coincidewith_RS
arcpy.UnsplitLine_management(split_DEM_coincidewith_RS,unsplit_DEM_coincidewith_RS)

##Get Snapped DEM-modeled drainage network which not coincided with RS-mapped river network
DEM_connect_RS = "connect_" + DEM
arcpy.Erase_analysis(DEM,RS_Polygon,DEM_connect_RS)
split_DEM_connect_RS = "split_" + DEM_connect_RS
arcpy.SplitLine_management(DEM_connect_RS,split_DEM_connect_RS)
unsplit_DEM_connect_RS = "unsplit_" + split_DEM_connect_RS
arcpy.UnsplitLine_management(split_DEM_connect_RS,unsplit_DEM_connect_RS)
print "Get coincided and connect line"

##Get dangle point of RS
RS_Point = "RS_Point_"+ RS
arcpy.FeatureVerticesToPoints_management(unsplit_DEM_coincidewith_RS,RS_Point,"BOTH_ENDS")
print "Get RS_Point"


arcpy.DeleteIdentical_management(unsplit_DEM_connect_RS , ["Shape"],"0.01 Meters")

flag=0
field = arcpy.da.TableToNumPyArray (unsplit_DEM_connect_RS, "Shape_Length", skip_nulls=True)
sum = field["Shape_Length"].sum() 
sum1=0

while sum != sum1 :
    flag=flag+1
    #Get dangle point of DEM
    ST_DEM =   "Both_Ends" +str(flag)+ "_" + unsplit_DEM_connect_RS
    arcpy.FeatureVerticesToPoints_management(unsplit_DEM_connect_RS,ST_DEM,"BOTH_ENDS")
    Start_DEM =   "Start" +str(flag)+ "_" + unsplit_DEM_connect_RS
    arcpy.FeatureVerticesToPoints_management(unsplit_DEM_connect_RS,Start_DEM,"START")
    End_DEM =   "End" +str(flag)+ "_" +unsplit_DEM_connect_RS
    arcpy.FeatureVerticesToPoints_management(unsplit_DEM_connect_RS,End_DEM,"END")

    layer1 = "interlayer" + str(flag) + "_" +unsplit_DEM_connect_RS
    arcpy.MakeFeatureLayer_management( Start_DEM ,layer1 )
    arcpy.SelectLayerByLocation_management(layer1,"INTERSECT",End_DEM)
    Inter_DEM = "Inter" + str(flag)+ "_" +unsplit_DEM_connect_RS
    if int(arcpy.GetCount_management(layer1).getOutput(0)) > 0:
        arcpy.CopyFeatures_management(layer1, Inter_DEM)
    print "Get DEM point"

    #delete
    erase1 ="erase_inter" + str(flag)  
    erase2 ="erase_RS" +str(flag) 
    arcpy.Erase_analysis(ST_DEM , Inter_DEM ,erase1 ,"0.01 Meters" )
    arcpy.Erase_analysis(erase1 , RS_Point ,erase2 ,"0.01 Meters" )

    layer2 = "deletelayer" + str(flag) +"_" + unsplit_DEM_connect_RS
    arcpy.MakeFeatureLayer_management(unsplit_DEM_connect_RS ,layer2 )
    arcpy.SelectLayerByLocation_management(layer2,"CONTAINS",erase2)
    if int(arcpy.GetCount_management(layer2).getOutput(0)) > 0:
        arcpy.DeleteFeatures_management(layer2)
    sum1=sum
    field = arcpy.da.TableToNumPyArray (unsplit_DEM_connect_RS, "Shape_Length", skip_nulls=True)
    sum = field["Shape_Length"].sum()
    print "Delete"
