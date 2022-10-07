#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:08:14 2022

@author: epfl-lhe
"""

import functions as f

RastersPath = "/mnt/data1/GITHUB/Iber4Rivgraph/Rasters/"
extension = ".asc"

# We convert the water depth raster to 
f.createMasks(RastersPath, extension)
