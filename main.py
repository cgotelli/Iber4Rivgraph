#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:08:14 2022

@author: epfl-lhe
"""


import functions as f

# -------------- Files' paths ---------------
RastersPath = "/mnt/data1/GITHUB/Iber4Rivgraph/Rasters/"
extension = ".asc"
mesh_path = "/mnt/data1/GITHUB/Iber4Rivgraph/Mesh/mesh.geojson"

# ---------- Necessary parameters -----------

# Set the exit sides of the river relative to the image. In this case, the
# Brahmaputra is "entering" the image from the West and "exiting" the
# image from the East.
es = "WE"  # The first character is the upstream side

maxSize = 5

dischargeThreshold = 0.01  # In q^2/s

plots = True


# ---- DO NOT MODIFY FROM THIS POINT DOWN ---
# -------------- Files' paths ---------------

# We convert the water depth raster to binary masks. They are stored in a new "Masks" folder inside
# the RastersPath folder.
f.preprocess(RastersPath, extension, dischargeThreshold, maxSize, plots)

# We read the masks and process them:
links, nodes, ebi, bi, am = f.getNetwork(RastersPath, mesh_path, es, plots)
