#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 11:37:26 2022

@author: gotelli
"""

import numpy as np

from os import listdir, mkdir
from os.path import join, exists

from osgeo import gdal, osr

from matplotlib import pyplot as plt

from rivgraph.classes import river
import rivgraph.rivers.river_utils as ru

from scipy.io import savemat

# import rivgraph.deltas.delta_metrics as dm

# import networkx as nx
plt.style.use('ggplot')

def preprocess(rasterFolder, extension, dischargeThreshold, maxSize, plots):
    """


    Parameters
    ----------
    rasterFolder : TYPE
        DESCRIPTION.
    extension : TYPE
        DESCRIPTION.
    dischargeThreshold : TYPE
        DESCRIPTION.
    maxSize : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    print("----------------------")
    print("Pre process started.\n")

    rasterFiles = sorted(listdir(rasterFolder))
    for file in rasterFiles:
        if file.endswith(extension):

            print("\t - Processing raster: " + file)
            rasterName = join(rasterFolder, file)
            # Transforms the Raster into a Binary Mask
            binarizeRaster(rasterName, rasterFolder, file, dischargeThreshold, maxSize, plots)

    print("\nPre process finished.")
    print("----------------------\n")

    return None


def getNetwork(RastersPath, mesh_path, es, plots):
    """


    Parameters
    ----------
    RastersPath : TYPE
        DESCRIPTION.
    mesh_path : TYPE
        DESCRIPTION.
    es : TYPE
        DESCRIPTION.

    Returns
    -------
    links : TYPE
        DESCRIPTION.
    nodes : TYPE
        DESCRIPTION.
    ebi : TYPE
        DESCRIPTION.
    bi : TYPE
        DESCRIPTION.

    """

    rasterFolder = join(RastersPath, "Masks")
    rasterFiles = sorted(listdir(rasterFolder))
    resultsFolder = join(RastersPath, "Results")

    # Creates output folder if it does not exist
    if not exists(resultsFolder):
        mkdir(resultsFolder)

    print("Getting Network from Masks\n")

    # Process each file inside folder that was stored as mask. Recognizable for its name.
    for file in rasterFiles:
        if file.endswith("_mask.tif"):
            print("\t - Processing mask: " + file)
            mask_path = join(rasterFolder, file)
            name = file[:-9]

            # Creates river class object.
            braidedRiver = river(name, mask_path, resultsFolder, exit_sides=es, verbose=plots)

            # Plots the mask.
            if plots:
                plt.figure(figsize=(20, 4))
                plt.imshow(braidedRiver.Imask, interpolation="none", cmap="gray")
                plt.title("Input tidy mask")
                plt.axis("off")
                plt.show()

            # SKELETONIZE THE BINARY MASK
            # Simply use the skeletonize() method.
            braidedRiver.skeletonize()

            # Plots the skeletonized image.
            if plots:
                # The skeletonized image is stored as an attribute to the river class.
                plt.figure(figsize=(20, 4))
                plt.imshow(braidedRiver.Iskel)
                plt.title("Skeleton")
                plt.axis("off")
                plt.show()

            # COMPUTE THE NETWORK FROM SKELETONIZED MASK
            # Simply use the compute_network() method.
            braidedRiver.compute_network()

            # Now we can see that the "links" and "nodes" dictionaries have been added
            # as attributes to the river class:
            links = braidedRiver.links
            nodes = braidedRiver.nodes

            # Exports the results to JSON files
            braidedRiver.to_geovectors("network", ftype="json")

            # Prints the information of links and nodes
            if plots:
                print("links: {}".format(links.keys()))
                print("nodes: {}".format(nodes.keys()))

                # Plots the river network.
                braidedRiver.plot("network")

            if plots:
                # Let's see where the network geovector files were written:
                print(braidedRiver.paths["links"])
                print(braidedRiver.paths["nodes"])

            # Prune the network
            braidedRiver.prune_network()

            if plots:
                braidedRiver.plot("network")


            if plots:
                # We see that 'inlets' and 'outlets' have been added to the nodes dictionary:
                print(braidedRiver.nodes.keys())

                # We can get the node ids of the inlets and outlets
                print("inlets:", braidedRiver.nodes["inlets"])
                print("outlets:", braidedRiver.nodes["outlets"])

            # COMPUTE MORPHOLOGIC METRICS (LENGTHS, WIDTHS)
            braidedRiver.compute_link_width_and_length()

            if plots:
                print("Links keys")
                print(braidedRiver.links.keys())

            braidedRiver.to_geovectors("network", ftype="json")

            if plots:
                # Let's look at histograms of link widths and lengths:
                plt.hist(braidedRiver.links["len_adj"], bins=20)
                plt.ylabel("count")
                plt.xlabel("link length (m)")
                plt.title("Histogram of link lengths")
                plt.show()

            # print(braidedRiver.unit)
            if plots:
                plt.hist(braidedRiver.links["wid_adj"], bins=20)
                plt.ylabel("count")
                plt.xlabel("link width (m)")
                plt.title("Histogram of link widths")
                plt.show()

            # Loads mesh file created with QGis
            ebi, bi = ru.compute_eBI(mesh_path, braidedRiver.paths["links"], method="avg")

            # As the mesh was made with QGis and the transect tool, it doesn't have the same format
            # as expected by RivGraph (For each transect it has to lines that make that transect,
            # one from the centerline to each side). The way to fix it is to take only one value per
            # line.
            bi = bi[::2]
            ebi = ebi[::2]
            
            # Gets the adjacency matrix
            am = braidedRiver.adjacency_matrix()
            
            # Plots both BI and eBI.
            if plots:
                plt.plot(bi, label="BI")
                plt.plot(ebi, label="eBI")
                plt.legend()
                plt.ylabel("Value")
                plt.xlabel("Transect [m]")
                plt.show()

            # Export output as Matfile
            savemat(
                join(resultsFolder, str(file[:-8] + "_output.mat")),
                {"eBI": ebi, "BI": bi, "links": links, "nodes": nodes, "Adjmat": am},
            )
            
            # TODO: Incluir la opción 
            # braidedRiver.assign_flow_directions()

    print("Getting Network from Masks finished \n")

    return links, nodes, ebi, bi, am


def binarizeRaster(rasterName, rasterFolder, file, dischargeThreshold, maxSize, plots):
    """


    Parameters
    ----------
    rasterName : TYPE
        DESCRIPTION.
    rasterFolder : TYPE
        DESCRIPTION.
    file : TYPE
        DESCRIPTION.
    dischargeThreshold : TYPE
        DESCRIPTION.
    maxSize : TYPE
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
    selection_nodata = np.logical_not(myarray == -9999.0)

    # Same with all elements whose value is below the threshold.
    selection_discharge = np.logical_not(myarray < dischargeThreshold)

    # Creates a new array of the same size of the raster, with zeros only.
    new_array = [[0 for i in range(band.XSize)] for j in range(band.YSize)]

    # On every element where we have a true in the boolean matrix, the new array will have a 1.
    for i, item in enumerate(myarray):
        for j, element in enumerate(item):
            if selection_nodata[i][j] == True:
                new_array[i][j] = 1
            else:
                new_array[i][j] = 0

    # On every element where we have a true in the boolean matrices, the new array will have a 1.
    for i, item in enumerate(myarray):
        for j, element in enumerate(item):
            if selection_discharge[i][j] == True:
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

    # New output file's name
    output_file = join(masks_folder, file[:-4] + "_mask.tif")

    dst_ds = driver.Create(output_file, band.XSize, band.YSize, 1, gdal.GDT_Int16)

    # Transforms into array
    new_array = np.array(new_array)

    # Tidy up the array removing noise
    new_array = tidy(new_array, maxSize, plots)

    # writting output raster
    dst_ds.GetRasterBand(1).WriteArray(new_array)
    # setting nodata value
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999.0)
    # setting extension of output raster
    # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
    dst_ds.SetGeoTransform(geotransform)
    # setting spatial reference of output raster
    srs = osr.SpatialReference()

    # Sets a metric CRS
    srs.SetFromUserInput("EPSG:32719")

    dst_ds.SetProjection(srs.ExportToWkt())

    # Close output raster dataset
    ds = None
    dst_ds = None


def tidy(Im, maxSize, plots):
    """


    Parameters
    ----------
    Im : TYPE
        DESCRIPTION.
    maxSize : TYPE
        DESCRIPTION.

    Returns
    -------
    Ihf : TYPE
        DESCRIPTION.

    """

    # Tidying up the mask
    from rivgraph import im_utils as iu

    if plots:
        plt.figure(figsize=(20, 4))
        plt.imshow(Im, interpolation="none", cmap="gray")
        plt.title("Original image before tidy")
        plt.axis("off")
        plt.show()

    # First, let's remove anything that isn't connected to the largest blob of the image
    Ib = iu.largest_blobs(
        Im, action="keep"
    )  # action can also be 'remove' if we want to delete it instead

    if plots:
        # Now take a look
        plt.figure(figsize=(20, 4))
        plt.imshow(Ib, interpolation="none", cmap="gray")
        plt.title("Biggest blob in original image")
        plt.axis("off")
        plt.show()

    return Ib
