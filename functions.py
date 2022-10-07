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


def createMasks(rasterFolder, extension):
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
            binarizeRaster(rasterName, rasterFolder, file)

    return None


def binarizeRaster(rasterName, rasterFolder, file):
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
    ds = gdal.Open(rasterName)
    band = ds.GetRasterBand(1)
    myarray = np.array(band.ReadAsArray())
    selection = np.logical_not(myarray == -9999.0)

    new_array = [[0 for i in range(band.XSize)] for j in range(band.YSize)]

    for i, item in enumerate(myarray):
        for j, element in enumerate(item):
            if selection[i][j] == True:
                new_array[i][j] = 1
            else:
                new_array[i][j] = 0
    geotransform = ds.GetGeoTransform()
    # wkt = ds.GetProjection()

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
