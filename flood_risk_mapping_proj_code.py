import arcpy

# Set workspace
arcpy.env.workspace = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb"
arcpy.env.overwriteOutput = True

# Input datasets (two layers for river networks)
water_areas = r"C:\Users\Dell\Downloads\paradigms prev\prog lang and paradigms spring 2023\river networks dataset shapfile\uae rivers shape file\ARE_water_areas_dcw.shp"
water_lines = r"C:\Users\Dell\Downloads\paradigms prev\prog lang and paradigms spring 2023\river networks dataset shapfile\uae rivers shape file\ARE_water_lines_dcw.shp"
land_use = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\LandUseLandcover_Clip"  # Corrected path
rainfall_data = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\rainfall_uae_Clip"  # Corrected path

# Output file paths (geodatabase feature classes)
buffer_500m_areas = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Water_Areas_Buffer_500m"
buffer_1km_areas = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Water_Areas_Buffer_1km"
buffer_500m_lines = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Water_Lines_Buffer_500m"
buffer_1km_lines = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Water_Lines_Buffer_1km"
merged_buffer_500m = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Merged_Buffer_500m"
merged_buffer_1km = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Merged_Buffer_1km"
flood_prone_areas = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\Flood_Prone_Zones"
high_risk_areas = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Risk_Mapping.gdb\High_Risk_Zones"
export_shapefile = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Flood_Prone_Zones.shp"

# Step 1: Buffer water areas and water lines separately
arcpy.Buffer_analysis(water_areas, buffer_500m_areas, "500 Meters", dissolve_option="ALL")
arcpy.Buffer_analysis(water_areas, buffer_1km_areas, "1 Kilometers", dissolve_option="ALL")
arcpy.Buffer_analysis(water_lines, buffer_500m_lines, "500 Meters", dissolve_option="ALL")
arcpy.Buffer_analysis(water_lines, buffer_1km_lines, "1 Kilometers", dissolve_option="ALL")

# Step 2: Merge buffered outputs to form a unified flood-prone zone
arcpy.Merge_management([buffer_500m_areas, buffer_500m_lines], merged_buffer_500m)
arcpy.Merge_management([buffer_1km_areas, buffer_1km_lines], merged_buffer_1km)

# Step 3: Intersect buffers with land use to find affected land types
arcpy.Intersect_analysis([merged_buffer_1km, land_use], flood_prone_areas, "ALL")

# Step 4: Overlay rainfall data to identify high-risk zones
arcpy.Intersect_analysis([flood_prone_areas, rainfall_data], high_risk_areas, "ALL")

# Step 5: Export the high-risk zones as a shapefile
arcpy.CopyFeatures_management(high_risk_areas, export_shapefile)

# Step 6: Summarize total area at risk per land use category
summary_table = r"C:\Users\Dell\Documents\ArcGIS\Projects\Flood_Risk_Mapping\Risk_Summary.dbf"
arcpy.Statistics_analysis(high_risk_areas, summary_table, [["Shape_Area", "SUM"]], "Land_Use_Type")

print("Flood risk mapping completed. Outputs:")
print(f" - Buffered water areas and lines: {buffer_500m_areas}, {buffer_1km_areas}, {buffer_500m_lines}, {buffer_1km_lines}")
print(f" - Merged buffered zones: {merged_buffer_500m}, {merged_buffer_1km}")
print(f" - Flood-prone areas: {flood_prone_areas}")
print(f" - High-risk zones: {high_risk_areas}")
print(f" - Exported flood-prone zones shapefile: {export_shapefile}")
print(f" - Summary report generated at: {summary_table}")
