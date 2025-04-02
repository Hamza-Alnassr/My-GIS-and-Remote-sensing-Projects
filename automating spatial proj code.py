
import arcpy
import os
from arcpy.sa import ExtractByMask

arcpy.env.workspace = r"C:\Users\Dell\Documents\ArcGIS\Projects\Automating Spatial Data Analysis Project\Automating Spatial Data Analysis Project.aprx"
arcpy.env.overwriteOutput = True

uae_region = r"C:\Users\Dell\Downloads\uae bounds shapefile for arcgispro\are_admbnda_adm0_fcsc_20230515.shp"


global_landcover = r"https://earthobs3.arcgis.com/arcgis/services/ESA_CCI_Land_Cover_Time_Series/ImageServer"


schools = r"C:\Users\Dell\Downloads\eduction points in uae arcgispro\hotosm_are_education_facilities_polygons_shp.shp"
hospitals = r"C:\Users\Dell\Downloads\healthcare points uae arcgispro\hotosm_are_health_facilities_points_shp.shp"


output_folder = r"C:\Users\Dell\Downloads\auto proj 1 output"


schools_points = os.path.join(output_folder, "Schools_Points.shp")


poi_shp = os.path.join(output_folder, "POI.shp")


uae_landcover_raster = os.path.join(output_folder, "UAE_Clipped_Landcover.tif")
uae_landcover_polygon = os.path.join(output_folder, "UAE_Clipped_Landcover_Polygons.shp")


poi_buffer = os.path.join(output_folder, "POI_Buffer_1km.shp")


spatial_join_result = os.path.join(output_folder, "POI_Landuse_SpatialJoin.shp")


summary_table = os.path.join(output_folder, "POI_Landuse_Summary.dbf")


diversity_table = os.path.join(output_folder, "POI_LandUse_Diversity.dbf")


arcpy.FeatureToPoint_management(in_features=schools, 
                                  out_feature_class=schools_points, 
                                  point_location="INSIDE")
print("Converted schools polygons to point features.")


arcpy.Merge_management([schools_points, hospitals], poi_shp)
print("Merged schools and hospitals into one Points of Interest shapefile.")


arcpy.CheckOutExtension("Spatial")


landcover_layer = "GlobalLandcoverLayer"
arcpy.MakeImageServerLayer_management(global_landcover, landcover_layer)
print("Created image service layer from the global land cover dataset.")

clipped_raster = ExtractByMask(landcover_layer, uae_region)
clipped_raster.save(uae_landcover_raster)
print("Clipped the global land cover raster to the UAE boundary.")


arcpy.CheckInExtension("Spatial")


arcpy.RasterToPolygon_conversion(in_raster=uae_landcover_raster, 
                                   out_polygon_features=uae_landcover_polygon, 
                                   simplify=True, 
                                   raster_field="Value")
print("Converted the clipped land cover raster to polygons.")


arcpy.Buffer_analysis(in_features=poi_shp, 
                      out_feature_class=poi_buffer, 
                      buffer_distance_or_field="1000 Meters", 
                      line_side="FULL", 
                      line_end_type="ROUND", 
                      dissolve_option="NONE")
print("Created a 1 km buffer around each point of interest.")


arcpy.SpatialJoin_analysis(target_features=poi_buffer, 
                           join_features=uae_landcover_polygon, 
                           out_feature_class=spatial_join_result, 
                           join_operation="JOIN_ONE_TO_MANY", 
                           match_option="INTERSECT")
print("Completed spatial join to identify land use classes within each buffer.")

spatial_join_result = "POI_Landuse_SpatialJoin"

# Using a geodatabase for the output instead of a .dbf file
output_gdb = r"C:\Users\Dell\Documents\ArcGIS\Projects\MyProject.gdb"
summary_table = output_gdb + r"\SummaryTable"  # Save as a table inside GDB


arcpy.Statistics_analysis(
    in_table=spatial_join_result,
    out_table=summary_table,
    statistics_fields=[["amenity", "COUNT"], ["building", "COUNT"]],
    case_field=["TARGET_FID", "amenity", "building"]
)

print("Generated summary table with statistics for 'amenity' and 'building'.")
print(f"Summary table saved at: {summary_table}")
