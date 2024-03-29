# Iber for Rivgraph

This is a code for using Rivgraph to analyze the results obtained with Iber. It looks forward to get the parameters explained in the work done by Tejedor et al. (2015a[^1], 2015b[^2], 2022[^3]). Below there is an explanation on how to use the code and process the results.    

[Iber](https://www.iberaula.es/1070/iber-model/about-the-model) is a two-dimensional numerical model for the simulation of free surface flow in rivers and estuaries. Iber solves the full depth-averaged shallow water equations in order to compute the water depth and the two horizontal components of the depth-averaged velocity.  

[Rivgraph](https://github.com/VeinsOfTheEarth/RivGraph) is a Python package that provides tools for converting a binary mask of a channel network into a directed, weighted graph (i.e. a set of connected links and nodes). You can see some description of RivGraph's functionality via this [AGU poster](https://www.researchgate.net/publication/329845073_Automatic_Extraction_of_Channel_Network_Topology_RivGraph), and the flow directionality logic and validation is described in their [ESurf Dynamics paper](https://www.earth-surf-dynam.net/8/87/2020/esurf-8-87-2020.html). Check the [documentation](https://veinsoftheearth.github.io/RivGraph/) for further information.

## Installing Rivgraph  

Rivgraph must be installed in a new environment to make it sure it will work. The simplest way of doing it is to create a new environment using the YML file available in this repository. This file contains not only Rivgraph but also other packages that are necessary for the postprocess of the data. to create this environment, you just have to enter in your console the following code:

```
conda env create -f Iber4Rivgraph.yml
```

If you prefer to create a new environment from scratch, you can do it both in **mamba** or in **Anaconda[^4]**.

- **With Anaconda:** We create a new environment that comes with rigraph included.  
    ```
    conda create -n Iber4Rivgraph rivgraph -c conda-forge
    ```  

- **With mamba:**  
    ```
    mamba create -n Iber4Rivgraph rivgraph -c conda-forge
    ```  

### **What is mamba and how to install it?**

**mamba** is a CLI tool to manage conda s environments. If you already know **conda**, great, you already know **mamba!**

If you’re new to this world, don’t panic you will find everything you need in [its documentation](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html#mamba). We recommend to get familiar with [these concepts](https://mamba.readthedocs.io/en/latest/user_guide/concepts.html#concepts) first.

There are different ways of installing **mamba**, whether you have Anaconda already installed or not. 

The recommended way is to do a *fresh install* without Anaconda. For that, in **Unix-like platforms**, open a terminal and enter:

```raw
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash Mambaforge-$(uname)-$(uname -m).sh
```  
For Windows, just download the installer from [here](https://github.com/conda-forge/miniforge#mambaforge) and execute it.

If you already have Anaconda, you can install **mamba* with the following code:
```
conda install mamba -n base -c conda-forge
```

## Preparing the data from Iber

Before running Rivgraph is necessary to export the **specific discharge** data from Iber as ASC file. To do it just follow the steps listed below: 

1. In the postprocess mode, press the button **Export results to Raster or XYZ**.

<p align="center">
  <img src="/Images/RasterExport_01.png" width="500" title="Button to select.">
</p>

2. Select **Specific Discharge (m2/s)**, the step and the cell size for the output Raster. 

<p align="center">
  <img src="/Images/RasterExport_02.png" width="300" title="Exportation pop up.">
</p>

3. The Raster file will be created and saved inside the Iber's project folder. The total discharge (not in x or y) is the file to be used with Rivgraph.
<p align="center">
  <img src="/Images/RasterExport_03.png" width="800" title="Files saved in Project's folder.">
</p>

It is also necessary to manually create the Mesh on which we will compute the different metrics (BI and eBI). For that task there are many different ways. We recommend to use the QGis. You just need to create a centerline, split it into different pieces of the size you wish (you can use the function **Split lines by maximum length** for that), and then create the transects by using the tool **Transect**. The result should look like this:

<p align="center">
  <img src="/Images/Mesh.png" width="900" title="Mesh example.">
</p>

## The code  

For running the code it is necessary to execute the file `main.py` with Spyder or any other IDE. This code reads Specific Discharge Raster, creates the mask and process it with Rivgraph to obtain different Morphologic metrics.

The structure of the folders and their contents are shown and explained below in a file tree.

```raw
├── main.py
├── functions.py
├── Mesh
│   └── mesh.geojson
└── Rasters
    ├── Masks*
    └── Results*
```
> **\*** These folders are automatically created by the code.  

- `main.py` is the file that calls all the functions and has the necessary parameters to go from Iber to the final output with the Morphologic metrics.
- `functions.py` is the script containing all the functions that are used. Some specific parameters that were set for the braided river flume at LHE must be modified inside.
- *Mesh* is the folder where the "handmade" mesh is stored. This file must be saved from QGis as a GeoJson file.
- *Rasters* is the folder in which all the rasters file to be processed are stored.
- Both *Masks* and *Results* folders are created by the code to store the results for each processed raster file.

### Code's workflow

So far the code does the following:

1. Creates the mask from the depth map,
2. Tidy-up of the mask,
3. Computing a graphical representation of the mask,
4. Prunes the network,
5. Gets the nodes, links, and BI and eBI values,
6. Exports these values for later use.


### Using the code

The code needs some inputs to work. These parameters are:  

- **rastersPath: Path to the folder containing the raster files.**
- **extension:** Extension of the raster files. Normally should be _*.asc_.
- **meshPath:** Path to the folder where the mesh geojson file is saved.
- **direction:** Input-to-Output movement direction in cardinal terms (e.g., "WE": West to East).
- **dischargeThreshold:** Threshold value for discharge to be considered important to be a part of the network. This value is hand picked based on calibration/comparison of images with simulation outputs.   
- **showPlots:** Boolean to indicate if plots are to be shown or not. Recommended to check process the first times. 

Once these parameters are correctly entered, it is just necessary to run the code. The folders with masks and results should appear automatically.

> :warning: **DO NOT FORGET TO ACTIVATE THE ENVIRONMENT BEFORE RUNNING THE CODE!**


[^1]: Tejedor, A., Schwenk, J., Kleinhans, M., Limaye, A. B., Vulis, L., Carling, P., et al. (2022). The entropic Braiding Index (eBI): A robust metric to account for the diversity of channel scales in multi-thread rivers. Geophysical Research Letters, 49, e2022GL099681. https://doi.org/10.1029/2022GL099681
[^2]: Tejedor, A., A. Longjas, I. Zaliapin, and E. Foufoula-Georgiou (2015), Delta channel networks: 1. A graph-theoretic approach for studying connectivity and steady state transport on deltaic surfaces, Water Resour. Res., 51, 3998–4018, https://doi.org/10.1002/2014WR016577.
[^3]: Tejedor, A., A. Longjas, I. Zaliapin, and E. Foufoula-Georgiou (2015), Delta channel networks: 2. Metrics of topologic and dynamic complexity for
delta comparison, physical inference, and vulnerability assessment, Water Resour. Res., 51, 4019–4045, https://doi.org/10.1002/2014WR016604.
[^4]: Sometimes Anaconda has problems to install Rivgraph (it keeps looking forever for the package). For that case, it is better to use **mamba**.
