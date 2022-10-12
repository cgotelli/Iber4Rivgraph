#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:08:14 2022

@author: epfl-lhe
"""

import functions as f


RastersPath = "/mnt/data1/GITHUB/Iber4Rivgraph/Rasters/"
extension = ".asc"


# Set the exit sides of the river relative to the image. In this case, the
# Brahmaputra is "entering" the image from the North and "exiting" the 
# image from the South.
es = 'WE' # The first character is the upstream side

maxSize = 5

dischargeThreshold = 0.005 # In q^2/s

# We convert the water depth raster to binary masks. They are stored in a new "Masks" folder inside
# the RastersPath folder.
f.preprocess(RastersPath, extension, dischargeThreshold, maxSize)

# We read the masks and process them:
f.getNetwork(RastersPath)

# f.getNetwork(RastersPath)
