"""This code creates a line CAD object in DXF_R2010 format from *.csv (comma separeted format) imported from
GNSS reciver in specific type of measure and coding of points.
The format of csv file has to be :" Number of point , X, Y , H, code".
Script will work corectly if you measured points of each line and gived them ascending numbers depend
from order of measure. You have to define this same code for each mesured line.
Script work for one coded line. If you want to drw another coded line use Toolbox for second time."""

# Import nessesery modules
import arcpy
import csv

# Import parameteters from GUI
data = arcpy.GetParameterAsText(0)
input_csv = arcpy.GetParameterAsText(1)
striped_csv = arcpy.GetParameterAsText(2)
path_dxf = arcpy.GetParameterAsText(3)

# Write a header output csv file , the header has to be in format like : nr,X,Y,Z,kod
with open(striped_csv, 'a') as stripDict:
    fieldnames = ['nr', 'X', 'Y', 'Z', 'kod']
    writer = csv.DictWriter(stripDict, fieldnames=fieldnames)
    writer.writeheader()

# Open input csv file as a dictionary
with open(input_csv) as Dict:
    reader = csv.DictReader(Dict)
# Searching for specified code from measurment inputed by user and write it in output csv file
    for row in reader:
        if data == row['kod']:
            with open(striped_csv, 'a') as stripDict:
                writer = csv.DictWriter(stripDict, delimiter=',', fieldnames=fieldnames, lineterminator='\n')

                writer.writerow(row)

# ArcPy operations

# Create workspace
arcpy.env.workspace = "E:/GIS Programming/Tory_Stacja_Korsze"
arcpy.env.overwriteOutput = True

# Reference frame
pjr = r"E:\GIS Programming\Tory_Stacja_Korsze\Uklad_2000.prj"



# Create a variables to use MakeXYEvenLayer
in_Table = striped_csv
x_coord = "X"
y_coord = "Y"
z_coord = "Z"
out_Layer = "tor_1_points"
tor1_shp = r"E:\GIS Programming\Tory_Stacja_Korsze\tor_1_point.shp"


# Make the XY event layer...
arcpy.MakeXYEventLayer_management(in_Table, x_coord, y_coord, out_Layer, pjr)

# Save to a layer file
arcpy.MakeFeatureLayer_management(out_Layer, tor1_shp)


# Creating lines from points
tor1_line_shp = r"E:\GIS Programming\Tory_Stacja_Korsze\tor1_line.shp"
arcpy.PointsToLine_management(tor1_shp, tor1_line_shp)


# Save to a layer file (tor_line_shp)
save_line = r"E:\GIS Programming\Tory_Stacja_Korsze\tor_1_line.shp"
arcpy.MakeFeatureLayer_management(tor1_line_shp, save_line)

# Deleting temporary layers
arcpy.Delete_management("tor_1_points")

arcpy.Delete_management("tor1_line")


# Exporting features to dwg

arcpy.ExportCAD_conversion(tor1_line_shp, "DXF_R2010", path_dxf)
#'E:/GIS Programming/Tory_Stacja_Korsze/DWG/tor1.dwg'