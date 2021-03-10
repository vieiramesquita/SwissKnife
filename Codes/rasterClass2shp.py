import os
import sys
from osgeo import ogr
import rasterio

##

##

#Create storage vector

outfile_name = sys.argv[2] #"E:\\Base_Geo_QGIS\\Rasters\\mapbiomas_col5_stable_declividade\\POINTS\\stable5y_D2_points.shp"

if (os.path.isfile(outfile_name[:-4]+'.shp')==True) & (os.path.isfile(outfile_name[:-4]+'.shx')==True) & (os.path.isfile(outfile_name[:-4]+'.dbf')==True):
	os.remove(outfile_name[:-4]+'.shp');
	os.remove(outfile_name[:-4]+'.shx');
	os.remove(outfile_name[:-4]+'.dbf');

driver = ogr.GetDriverByName('ESRI Shapefile')
output_file = driver.CreateDataSource(os.path.dirname(outfile_name));

output_layer = output_file.CreateLayer(os.path.basename(outfile_name)[:-4], None, ogr.wkbPoint);

classField= ogr.FieldDefn("Class", ogr.OFTInteger);
output_layer.CreateField(classField);


##

##

#Read and extract raster values to points

fname = sys.argv[1] #"E:\\Base_Geo_QGIS\\Rasters\\mapbiomas_col5_stable_declividade\\mapbiomas_col5_stable5y_D2.tif"

map_layer = rasterio.open(fname,nodata=sys.argv[3])

band_layer = map_layer.read(1)

xcount = map_layer.width
ycount = map_layer.height

for y in range(0,ycount,1):
	for x in range(0,xcount,1):
		pixels2coords = map_layer.xy(x, y)  #input px, py
		#coords2pixels = map_layer.index(pixels2coords[0],pixels2coords[1]) #input lon,lat
		band_value = band_layer[x,y]

		if band_value != sys.argv[3]:

			print(pixels2coords,band_value)

			feat = ogr.Feature(output_layer.GetLayerDefn())

			point = ogr.Geometry(ogr.wkbPoint)
			point.AddPoint(pixels2coords[0],pixels2coords[1])

			feat.SetGeometry(point);
			feat.SetField("Class", int(band_value));

			output_layer.CreateFeature(feat)