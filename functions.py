#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 11:37:26 2022

@author: gotelli
"""

import numpy as np

from os import listdir

from os.path import isfile, join, exists
from os import listdir, mkdir
from osgeo import gdal, osr


def createMasks(rasterFolder, extension, depthThreshold, dischargeThreshold):
    """


    Parameters
    ----------
    rasterFolder : TYPE
        DESCRIPTION.
    extension : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    rasterFiles = sorted(listdir(rasterFolder))
    for file in rasterFiles:
        if file.endswith(extension):

            print("Processing: " + file)

            rasterName = join(rasterFolder, file)
            binarizeRaster(rasterName, rasterFolder, file, depthThreshold, dischargeThreshold)

    return None


def binarizeRaster(rasterName, rasterFolder, file, depthThreshold, dischargeThreshold):
    """


    Parameters
    ----------
    rasterName : TYPE
        DESCRIPTION.
    rasterFolder : TYPE
        DESCRIPTION.
    file : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # It opens the raster file as an array
    ds = gdal.Open(rasterName)
    band = ds.GetRasterBand(1)
    myarray = np.array(band.ReadAsArray())
    
    # Creates an array of the same size of the raster, on which all the NoData elements 
    # (equal to -9999.0) are True and the rest are False.
    selection = np.logical_not(myarray == -9999.0)

    # Creates a new array of the same size of the raster, with zeros only.
    new_array = [[0 for i in range(band.XSize)] for j in range(band.YSize)]

    # On every element where we have a true in the boolean matrix, the new array will have a 1.
    for i, item in enumerate(myarray):
        for j, element in enumerate(item):
            if selection[i][j] == True:
                new_array[i][j] = 1
            else:
                new_array[i][j] = 0
    
    # It gets the geo transformation 
    geotransform = ds.GetGeoTransform()
    
    # Create gtif file
    driver = gdal.GetDriverByName("GTiff")

    masks_folder = join(rasterFolder, "Masks")
    if not exists(masks_folder):
        mkdir(masks_folder)

    output_file = join(masks_folder, file[:-4] + "_mask.tif")

    dst_ds = driver.Create(output_file, band.XSize, band.YSize, 1, gdal.GDT_Int16)

    new_array = np.array(new_array)

    # writting output raster
    dst_ds.GetRasterBand(1).WriteArray(new_array)
    # setting nodata value
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999.0)
    # setting extension of output raster
    # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
    dst_ds.SetGeoTransform(geotransform)
    # setting spatial reference of output raster
    srs = osr.SpatialReference()

    srs.SetFromUserInput("EPSG:32719")

    dst_ds.SetProjection(srs.ExportToWkt())
    # Close output raster dataset

    ds = None
    dst_ds = None
