# -*- coding: utf-8 -*-
import arcpy
import os

# Set workspace to the MDB path
mdb_path = arcpy.GetParameterAsText(0)  # Toolbox input
arcpy.env.workspace = mdb_path

# Access the current map document and data frame
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

# List feature classes
feature_classes = arcpy.ListFeatureClasses()

if not feature_classes:
    arcpy.AddMessage("❌ No feature classes found in the MDB file.")
else:
    for fc in feature_classes:
        try:
            # Full path to feature class
            fc_path = os.path.join(mdb_path, fc)

            # Create a Layer object and name it cleanly
            layer = arcpy.mapping.Layer(fc_path)
            layer.name = fc

            # Add to map
            arcpy.mapping.AddLayer(df, layer, "BOTTOM")
            arcpy.AddMessage("✅ Added: {}".format(fc))

        except Exception as e:
            arcpy.AddWarning("⚠️ Failed to add {}: {}".format(fc, e))

    # Refresh view
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    arcpy.AddMessage("🎉 All layers processed.")
