# Iber for Rivgraph
Functions for preparing Iber output files to work with Rivgraph


You have two different ways to install rivgraph:

- **With Anaconda:** We create a new environment that comes with rigraph included.

`conda create -n Iber4Rivgrap rivgraph -c conda-forge`
- **With Mambaforge:** We create a new environment first.

`conda env create -n Iber4Rivgraph`

Once it finishes, we activate this new environment.

`conda activate Iber4Rivgraph`

Then we use Mambaforge to install rivgraph from the conda-forge channel.

`mamba install rivgraph -c conda-forge`



### **How to install Mambaforge?**

In **Unix-like platforms**, open a terminal and enter:

```raw
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"
bash Mambaforge-$(uname)-$(uname -m).sh
```  
