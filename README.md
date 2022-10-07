# Iber for Rivgraph

Using Rivgraph to analyze Iber result _*.asc_ files to work with Rivgraph. [documentation](https://veinsoftheearth.github.io/RivGraph/) and
[repository](https://github.com/VeinsOfTheEarth/RivGraph)

Tejedor et al. (2022)[^1]

## Installing Rivgraph  

You have two different ways to install rivgraph:

- **With Anaconda[^2]:** We create a new environment that comes with rigraph included.  
    ```
    conda create -n Iber4Rivgrap rivgraph -c conda-forge
    ```  

- **With mamba:**
  1. We create a new environment first.
    ```
    conda env create -n Iber4Rivgraph
    ```  
  2. Once it finishes, we activate this new environment.  
    ```
    conda activate Iber4Rivgraph
    ```  
  3. Then we use Mambaforge to install rivgraph from the conda-forge channel.  
    ```
    mamba install rivgraph -c conda-forge
    ```  



### **What is mamba and how to install it?**

**mamba** is a CLI tool to manage conda s environments. If you already know **conda**, great, you already know **mamba!**

If you’re new to this world, don’t panic you will find everything you need in [its documentation](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html#mamba). We recommend to get familiar with [these concepts](https://mamba.readthedocs.io/en/latest/user_guide/concepts.html#concepts) first.

There are different ways of installing **mamba**, rather when you have Anaconda already installed or not. 

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

## Using the code  

The analysis with RivGraph of the To analyze the results of depth obtained with Iber it is necessary to follow the steps listed below:  
1. The _*.asc_ file exported from Iber (Using the "Export results to Raster or XYZ" option).
2. Use the `main.py` script to apply the following steps to the file:
    - Creates the mask from the depth map,
    - Tide up of the mask,
    - Computing a graphical representation of the mask,
    - Pruning the network,
    - Converting the graph to a NetworkX object,
    - Getting other parameters from the Network.


[^2]: Sometimes Anaconda has problems to install Rivgraph (it keeps looking forever for the package). For that case, it is better to use **mamba**.
[^1]: Tejedor, A., Schwenk, J., Kleinhans, M., Limaye, A. B., Vulis, L., Carling, P., et al. (2022). The entropic Braiding Index (eBI): A robust metric to account for the diversity of channel scales in multi-thread rivers. Geophysical Research Letters, 49, e2022GL099681. https://doi.org/10.1029/2022GL099681
