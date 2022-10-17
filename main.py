#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:08:14 2022

@author: epfl-lhe
"""


import functions as f

# -------------- Files' paths ---------------
rastersPath = "/mnt/data1/GITHUB/Iber4Rivgraph/Rasters/"
extension = ".asc"
meshPath = "/mnt/data1/GITHUB/Iber4Rivgraph/Mesh/mesh.geojson"

# ---------- Process parameters -----------

# Set the exit sides of the river relative to the image. In this case, the
# Brahmaputra is "entering" the image from the West and "exiting" the
# image from the East.
direction = "WE"  # The first character is the upstream side

dischargeThreshold = 0.01  # In q^2/s

showPlots = True  # To plot or not the figures.


# ---- DO NOT MODIFY FROM THIS POINT DOWN ---
# -------------- Files' paths ---------------

# We convert the water depth raster to binary masks. They are stored in a new "Masks" folder inside
# the RastersPath folder.
f.preprocess(rastersPath, extension, dischargeThreshold, showPlots)

# We read the masks and process them:
links, nodes, ebi, bi, am = f.getNetwork(rastersPath, meshPath, direction, showPlots)


# TODO: Include the computation of all other parameters explained in Tejedor et al. (2015a, 2015b).
